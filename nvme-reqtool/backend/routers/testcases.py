from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud import (
    create_testcase,
    delete_testcase,
    get_testcase,
    get_testcases,
    link_testcase,
    unlink_testcase,
    update_testcase,
)
from database import get_db
from schemas import TestCaseCreate, TestCaseRead, TestCaseUpdate

router = APIRouter(prefix="/api", tags=["testcases"])


@router.get("/testcases", response_model=list[TestCaseRead])
async def list_testcases(
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await get_testcases(db, category, status)


@router.post("/testcases", response_model=TestCaseRead, status_code=201)
async def create(data: TestCaseCreate, db: AsyncSession = Depends(get_db)):
    return await create_testcase(db, data)


@router.patch("/testcases/{tc_id}", response_model=TestCaseRead)
async def patch(tc_id: str, data: TestCaseUpdate, db: AsyncSession = Depends(get_db)):
    tc = await update_testcase(db, tc_id, data)
    if not tc:
        raise HTTPException(404, "TestCase not found")
    return tc


@router.delete("/testcases/{tc_id}", status_code=204)
async def remove(tc_id: str, db: AsyncSession = Depends(get_db)):
    ok = await delete_testcase(db, tc_id)
    if not ok:
        raise HTTPException(404, "TestCase not found")


@router.post("/requirements/{req_id}/testcases", status_code=201)
async def link(req_id: str, tc_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    ok = await link_testcase(db, req_id, tc_id)
    if not ok:
        raise HTTPException(400, "Link failed (not found or already editing)")
    return {"linked": True}


@router.delete("/requirements/{req_id}/testcases/{tc_id}", status_code=204)
async def unlink(req_id: str, tc_id: str, db: AsyncSession = Depends(get_db)):
    ok = await unlink_testcase(db, req_id, tc_id)
    if not ok:
        raise HTTPException(404, "Link not found")
