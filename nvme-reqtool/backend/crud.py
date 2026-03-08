from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import EditSession, Requirement, TestCase, requirement_testcase
from schemas import RequirementCreate, RequirementUpdate, TestCaseCreate, TestCaseUpdate


def _now() -> str:
    return datetime.utcnow().isoformat()


# ── Requirements ──────────────────────────────────────────────


async def get_requirements(
    db: AsyncSession,
    category: str | None = None,
    status: str | None = None,
    support_status: str | None = None,
    keyword: str | None = None,
    assigned_to: str | None = None,
    derived_from: str | None = None,
):
    stmt = select(Requirement).options(selectinload(Requirement.test_cases))
    if category:
        stmt = stmt.where(Requirement.category == category)
    if status:
        stmt = stmt.where(Requirement.status == status)
    if support_status:
        stmt = stmt.where(Requirement.support_status == support_status)
    if keyword:
        stmt = stmt.where(
            Requirement.spec_text.ilike(f"%{keyword}%")
            | Requirement.spec_text_ko.ilike(f"%{keyword}%")
            | Requirement.keyword.ilike(f"%{keyword}%")
            | Requirement.id.ilike(f"%{keyword}%")
            | Requirement.derived_from.ilike(f"%{keyword}%")
        )
    if assigned_to:
        stmt = stmt.where(Requirement.assigned_to == assigned_to)
    if derived_from:
        stmt = stmt.where(Requirement.derived_from.ilike(f"%{derived_from}%"))
    stmt = stmt.order_by(Requirement.id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_requirement(db: AsyncSession, req_id: str):
    stmt = select(Requirement).options(selectinload(Requirement.test_cases)).where(Requirement.id == req_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_requirement(db: AsyncSession, data: RequirementCreate):
    now = _now()
    req = Requirement(**data.model_dump(), created_at=now, updated_at=now)
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return req


async def update_requirement(db: AsyncSession, req_id: str, data: RequirementUpdate):
    req = await get_requirement(db, req_id)
    if not req:
        return None
    updates = data.model_dump(exclude_unset=True)
    updates["updated_at"] = _now()
    for k, v in updates.items():
        setattr(req, k, v)
    await db.commit()
    await db.refresh(req)
    return req


async def delete_requirement(db: AsyncSession, req_id: str):
    req = await get_requirement(db, req_id)
    if not req:
        return False
    await db.delete(req)
    await db.commit()
    return True


async def bulk_create_requirements(db: AsyncSession, items: list[RequirementCreate]):
    now = _now()
    objs = [Requirement(**item.model_dump(), created_at=now, updated_at=now) for item in items]
    db.add_all(objs)
    await db.commit()
    return len(objs)


# ── TestCases ─────────────────────────────────────────────────


async def get_testcases(db: AsyncSession, category: str | None = None, status: str | None = None):
    stmt = select(TestCase)
    if category:
        stmt = stmt.where(TestCase.category == category)
    if status:
        stmt = stmt.where(TestCase.status == status)
    stmt = stmt.order_by(TestCase.id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_testcase(db: AsyncSession, tc_id: str):
    result = await db.execute(select(TestCase).where(TestCase.id == tc_id))
    return result.scalar_one_or_none()


async def create_testcase(db: AsyncSession, data: TestCaseCreate):
    now = _now()
    tc = TestCase(**data.model_dump(), created_at=now, updated_at=now)
    db.add(tc)
    await db.commit()
    await db.refresh(tc)
    return tc


async def update_testcase(db: AsyncSession, tc_id: str, data: TestCaseUpdate):
    tc = await get_testcase(db, tc_id)
    if not tc:
        return None
    updates = data.model_dump(exclude_unset=True)
    updates["updated_at"] = _now()
    for k, v in updates.items():
        setattr(tc, k, v)
    await db.commit()
    await db.refresh(tc)
    return tc


async def delete_testcase(db: AsyncSession, tc_id: str):
    tc = await get_testcase(db, tc_id)
    if not tc:
        return False
    await db.delete(tc)
    await db.commit()
    return True


# ── Requirement ↔ TestCase link ───────────────────────────────


async def link_testcase(db: AsyncSession, req_id: str, tc_id: str):
    req = await get_requirement(db, req_id)
    tc = await get_testcase(db, tc_id)
    if not req or not tc:
        return False
    if tc not in req.test_cases:
        req.test_cases.append(tc)
        req.updated_at = _now()
        if req.status == "OPEN":
            req.status = "LINKED"
        await db.commit()
    return True


async def unlink_testcase(db: AsyncSession, req_id: str, tc_id: str):
    req = await get_requirement(db, req_id)
    tc = await get_testcase(db, tc_id)
    if not req or not tc:
        return False
    if tc in req.test_cases:
        req.test_cases.remove(tc)
        req.updated_at = _now()
        if not req.test_cases and req.status == "LINKED":
            req.status = "OPEN"
        await db.commit()
    return True


# ── Coverage ──────────────────────────────────────────────────


async def coverage_summary(db: AsyncSession):
    total = (await db.execute(select(func.count(Requirement.id)))).scalar() or 0
    linked_stmt = (
        select(func.count(func.distinct(requirement_testcase.c.req_id)))
    )
    linked = (await db.execute(linked_stmt)).scalar() or 0
    return {
        "total_requirements": total,
        "linked_requirements": linked,
        "coverage_percent": round(linked / total * 100, 1) if total else 0,
    }


async def coverage_by_category(db: AsyncSession):
    # total per category
    total_stmt = select(Requirement.category, func.count(Requirement.id)).group_by(Requirement.category)
    totals = {row[0]: row[1] for row in (await db.execute(total_stmt)).all()}

    # linked per category
    linked_stmt = (
        select(Requirement.category, func.count(func.distinct(requirement_testcase.c.req_id)))
        .join(requirement_testcase, Requirement.id == requirement_testcase.c.req_id)
        .group_by(Requirement.category)
    )
    linkeds = {row[0]: row[1] for row in (await db.execute(linked_stmt)).all()}

    results = []
    for cat, total in sorted(totals.items()):
        linked = linkeds.get(cat, 0)
        results.append({
            "category": cat,
            "total": total,
            "linked": linked,
            "coverage_percent": round(linked / total * 100, 1) if total else 0,
        })
    return results


async def uncovered_requirements(db: AsyncSession):
    subq = select(requirement_testcase.c.req_id)
    stmt = (
        select(Requirement)
        .where(Requirement.id.notin_(subq))
        .order_by(Requirement.id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def support_status_summary(db: AsyncSession):
    stmt = select(Requirement.support_status, func.count(Requirement.id)).group_by(Requirement.support_status)
    rows = (await db.execute(stmt)).all()
    mapping = {r[0]: r[1] for r in rows}
    return {
        "supported": mapping.get("SUPPORTED", 0),
        "partial": mapping.get("PARTIAL", 0),
        "not_supported": mapping.get("NOT_SUPPORTED", 0),
        "n_a": mapping.get("N_A", 0),
        "unknown": mapping.get("UNKNOWN", 0),
    }


# ── Edit Sessions ────────────────────────────────────────────


async def start_edit(db: AsyncSession, req_id: str, username: str):
    existing = await db.execute(select(EditSession).where(EditSession.req_id == req_id))
    session = existing.scalar_one_or_none()
    if session:
        if session.username == username:
            return True
        return False  # someone else is editing
    es = EditSession(req_id=req_id, username=username, started_at=_now())
    db.add(es)
    await db.commit()
    return True


async def end_edit(db: AsyncSession, req_id: str, username: str):
    result = await db.execute(
        select(EditSession).where(EditSession.req_id == req_id, EditSession.username == username)
    )
    session = result.scalar_one_or_none()
    if session:
        await db.delete(session)
        await db.commit()


async def get_active_editors(db: AsyncSession) -> dict[str, str]:
    result = await db.execute(select(EditSession))
    return {es.req_id: es.username for es in result.scalars().all()}
