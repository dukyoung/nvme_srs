from sqlalchemy import Column, ForeignKey, Text, Table
from sqlalchemy.orm import relationship

from database import Base

requirement_testcase = Table(
    "requirement_testcase",
    Base.metadata,
    Column("req_id", Text, ForeignKey("requirement.id", ondelete="CASCADE"), primary_key=True),
    Column("tc_id", Text, ForeignKey("test_case.id", ondelete="CASCADE"), primary_key=True),
)


class Requirement(Base):
    __tablename__ = "requirement"

    id = Column(Text, primary_key=True)
    category = Column(Text, nullable=False)      # IDENT / QUEUE / DATA_IO / NS_MGMT / MONITOR / POWER / SECURITY / INTEGRITY / FW_MGMT / VIRT
    level1 = Column(Text, nullable=False)         # 소분류명 (예: "1.1 컨트롤러 초기화 및 속성 설정")
    derived_from = Column(Text)                   # 출처 (예: "NVMe 2.2 §5.1.1", "NVMe 2.2 §3.5 CC.EN")
    spec_section = Column(Text)
    spec_text = Column(Text, nullable=False)
    spec_text_ko = Column(Text)
    keyword = Column(Text)
    controller_type = Column(Text)
    mandatory = Column(Text, default="M")

    support_status = Column(Text, default="UNKNOWN")
    support_note = Column(Text)
    fw_version = Column(Text)

    status = Column(Text, default="OPEN")
    priority = Column(Text, default="NORMAL")
    assigned_to = Column(Text)
    created_at = Column(Text)
    updated_at = Column(Text)

    test_cases = relationship("TestCase", secondary=requirement_testcase, back_populates="requirements")


class TestCase(Base):
    __tablename__ = "test_case"

    id = Column(Text, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    precondition = Column(Text)
    steps = Column(Text)
    expected = Column(Text)
    category = Column(Text)
    status = Column(Text, default="DRAFT")
    assigned_to = Column(Text)
    created_at = Column(Text)
    updated_at = Column(Text)

    requirements = relationship("Requirement", secondary=requirement_testcase, back_populates="test_cases")


class EditSession(Base):
    __tablename__ = "edit_session"

    req_id = Column(Text, primary_key=True)
    username = Column(Text)
    started_at = Column(Text)
