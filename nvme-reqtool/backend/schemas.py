from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


# ---------- Requirement ----------
class RequirementBase(BaseModel):
    id: str
    category: str
    level1: str
    derived_from: Optional[str] = None
    spec_section: Optional[str] = None
    spec_text: str
    spec_text_ko: Optional[str] = None
    keyword: Optional[str] = None
    controller_type: Optional[str] = None
    mandatory: Optional[str] = "M"
    support_status: Optional[str] = "UNKNOWN"
    support_note: Optional[str] = None
    fw_version: Optional[str] = None
    status: Optional[str] = "OPEN"
    priority: Optional[str] = "NORMAL"
    assigned_to: Optional[str] = None


class RequirementCreate(RequirementBase):
    pass


class RequirementUpdate(BaseModel):
    category: Optional[str] = None
    level1: Optional[str] = None
    derived_from: Optional[str] = None
    spec_section: Optional[str] = None
    spec_text: Optional[str] = None
    spec_text_ko: Optional[str] = None
    keyword: Optional[str] = None
    controller_type: Optional[str] = None
    mandatory: Optional[str] = None
    support_status: Optional[str] = None
    support_note: Optional[str] = None
    fw_version: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None


class RequirementRead(RequirementBase):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    tc_count: int = 0

    model_config = {"from_attributes": True}


# ---------- TestCase ----------
class TestCaseBase(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    precondition: Optional[str] = None
    steps: Optional[str] = None
    expected: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = "DRAFT"
    assigned_to: Optional[str] = None


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    precondition: Optional[str] = None
    steps: Optional[str] = None
    expected: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None


class TestCaseRead(TestCaseBase):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"from_attributes": True}


# ---------- Coverage ----------
class CoverageSummary(BaseModel):
    total_requirements: int
    linked_requirements: int
    coverage_percent: float


class CategoryCoverage(BaseModel):
    category: str
    total: int
    linked: int
    coverage_percent: float


class SupportStatusSummary(BaseModel):
    supported: int
    partial: int
    not_supported: int
    n_a: int
    unknown: int
