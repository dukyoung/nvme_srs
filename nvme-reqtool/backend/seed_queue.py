"""Insert Queue Management, Arbitration, Interrupt, Doorbell requirements into DB."""
import sqlite3
import datetime

now = datetime.datetime.now(datetime.UTC).isoformat()
c = sqlite3.connect("nvme_req.db")

reqs = [
    # === QUE Queue Management - Create I/O CQ ===
    {
        "id": "REQ-QUEUE-QUE-001",
        "level1": "QUE Queue Management",
        "level2": "Create I/O CQ",
        "derived_from": "NVMe 2.2 §5.2.1",
        "spec_section": "§5.2.1",
        "spec_text": "The controller shall support the Create I/O Completion Queue command to create I/O Completion Queues. The Queue Identifier value shall not exceed the value reported in the Number of Queues feature for I/O Completion Queues.",
        "spec_text_ko": "컨트롤러는 I/O Completion Queue를 생성하는 Create I/O Completion Queue 명령을 지원해야 한다. Queue Identifier 값은 Number of Queues 기능에서 보고된 I/O Completion Queue 수를 초과해서는 안 된다.",
        "keyword": "Create I/O CQ Queue Identifier Number of Queues",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-QUE-002",
        "level1": "QUE Queue Management",
        "level2": "Create I/O CQ",
        "derived_from": "NVMe 2.2 §5.2.1",
        "spec_section": "§5.2.1",
        "spec_text": "If the Physically Contiguous (PC) bit is cleared to '0' and CAP.CQR is set to '1', then the controller shall abort the command with a status code of Invalid Field in Command.",
        "spec_text_ko": "PC(Physically Contiguous) 비트가 '0'으로 클리어되고 CAP.CQR이 '1'로 설정된 경우, 컨트롤러는 Invalid Field in Command 상태 코드로 명령을 중단해야 한다.",
        "keyword": "Create CQ PC CAP.CQR Invalid Field",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-QUE-003",
        "level1": "QUE Queue Management",
        "level2": "Create I/O CQ",
        "derived_from": "NVMe 2.2 §5.2.1",
        "spec_section": "§5.2.1",
        "spec_text": "If the queue is located in the Controller Memory Buffer, PC is cleared to '0', and CMBLOC.CQPDS is cleared to '0', then the controller shall abort the command with a status code of Invalid Use of Controller Memory Buffer.",
        "spec_text_ko": "큐가 Controller Memory Buffer에 위치하고, PC가 '0'이며, CMBLOC.CQPDS가 '0'인 경우, 컨트롤러는 Invalid Use of Controller Memory Buffer 상태 코드로 명령을 중단해야 한다.",
        "keyword": "Create CQ CMB CMBLOC.CQPDS Invalid Use",
        "mandatory": "M",
    },

    # === QUE Queue Management - Delete I/O CQ ===
    {
        "id": "REQ-QUEUE-QUE-004",
        "level1": "QUE Queue Management",
        "level2": "Delete I/O CQ",
        "derived_from": "NVMe 2.2 §5.2.3",
        "spec_section": "§5.2.3",
        "spec_text": "If there are any associated I/O Submission Queues present when the Delete I/O Completion Queue command is issued, then the command shall abort with a status code of Invalid Queue Deletion. The Admin Completion Queue (ID 0h) shall not be specified.",
        "spec_text_ko": "Delete I/O Completion Queue 명령 발행 시 연관된 I/O Submission Queue가 존재하면, 명령은 Invalid Queue Deletion 상태 코드로 중단되어야 한다. Admin Completion Queue(ID 0h)는 지정될 수 없다.",
        "keyword": "Delete CQ associated SQ Invalid Queue Deletion",
        "mandatory": "M",
    },

    # === QUE Queue Management - Create I/O SQ ===
    {
        "id": "REQ-QUEUE-QUE-005",
        "level1": "QUE Queue Management",
        "level2": "Create I/O SQ",
        "derived_from": "NVMe 2.2 §5.2.2",
        "spec_section": "§5.2.2",
        "spec_text": "The controller shall support the Create I/O Submission Queue command. The Queue Identifier value shall not exceed the value reported in the Number of Queues feature for I/O Submission Queues.",
        "spec_text_ko": "컨트롤러는 Create I/O Submission Queue 명령을 지원해야 한다. Queue Identifier 값은 Number of Queues 기능에서 보고된 I/O Submission Queue 수를 초과해서는 안 된다.",
        "keyword": "Create I/O SQ Queue Identifier Number of Queues",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-QUE-006",
        "level1": "QUE Queue Management",
        "level2": "Create I/O SQ",
        "derived_from": "NVMe 2.2 §5.2.2",
        "spec_section": "§5.2.2",
        "spec_text": "If a PRP List is provided to describe the SQ, then the PRP List shall be maintained by host software at the same location and the values shall not be modified until the corresponding Delete I/O Submission Queue command is completed or the controller is reset.",
        "spec_text_ko": "SQ를 설명하기 위해 PRP List가 제공된 경우, PRP List는 동일한 위치에 유지되어야 하며 해당 Delete I/O Submission Queue 명령이 완료되거나 컨트롤러가 리셋될 때까지 값이 수정되어서는 안 된다.",
        "keyword": "Create SQ PRP List maintenance",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-QUE-007",
        "level1": "QUE Queue Management",
        "level2": "Create I/O SQ",
        "derived_from": "NVMe 2.2 §5.2.2",
        "spec_section": "§5.2.2",
        "spec_text": "If the NVM Set Identifier field is set to a non-zero value that is not specified in the NVM Set List and the SQ Associations capability is supported, then the controller shall abort the command with a status code of Invalid Field in Command.",
        "spec_text_ko": "NVM Set Identifier 필드가 NVM Set List에 지정되지 않은 0이 아닌 값으로 설정되고 SQ Associations 기능이 지원되는 경우, 컨트롤러는 Invalid Field in Command 상태 코드로 명령을 중단해야 한다.",
        "keyword": "Create SQ NVM Set Identifier validation",
        "mandatory": "M",
    },

    # === QUE Queue Management - Delete I/O SQ ===
    {
        "id": "REQ-QUEUE-QUE-008",
        "level1": "QUE Queue Management",
        "level2": "Delete I/O SQ",
        "derived_from": "NVMe 2.2 §5.2.4",
        "spec_section": "§5.2.4",
        "spec_text": "Upon successful completion of the Delete I/O Submission Queue command, all I/O commands previously submitted to the indicated Submission Queue shall be either explicitly completed or implicitly completed.",
        "spec_text_ko": "Delete I/O Submission Queue 명령 성공 완료 시, 해당 Submission Queue에 이전에 제출된 모든 I/O 명령은 명시적 또는 암시적으로 완료되어야 한다.",
        "keyword": "Delete SQ explicit implicit completion",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-QUE-009",
        "level1": "QUE Queue Management",
        "level2": "Delete I/O SQ",
        "derived_from": "NVMe 2.2 §5.2.4",
        "spec_section": "§5.2.4",
        "spec_text": "After successful completion of the Delete I/O Submission Queue command, the controller shall not post completion status for any I/O commands that were submitted to the deleted I/O Submission Queue. The Admin Submission Queue (ID 0h) shall not be specified.",
        "spec_text_ko": "Delete I/O Submission Queue 명령 성공 완료 후, 컨트롤러는 삭제된 I/O Submission Queue에 제출된 I/O 명령에 대한 완료 상태를 포스팅해서는 안 된다. Admin Submission Queue(ID 0h)는 지정될 수 없다.",
        "keyword": "Delete SQ no post-deletion completions",
        "mandatory": "M",
    },

    # === QUE Queue Management - Number of Queues ===
    {
        "id": "REQ-QUEUE-QUE-010",
        "level1": "QUE Queue Management",
        "level2": "Number of Queues",
        "derived_from": "NVMe 2.2 §5.1.25.2.1",
        "spec_section": "§5.1.25.2.1",
        "spec_text": "The Number of Queues feature (Feature 07h) shall only be issued during initialization prior to creation of any I/O Submission and/or Completion Queues. If issued after creation, the command shall abort with Command Sequence Error.",
        "spec_text_ko": "Number of Queues 기능(Feature 07h)은 I/O Submission 및/또는 Completion Queue 생성 전 초기화 중에만 발행되어야 한다. 생성 후 발행되면 Command Sequence Error로 중단되어야 한다.",
        "keyword": "Number of Queues Feature 07h initialization only",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-QUE-011",
        "level1": "QUE Queue Management",
        "level2": "Number of Queues",
        "derived_from": "NVMe 2.2 §5.1.25.2.1",
        "spec_section": "§5.1.25.2.1",
        "spec_text": "The controller shall allocate a minimum of one I/O Submission Queue and one I/O Completion Queue. The controller shall not change the value allocated between resets.",
        "spec_text_ko": "컨트롤러는 최소 하나의 I/O Submission Queue와 하나의 I/O Completion Queue를 할당해야 한다. 컨트롤러는 리셋 사이에 할당된 값을 변경해서는 안 된다.",
        "keyword": "Number of Queues minimum allocation no change between resets",
        "mandatory": "M",
    },

    # === ARB Arbitration ===
    {
        "id": "REQ-QUEUE-ARB-001",
        "level1": "ARB Arbitration",
        "level2": None,
        "derived_from": "NVMe 2.2 §3.4.4",
        "spec_section": "§3.4.4",
        "spec_text": "All controllers shall support the round robin command arbitration mechanism. If selected, the controller shall implement round robin command arbitration amongst all Submission Queues, including the Admin Submission Queue, with equal priority.",
        "spec_text_ko": "모든 컨트롤러는 라운드 로빈 명령 중재 메커니즘을 지원해야 한다. 선택된 경우, Admin Submission Queue를 포함한 모든 Submission Queue 간에 동일한 우선순위로 라운드 로빈 명령 중재를 구현해야 한다.",
        "keyword": "Round Robin arbitration equal priority mandatory",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-ARB-002",
        "level1": "ARB Arbitration",
        "level2": None,
        "derived_from": "NVMe 2.2 §3.4.4",
        "spec_section": "§3.4.4",
        "spec_text": "Once a Submission Queue is selected using arbitration, the Arbitration Burst setting determines the maximum number of commands that the controller may start processing from that Submission Queue before arbitration shall again take place.",
        "spec_text_ko": "중재를 통해 Submission Queue가 선택되면, Arbitration Burst 설정은 다시 중재가 수행되기 전에 컨트롤러가 해당 Submission Queue에서 처리를 시작할 수 있는 최대 명령 수를 결정한다.",
        "keyword": "Arbitration Burst maximum commands",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-ARB-003",
        "level1": "ARB Arbitration",
        "level2": None,
        "derived_from": "NVMe 2.2 §3.4.4",
        "spec_section": "§3.4.4",
        "spec_text": "A controller may optionally implement weighted round robin with urgent priority class. If implemented, Submission Queue A of higher strict priority than Submission Queue B shall have all its candidate commands start processing before commands from Submission Queue B.",
        "spec_text_ko": "컨트롤러는 선택적으로 긴급 우선순위 클래스를 가진 가중 라운드 로빈을 구현할 수 있다. 구현된 경우, 더 높은 엄격 우선순위의 Submission Queue A의 모든 후보 명령은 Submission Queue B의 명령보다 먼저 처리를 시작해야 한다.",
        "keyword": "WRR Weighted Round Robin urgent priority strict",
        "mandatory": "O",
    },

    # === INT Interrupt Management ===
    {
        "id": "REQ-QUEUE-INT-001",
        "level1": "INT Interrupt Management",
        "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.2.2",
        "spec_section": "§5.1.25.2.2",
        "spec_text": "The Interrupt Coalescing feature (Feature 08h) applies only to I/O Queues. The controller should signal an interrupt when either the Aggregation Time or the Aggregation Threshold conditions are met. If either field is cleared to 0h, interrupt coalescing is implicitly disabled.",
        "spec_text_ko": "Interrupt Coalescing 기능(Feature 08h)은 I/O Queue에만 적용된다. 컨트롤러는 Aggregation Time 또는 Aggregation Threshold 조건이 충족되면 인터럽트를 신호해야 한다. 어느 필드든 0h로 클리어되면 인터럽트 병합이 암시적으로 비활성화된다.",
        "keyword": "Interrupt Coalescing Feature 08h Aggregation Time Threshold",
        "mandatory": "O",
    },
    {
        "id": "REQ-QUEUE-INT-002",
        "level1": "INT Interrupt Management",
        "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.2.3",
        "spec_section": "§5.1.25.2.3",
        "spec_text": "The Interrupt Vector Configuration feature (Feature 09h) controls per-vector coalescing settings. By default, coalescing settings are enabled for each interrupt vector. Interrupt coalescing is not supported for the Admin Completion Queue.",
        "spec_text_ko": "Interrupt Vector Configuration 기능(Feature 09h)은 벡터별 병합 설정을 제어한다. 기본적으로 각 인터럽트 벡터에 대해 병합 설정이 활성화된다. Admin Completion Queue에 대해서는 인터럽트 병합이 지원되지 않는다.",
        "keyword": "Interrupt Vector Config Feature 09h per-vector coalescing Admin CQ",
        "mandatory": "O",
    },
    {
        "id": "REQ-QUEUE-INT-003",
        "level1": "INT Interrupt Management",
        "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.2.3",
        "spec_section": "§5.1.25.2.3",
        "spec_text": "If the Coalescing Disable (CD) bit is set to '1' in the Interrupt Vector Configuration, then any interrupt coalescing settings shall not be applied for this interrupt vector. Prior to issuing Set Features for this feature, the host shall configure the specified Interrupt Vector with an I/O Completion Queue.",
        "spec_text_ko": "Interrupt Vector Configuration에서 CD(Coalescing Disable) 비트가 '1'로 설정되면, 해당 인터럽트 벡터에 인터럽트 병합 설정이 적용되지 않아야 한다. 이 기능에 대한 Set Features 발행 전, 호스트는 지정된 Interrupt Vector를 I/O Completion Queue로 구성해야 한다.",
        "keyword": "CD Coalescing Disable bit Interrupt Vector CQ prerequisite",
        "mandatory": "O",
    },

    # === DBL Doorbell ===
    {
        "id": "REQ-QUEUE-DBL-001",
        "level1": "DBL Doorbell",
        "level2": None,
        "derived_from": "NVMe 2.2 §5.2.5",
        "spec_section": "§5.2.5",
        "spec_text": "If the Doorbell Buffer Config command is supported, each buffer supplied shall be a single physical memory page as defined by CC.MPS. The Shadow Doorbell buffer and EventIdx buffer shall be memory page aligned.",
        "spec_text_ko": "Doorbell Buffer Config 명령이 지원되는 경우, 제공되는 각 버퍼는 CC.MPS로 정의된 단일 물리적 메모리 페이지여야 한다. Shadow Doorbell 버퍼와 EventIdx 버퍼는 메모리 페이지 정렬되어야 한다.",
        "keyword": "Doorbell Buffer Config CC.MPS page aligned",
        "mandatory": "O",
    },
    {
        "id": "REQ-QUEUE-DBL-002",
        "level1": "DBL Doorbell",
        "level2": None,
        "derived_from": "NVMe 2.2 §5.2.5",
        "spec_section": "§5.2.5",
        "spec_text": "The controller shall ensure the following buffer size constraint is satisfied: (4 << CAP.DSTRD) * (max(NSQA, NCQA)+1) <= (2^(12+CC.MPS)). If the buffer memory addresses are invalid, a status code of Invalid Field in Command shall be returned.",
        "spec_text_ko": "컨트롤러는 다음 버퍼 크기 제약 조건이 충족되는지 확인해야 한다: (4 << CAP.DSTRD) * (max(NSQA, NCQA)+1) <= (2^(12+CC.MPS)). 버퍼 메모리 주소가 유효하지 않으면 Invalid Field in Command 상태 코드가 반환되어야 한다.",
        "keyword": "Doorbell Buffer size constraint CAP.DSTRD validation",
        "mandatory": "O",
    },
]

for r in reqs:
    r.setdefault("category", "QUEUE")
    r.setdefault("controller_type", "BOTH")
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
print(f"\nImported {len(reqs)} Queue requirements.")
