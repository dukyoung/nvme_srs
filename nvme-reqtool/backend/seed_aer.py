"""Insert Asynchronous Event Request (AER) requirements into DB."""
import sqlite3
import datetime

now = datetime.datetime.now(datetime.UTC).isoformat()
c = sqlite3.connect("nvme_req.db")

reqs = [
    # --- AER 기본 동작 ---
    {
        "id": "REQ-QUEUE-AER-001",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "The controller shall support the Asynchronous Event Request command (Opcode 0Ch) to enable the reporting of asynchronous events (status, error, and health information) from the controller to the host.",
        "spec_text_ko": "컨트롤러는 비동기 이벤트(상태, 오류, 건강 정보)를 호스트에 보고할 수 있도록 Asynchronous Event Request 명령(Opcode 0Ch)을 지원해야 한다.",
        "keyword": "AER Asynchronous Event Request 0Ch",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-AER-002",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "If Asynchronous Event Request commands are outstanding when the controller is reset, then each of those commands is aborted and shall not return a CQE.",
        "spec_text_ko": "컨트롤러 리셋 시 미처리 상태의 Asynchronous Event Request 명령이 있으면, 해당 명령은 모두 중단되며 CQE를 반환해서는 안 된다.",
        "keyword": "AER reset abort no CQE",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-AER-003",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "The total number of simultaneously outstanding Asynchronous Event Request commands shall be limited by the value indicated in the Asynchronous Event Request Limit (AERL) field in the Identify Controller data structure.",
        "spec_text_ko": "동시에 미처리 상태인 Asynchronous Event Request 명령의 총 수는 Identify Controller 데이터 구조의 AERL 필드에 명시된 값으로 제한되어야 한다.",
        "keyword": "AERL Asynchronous Event Request Limit",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-AER-004",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "The number of concurrently outstanding Asynchronous Event Request commands that exceeds the AERL shall be completed with the status code Asynchronous Event Request Limit Exceeded (status value 05h).",
        "spec_text_ko": "AERL을 초과하는 동시 미처리 AER 명령은 Asynchronous Event Request Limit Exceeded(상태 값 05h) 상태 코드로 완료되어야 한다.",
        "keyword": "AER Limit Exceeded 05h",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- 이벤트 마스킹 및 클리어 ---
    {
        "id": "REQ-QUEUE-AER-005",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "When the controller reports an asynchronous event, subsequent events of that event type shall be automatically masked by the controller until the host clears that event by reading the associated log page with the Retain Asynchronous Event bit cleared to '0'. Immediate events are excluded from this masking behavior.",
        "spec_text_ko": "컨트롤러가 비동기 이벤트를 보고하면, 호스트가 Retain Asynchronous Event 비트를 '0'으로 클리어한 상태에서 관련 로그 페이지를 읽어 해당 이벤트를 클리어할 때까지 동일 이벤트 유형의 후속 이벤트는 자동으로 마스킹되어야 한다. Immediate 이벤트는 이 마스킹에서 제외된다.",
        "keyword": "AER auto mask event type Retain Asynchronous Event",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-AER-006",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "If a log page associated with an asynchronous event is not accessible because media is not ready (i.e., the controller aborts the Get Log Page command with Admin Command Media Not Ready), then the controller shall not post a CQE for that asynchronous event until the controller is able to successfully return the log page.",
        "spec_text_ko": "비동기 이벤트와 관련된 로그 페이지가 미디어 준비 미완료로 접근 불가능한 경우(Get Log Page 명령이 Admin Command Media Not Ready로 중단), 컨트롤러가 해당 로그 페이지를 성공적으로 반환할 수 있을 때까지 해당 비동기 이벤트의 CQE를 포스팅해서는 안 된다.",
        "keyword": "AER media not ready log page CQE defer",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- 이벤트 유형별 요구사항 ---
    {
        "id": "REQ-QUEUE-AER-007",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "For Error events, the controller shall set the Log Page Identifier field to the identifier of the Error Information log page (LID 01h). The host clears this event by reading the Error Information log page with the Retain Asynchronous Event bit cleared to '0'.",
        "spec_text_ko": "Error 이벤트의 경우, 컨트롤러는 Log Page Identifier 필드를 Error Information 로그 페이지 식별자(LID 01h)로 설정해야 한다. 호스트는 Retain Asynchronous Event 비트를 '0'으로 한 상태에서 Error Information 로그 페이지를 읽어 이벤트를 클리어한다.",
        "keyword": "AER Error event LID 01h Error Information",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-AER-008",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "For SMART / Health Status events, the controller shall set the Log Page Identifier field to the identifier of the SMART/Health Information log page (LID 02h). The host clears this event by reading the SMART / Health Information log page with the Retain Asynchronous Event bit cleared to '0'.",
        "spec_text_ko": "SMART / Health Status 이벤트의 경우, 컨트롤러는 Log Page Identifier 필드를 SMART/Health Information 로그 페이지 식별자(LID 02h)로 설정해야 한다. 호스트는 Retain Asynchronous Event 비트를 '0'으로 한 상태에서 SMART / Health Information 로그 페이지를 읽어 이벤트를 클리어한다.",
        "keyword": "AER SMART Health event LID 02h",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-AER-009",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "For Notice events, the controller shall set the Log Page Identifier field to the log page identifier of the appropriate log page. The host clears this event by reading that log page with the Retain Asynchronous Event bit cleared to '0'.",
        "spec_text_ko": "Notice 이벤트의 경우, 컨트롤러는 Log Page Identifier 필드를 해당 로그 페이지의 식별자로 설정해야 한다. 호스트는 Retain Asynchronous Event 비트를 '0'으로 한 상태에서 해당 로그 페이지를 읽어 이벤트를 클리어한다.",
        "keyword": "AER Notice event log page clear",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-AER-010",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "For Immediate events, if the event occurs and there is no outstanding Asynchronous Event Request command, then the event shall not be reported.",
        "spec_text_ko": "Immediate 이벤트의 경우, 이벤트 발생 시 미처리 상태의 AER 명령이 없으면 해당 이벤트는 보고되지 않아야 한다.",
        "keyword": "AER Immediate event no outstanding not reported",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- CQE 포맷 ---
    {
        "id": "REQ-QUEUE-AER-011",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "The AER completion queue entry Dword 0 shall contain: Asynchronous Event Type (AET) in bits 02:00, Asynchronous Event Information (AEI) in bits 15:08, and Log Page Identifier (LID) in bits 23:16.",
        "spec_text_ko": "AER CQE의 Dword 0은 비트 02:00에 Asynchronous Event Type(AET), 비트 15:08에 Asynchronous Event Information(AEI), 비트 23:16에 Log Page Identifier(LID)를 포함해야 한다.",
        "keyword": "AER CQE Dword0 AET AEI LID",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- 이벤트 큐잉 ---
    {
        "id": "REQ-QUEUE-AER-012",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "If an event occurs for which reporting is enabled and there are no AER commands outstanding, the controller should retain the event information (pending event) and use it as a response to the next AER command received. If a Get Log Page clears the event prior to receiving the AER command or if a Controller Level Reset occurs, then a notification is not sent.",
        "spec_text_ko": "보고가 활성화된 이벤트 발생 시 미처리 AER 명령이 없으면, 컨트롤러는 이벤트 정보(보류 이벤트)를 유지하고 다음 AER 명령 수신 시 응답으로 사용해야 한다. AER 명령 수신 전에 Get Log Page가 이벤트를 클리어하거나 Controller Level Reset이 발생하면 알림은 전송되지 않는다.",
        "keyword": "AER pending event queue retain",
        "controller_type": "BOTH",
        "mandatory": "O",
    },
    {
        "id": "REQ-QUEUE-AER-013",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "If multiple events occur that are of different types or have different responses, the controller should retain a queue of those events for reporting in responses to subsequent Asynchronous Event Request commands.",
        "spec_text_ko": "서로 다른 유형이거나 다른 응답을 갖는 다수의 이벤트가 발생한 경우, 컨트롤러는 후속 AER 명령에 대한 응답으로 보고하기 위해 해당 이벤트들의 큐를 유지해야 한다.",
        "keyword": "AER multiple events queue different types",
        "controller_type": "BOTH",
        "mandatory": "O",
    },

    # --- Sanitize 관련 AER ---
    {
        "id": "REQ-QUEUE-AER-014",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2",
        "spec_section": "§5.1.2",
        "spec_text": "The Sanitize Operation Completed With Unexpected Deallocation asynchronous event shall be supported if the controller supports the Sanitize Config feature.",
        "spec_text_ko": "컨트롤러가 Sanitize Config 기능을 지원하는 경우, Sanitize Operation Completed With Unexpected Deallocation 비동기 이벤트를 지원해야 한다.",
        "keyword": "AER Sanitize Unexpected Deallocation",
        "controller_type": "BOTH",
        "mandatory": "C",
    },

    # --- Notice 이벤트 세부 ---
    {
        "id": "REQ-QUEUE-AER-015",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2 Figure 152",
        "spec_section": "§5.1.2",
        "spec_text": "The Attached Namespace Attribute Changed notice (AEI 00h) shall be reported for changes to Identify Namespace data structures, Active Namespace ID list, or I/O Command Set specific Active Namespace ID list of attached namespaces. The controller shall not send this event during shutdown processing or when the controller itself requests a namespace delete operation.",
        "spec_text_ko": "Attached Namespace Attribute Changed 알림(AEI 00h)은 부착된 네임스페이스의 Identify Namespace 데이터 구조, Active Namespace ID 목록, 또는 I/O Command Set 전용 Active Namespace ID 목록 변경 시 보고되어야 한다. 컨트롤러는 종료 처리 중이거나 컨트롤러 자체가 네임스페이스 삭제 작업을 요청한 경우 이 이벤트를 전송해서는 안 된다.",
        "keyword": "AER Attached Namespace Attribute Changed 00h",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-QUEUE-AER-016",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.2 Figure 152",
        "spec_section": "§5.1.2",
        "spec_text": "The Firmware Activation Starting notice (AEI 01h) shall be reported when the controller is starting a firmware activation process during which command processing is paused. The host clears this event by reading the Firmware Slot Information log page with the Retain Asynchronous Event bit cleared to '0'.",
        "spec_text_ko": "Firmware Activation Starting 알림(AEI 01h)은 명령 처리가 일시 중지되는 펌웨어 활성화 프로세스를 컨트롤러가 시작할 때 보고되어야 한다. 호스트는 Retain Asynchronous Event 비트를 '0'으로 한 상태에서 Firmware Slot Information 로그 페이지를 읽어 이벤트를 클리어한다.",
        "keyword": "AER Firmware Activation Starting 01h",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- Asynchronous Event Configuration (Set Features 0Bh) ---
    {
        "id": "REQ-QUEUE-AER-017",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.25.1.5",
        "spec_section": "§5.1.25.1.5",
        "spec_text": "The controller shall support the Asynchronous Event Configuration feature (Feature Identifier 0Bh) via the Set Features command to configure which events trigger AER notifications, including SMART/Health Critical Warnings (bits 7:0), Attached Namespace Attribute Notices, Firmware Activation Notices, Telemetry Log Notices, and other configurable events.",
        "spec_text_ko": "컨트롤러는 Set Features 명령을 통해 Asynchronous Event Configuration 기능(Feature Identifier 0Bh)을 지원하여 SMART/Health Critical Warnings(비트 7:0), Attached Namespace Attribute Notices, Firmware Activation Notices, Telemetry Log Notices 등 AER 알림을 트리거하는 이벤트를 구성할 수 있어야 한다.",
        "keyword": "AER Configuration Feature 0Bh Set Features",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- Shutdown 관련 AER ---
    {
        "id": "REQ-QUEUE-AER-018",
        "category": "QUEUE",
        "level1": "CMD Command Control",
        "level2": "AER",
        "derived_from": "NVMe 2.2 §5.1.25.1.5",
        "spec_section": "§5.1.25.1.5",
        "spec_text": "If an outstanding Asynchronous Event Request command exists and Normal NVM Subsystem Shutdown notification is enabled, the controller shall issue a Normal NVM Subsystem Shutdown event prior to shutting down.",
        "spec_text_ko": "미처리 AER 명령이 존재하고 Normal NVM Subsystem Shutdown 알림이 활성화된 경우, 컨트롤러는 종료 전에 Normal NVM Subsystem Shutdown 이벤트를 발행해야 한다.",
        "keyword": "AER Normal NVM Subsystem Shutdown",
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
print(f"\nImported {len(reqs)} AER requirements.")
