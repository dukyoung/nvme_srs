import csv
import io
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud import (
    bulk_create_requirements,
    create_requirement,
    delete_requirement,
    get_requirement,
    get_requirements,
    update_requirement,
)
from database import get_db
from schemas import RequirementCreate, RequirementRead, RequirementUpdate

router = APIRouter(prefix="/api/requirements", tags=["requirements"])


def _to_read(req) -> RequirementRead:
    return RequirementRead(
        **{c.name: getattr(req, c.name) for c in req.__table__.columns},
        tc_count=len(req.test_cases) if req.test_cases else 0,
    )


# ── 고정 경로를 먼저 정의 (/{req_id} 보다 위에) ──

@router.get("/export", response_model=None)
async def export_csv(db: AsyncSession = Depends(get_db)):
    reqs = await get_requirements(db)
    output = io.StringIO()
    fields = [
        "id", "category", "level1", "level2", "derived_from", "spec_section", "spec_text", "spec_text_ko",
        "keyword", "controller_type", "mandatory", "support_status", "support_note",
        "fw_version", "status", "priority", "assigned_to",
    ]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for r in reqs:
        writer.writerow({f: getattr(r, f) for f in fields})
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=requirements_export.csv"},
    )


@router.post("/import", status_code=201)
async def import_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    content = (await file.read()).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))
    items = []
    for row in reader:
        items.append(RequirementCreate(
            id=row["id"],
            category=row.get("category", ""),
            level1=row.get("level1", ""),
            level2=row.get("level2"),
            derived_from=row.get("derived_from"),
            spec_section=row.get("spec_section"),
            spec_text=row.get("spec_text", ""),
            spec_text_ko=row.get("spec_text_ko"),
            keyword=row.get("keyword"),
            controller_type=row.get("controller_type"),
            mandatory=row.get("mandatory", "M"),
            support_status=row.get("support_status", "UNKNOWN"),
            support_note=row.get("support_note"),
            fw_version=row.get("fw_version"),
            status=row.get("status", "OPEN"),
            priority=row.get("priority", "NORMAL"),
            assigned_to=row.get("assigned_to"),
        ))
    count = await bulk_create_requirements(db, items)
    return {"imported": count}


# ── 목록 / CRUD ──

@router.get("", response_model=list[RequirementRead])
async def list_requirements(
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    support_status: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None),
    derived_from: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    reqs = await get_requirements(db, category, status, support_status, keyword, assigned_to, derived_from)
    return [_to_read(r) for r in reqs]


@router.post("", response_model=RequirementRead, status_code=201)
async def create(data: RequirementCreate, db: AsyncSession = Depends(get_db)):
    req = await create_requirement(db, data)
    return _to_read(req)


@router.get("/{req_id}", response_model=RequirementRead)
async def read_requirement(req_id: str, db: AsyncSession = Depends(get_db)):
    req = await get_requirement(db, req_id)
    if not req:
        raise HTTPException(404, "Requirement not found")
    return _to_read(req)


@router.patch("/{req_id}", response_model=RequirementRead)
async def patch(req_id: str, data: RequirementUpdate, db: AsyncSession = Depends(get_db)):
    req = await update_requirement(db, req_id, data)
    if not req:
        raise HTTPException(404, "Requirement not found")
    return _to_read(req)


@router.delete("/{req_id}", status_code=204)
async def remove(req_id: str, db: AsyncSession = Depends(get_db)):
    ok = await delete_requirement(db, req_id)
    if not ok:
        raise HTTPException(404, "Requirement not found")
