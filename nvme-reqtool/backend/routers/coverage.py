from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import coverage_by_category, coverage_summary, support_status_summary, uncovered_requirements
from database import get_db
from schemas import RequirementRead

router = APIRouter(prefix="/api/coverage", tags=["coverage"])


@router.get("/summary")
async def summary(db: AsyncSession = Depends(get_db)):
    return await coverage_summary(db)


@router.get("/by-category")
async def by_category(db: AsyncSession = Depends(get_db)):
    return await coverage_by_category(db)


@router.get("/uncovered")
async def uncovered(db: AsyncSession = Depends(get_db)):
    reqs = await uncovered_requirements(db)
    return [
        RequirementRead(
            **{c.name: getattr(r, c.name) for c in r.__table__.columns},
            tc_count=0,
        )
        for r in reqs
    ]


@router.get("/support-status")
async def support_status(db: AsyncSession = Depends(get_db)):
    return await support_status_summary(db)
