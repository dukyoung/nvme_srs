"""Insert Abort command requirements into DB."""
import sqlite3
import datetime

now = datetime.datetime.utcnow().isoformat()
c = sqlite3.connect("nvme_req.db")

reqs = [
    {
        "id": "REQ-QUEUE-ABRT-001",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "Abort",
        "derived_from": "NVMe 2.2 §5.1.1",
        "spec_section": "§5.1.1",
        "spec_text": "The controller shall support the Abort command (Opcode 08h) to request an abort of a specific command previously submitted to the Admin Submission Queue or an I/O Submission Queue.",
        "spec_text_ko": "컨트롤러는 Admin Submission Queue 또는 I/O Submission Queue에 이전에 제출된 특정 명령의 중단을 요청하기 위한 Abort 명령어(Opcode 08h)를 지원해야 한다.",
        "keyword": "Abort 08h",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-ABRT-002",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "Abort",
        "derived_from": "NVMe 2.2 §5.1.1",
        "spec_section": "§5.1.1",
        "spec_text": "If an immediate abort is performed, the controller shall either: (a) post the CQE for the command to abort with status code Command Abort Requested before the CQE for the Abort command is posted; or (b) ensure there are no subsequent effects of the command to abort prior to posting the CQE for the Abort command, and post the CQE for the command to abort with status code Command Abort Requested (CQEs may be posted in any order).",
        "spec_text_ko": "즉시 중단(immediate abort) 수행 시, 컨트롤러는 (a) Abort 명령의 CQE 포스팅 전에 중단 대상 명령의 CQE를 Command Abort Requested 상태 코드로 포스팅하거나, (b) Abort 명령의 CQE 포스팅 전에 중단 대상 명령의 후속 효과가 없음을 보장하고 중단 대상 명령의 CQE를 Command Abort Requested로 포스팅해야 한다(CQE 순서 무관).",
        "keyword": "immediate abort CQE Command Abort Requested",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-ABRT-003",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "Abort",
        "derived_from": "NVMe 2.2 §5.1.1.1",
        "spec_section": "§5.1.1.1",
        "spec_text": "If the controller performs an immediate abort, the controller shall ensure that there are no effects of the command to abort (e.g., no host memory access, no modification of NVM media, NVM Set state, Endurance Group state, namespace state, controller state, domain state, or NVM subsystem state) subsequent to the posting of the CQE for the Abort command.",
        "spec_text_ko": "컨트롤러가 즉시 중단을 수행하는 경우, Abort 명령의 CQE 포스팅 이후 중단 대상 명령의 효과(호스트 메모리 접근, NVM 미디어/NVM Set/Endurance Group/네임스페이스/컨트롤러/도메인/NVM 서브시스템 상태 변경 등)가 없음을 보장해야 한다.",
        "keyword": "immediate abort no effects NVM media state",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-ABRT-004",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "Abort",
        "derived_from": "NVMe 2.2 §5.1.1.1",
        "spec_section": "§5.1.1.1",
        "spec_text": "If the controller is not able to ensure there are no effects of the command to abort subsequent to the posting of the CQE for the Abort command, then the controller shall not perform an immediate abort on that command.",
        "spec_text_ko": "컨트롤러가 Abort 명령의 CQE 포스팅 이후 중단 대상 명령의 효과가 없음을 보장할 수 없는 경우, 해당 명령에 대해 즉시 중단을 수행해서는 안 된다.",
        "keyword": "immediate abort prohibited data transfer",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-ABRT-005",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "Abort",
        "derived_from": "NVMe 2.2 §5.1.1",
        "spec_section": "§5.1.1",
        "spec_text": "Upon completion of the Abort command, the controller shall post a completion queue entry to the Admin Completion Queue indicating the status for the Abort command, with Dword 0 containing the Immediate Abort Not Performed (IANP) bit.",
        "spec_text_ko": "Abort 명령 완료 시, 컨트롤러는 Admin Completion Queue에 Abort 명령의 상태를 나타내는 CQE를 포스팅해야 하며, Dword 0에 Immediate Abort Not Performed(IANP) 비트를 포함해야 한다.",
        "keyword": "Abort CQE Admin Completion Queue IANP",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-ABRT-006",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "Abort",
        "derived_from": "NVMe 2.2 §5.1.1",
        "spec_section": "§5.1.1",
        "spec_text": "If the IANP bit is set to '1' in the CQE for the Abort command and a deferred abort is performed, then the controller shall set the status code for the command to abort to Command Abort Requested.",
        "spec_text_ko": "Abort 명령의 CQE에서 IANP 비트가 '1'로 설정되고 지연 중단(deferred abort)이 수행된 경우, 컨트롤러는 중단 대상 명령의 상태 코드를 Command Abort Requested로 설정해야 한다.",
        "keyword": "IANP deferred abort Command Abort Requested",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-ABRT-007",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "Abort",
        "derived_from": "NVMe 2.2 §5.1.1 Figure 313",
        "spec_section": "§5.1.1",
        "spec_text": "The controller may complete any Abort commands exceeding the Abort Command Limit (ACL) indicated in the Identify Controller data structure with the status code set to Abort Command Limit Exceeded (status value 3h).",
        "spec_text_ko": "컨트롤러는 Identify Controller 데이터 구조에 표시된 Abort Command Limit(ACL)를 초과하는 Abort 명령을 Abort Command Limit Exceeded(상태 값 3h) 상태 코드로 완료할 수 있다.",
        "keyword": "ACL Abort Command Limit Exceeded 3h",
        "controller_type": "BOTH",
        "mandatory": "O",
    },
    {
        "id": "REQ-QUEUE-ABRT-008",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "Abort",
        "derived_from": "NVMe 2.2 §5.1.1 Figure 144",
        "spec_section": "§5.1.1",
        "spec_text": "The Abort command shall use the Command Dword 10 field containing the Command Identifier (CID) in bits 31:16 and the Submission Queue Identifier (SQID) in bits 15:00 to identify the command to be aborted.",
        "spec_text_ko": "Abort 명령은 Command Dword 10 필드를 사용해야 하며, 비트 31:16에 Command Identifier(CID), 비트 15:00에 Submission Queue Identifier(SQID)를 포함하여 중단 대상 명령을 식별해야 한다.",
        "keyword": "CDW10 CID SQID Abort",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
]

for r in reqs:
    c.execute(
        """INSERT OR IGNORE INTO requirement
        (id, category, level1, level2, derived_from, spec_section, spec_text, spec_text_ko,
         keyword, controller_type, mandatory, support_status, status, priority, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            r["id"], r["category"], r["level1"], r["level2"], r["derived_from"], r["spec_section"],
            r["spec_text"], r["spec_text_ko"], r["keyword"], r["controller_type"], r["mandatory"],
            "UNKNOWN", "OPEN", "NORMAL", now, now,
        ),
    )
    print(f"  ADD: {r['id']}")

c.commit()
c.close()
print(f"\nImported {len(reqs)} Abort requirements.")
