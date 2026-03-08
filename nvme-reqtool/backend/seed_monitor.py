"""Insert MONITOR requirements into DB."""
import sqlite3, datetime
now = datetime.datetime.now(datetime.UTC).isoformat()
c = sqlite3.connect("nvme_req.db")

reqs = [
    # === SMT SMART Health Information ===
    {"id":"REQ-MON-SMT-001","level1":"SMT SMART Health Information","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.3","spec_section":"§5.1.12.1.3",
     "spec_text":"The controller shall support the SMART / Health Information log page (LID 02h). For SMART/Health Status events, the controller shall set the Log Page Identifier field to 02h.",
     "spec_text_ko":"컨트롤러는 SMART / Health Information 로그 페이지(LID 02h)를 지원해야 한다. SMART/Health Status 이벤트의 경우, 컨트롤러는 Log Page Identifier 필드를 02h로 설정해야 한다.",
     "keyword":"SMART Health LID 02h mandatory log page","mandatory":"M"},
    {"id":"REQ-MON-SMT-002","level1":"SMT SMART Health Information","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.3","spec_section":"§5.1.12.1.3",
     "spec_text":"If a namespace identifier other than 0h or FFFFFFFFh is specified by the host for the SMART / Health Information log page, the controller shall abort the command with Invalid Field in Command.",
     "spec_text_ko":"SMART / Health Information 로그 페이지에 호스트가 0h 또는 FFFFFFFFh 이외의 namespace identifier를 지정한 경우, 컨트롤러는 Invalid Field in Command로 명령을 중단해야 한다.",
     "keyword":"SMART NSID 0h FFFFFFFFh Invalid Field","mandatory":"M"},
    {"id":"REQ-MON-SMT-003","level1":"SMT SMART Health Information","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.3","spec_section":"§5.1.12.1.3",
     "spec_text":"The controller shall not set the All Media Read-Only bit to '1' in the Critical Warning field if the read-only condition on the media is a result of a change in the namespace write protection state.",
     "spec_text_ko":"컨트롤러는 미디어의 읽기 전용 상태가 네임스페이스 쓰기 보호 상태 변경으로 인한 경우 Critical Warning 필드의 All Media Read-Only 비트를 '1'로 설정해서는 안 된다.",
     "keyword":"SMART Critical Warning All Media Read-Only write protection","mandatory":"M"},
    {"id":"REQ-MON-SMT-004","level1":"SMT SMART Health Information","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.3","spec_section":"§5.1.12.1.3",
     "spec_text":"The Percentage Used (PUSED) field value shall be updated once per power-on hour when the controller is not in a sleep state.",
     "spec_text_ko":"Percentage Used(PUSED) 필드 값은 컨트롤러가 sleep 상태가 아닐 때 전원 투입 시간당 한 번 업데이트되어야 한다.",
     "keyword":"SMART PUSED Percentage Used power-on hour","mandatory":"M"},

    # === ERR Error Information ===
    {"id":"REQ-MON-ERR-001","level1":"ERR Error Information","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.2","spec_section":"§5.1.12.1.2",
     "spec_text":"The controller shall support the Error Information log page (LID 01h). For Error events, the controller shall set the Log Page Identifier field to 01h.",
     "spec_text_ko":"컨트롤러는 Error Information 로그 페이지(LID 01h)를 지원해야 한다. Error 이벤트의 경우, 컨트롤러는 Log Page Identifier 필드를 01h로 설정해야 한다.",
     "keyword":"Error Information LID 01h mandatory log page","mandatory":"M"},
    {"id":"REQ-MON-ERR-002","level1":"ERR Error Information","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.2","spec_section":"§5.1.12.1.2",
     "spec_text":"If the error is not specific to a particular command, then the SQID, CID, and Parameter Error Location fields shall be set to FFFFh. The Log Page Version field shall be set to 1h.",
     "spec_text_ko":"오류가 특정 명령에 한정되지 않는 경우, SQID, CID 및 Parameter Error Location 필드는 FFFFh로 설정되어야 한다. Log Page Version 필드는 1h로 설정되어야 한다.",
     "keyword":"Error Information SQID CID FFFFh Version 1h","mandatory":"M"},

    # === TLM Telemetry ===
    {"id":"REQ-MON-TLM-001","level1":"TLM Telemetry","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.8","spec_section":"§5.1.12.1.8",
     "spec_text":"The Telemetry Host-Initiated log page (LID 07h) header shall always be available even if there is no Telemetry Host-Initiated Data available.",
     "spec_text_ko":"Telemetry Host-Initiated 로그 페이지(LID 07h) 헤더는 Telemetry Host-Initiated Data가 없더라도 항상 사용 가능해야 한다.",
     "keyword":"Telemetry Host-Initiated LID 07h header available","mandatory":"O"},
    {"id":"REQ-MON-TLM-002","level1":"TLM Telemetry","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.8","spec_section":"§5.1.12.1.8",
     "spec_text":"If the Create Telemetry Host-Initiated Data bit is set to '1' in the Get Log Page command, the controller shall capture the internal state at the time the command is processed.",
     "spec_text_ko":"Get Log Page 명령에서 Create Telemetry Host-Initiated Data 비트가 '1'로 설정된 경우, 컨트롤러는 명령 처리 시점의 내부 상태를 캡처해야 한다.",
     "keyword":"Telemetry Create Host-Initiated capture internal state","mandatory":"O"},
    {"id":"REQ-MON-TLM-003","level1":"TLM Telemetry","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.9","spec_section":"§5.1.12.1.9",
     "spec_text":"The Telemetry Controller-Initiated Data for Data Area 1 through Data Area 3 shall persist across all resets. If the host specifies a Log Page Offset Lower value that is not a multiple of 512 bytes, the controller shall return Invalid Field in Command.",
     "spec_text_ko":"Telemetry Controller-Initiated Data의 Data Area 1~3은 모든 리셋에 걸쳐 유지되어야 한다. 호스트가 512바이트의 배수가 아닌 Log Page Offset Lower 값을 지정하면, 컨트롤러는 Invalid Field in Command를 반환해야 한다.",
     "keyword":"Telemetry Controller-Initiated persist resets 512 alignment","mandatory":"O"},

    # === PEL Persistent Event Log ===
    {"id":"REQ-MON-PEL-001","level1":"PEL Persistent Event Log","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.14","spec_section":"§5.1.12.1.14",
     "spec_text":"The information in the Persistent Event Log page (LID 0Dh) shall be retained across power cycles and resets.",
     "spec_text_ko":"Persistent Event Log 페이지(LID 0Dh)의 정보는 전원 사이클 및 리셋에 걸쳐 유지되어야 한다.",
     "keyword":"Persistent Event Log LID 0Dh retain power cycle reset","mandatory":"O"},
    {"id":"REQ-MON-PEL-002","level1":"PEL Persistent Event Log","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.14","spec_section":"§5.1.12.1.14",
     "spec_text":"The controller shall log all supported events at each event occurrence unless the controller determines that the same event is occurring at a frequency that exceeds a vendor specific threshold.",
     "spec_text_ko":"컨트롤러는 동일 이벤트가 벤더 고유 임계값을 초과하는 빈도로 발생하는 것으로 판단하지 않는 한, 각 이벤트 발생 시 모든 지원 이벤트를 기록해야 한다.",
     "keyword":"PEL log all events vendor threshold suppress","mandatory":"O"},
    {"id":"REQ-MON-PEL-003","level1":"PEL Persistent Event Log","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.14","spec_section":"§5.1.12.1.14",
     "spec_text":"A Power-on or Reset event shall be recorded in the Persistent Event Log when an NVM Subsystem Reset or a Controller Level Reset is completed.",
     "spec_text_ko":"NVM Subsystem Reset 또는 Controller Level Reset이 완료되면 Persistent Event Log에 Power-on or Reset 이벤트가 기록되어야 한다.",
     "keyword":"PEL Power-on Reset event CLR NSSR","mandatory":"O"},

    # === DST Device Self-Test ===
    {"id":"REQ-MON-DST-001","level1":"DST Device Self-Test","level2":None,
     "derived_from":"NVMe 2.2 §5.1.5","spec_section":"§5.1.5",
     "spec_text":"The controller shall support the Device Self-test command if the OACS field in the Identify Controller data structure indicates support. The Device Self-test log page (LID 06h) shall report results of self-test operations.",
     "spec_text_ko":"Identify Controller 데이터 구조의 OACS 필드가 지원을 표시하면 컨트롤러는 Device Self-test 명령을 지원해야 한다. Device Self-test 로그 페이지(LID 06h)는 self-test 작업 결과를 보고해야 한다.",
     "keyword":"Device Self-test OACS LID 06h","mandatory":"O"},
    {"id":"REQ-MON-DST-002","level1":"DST Device Self-Test","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.7","spec_section":"§5.1.12.1.7",
     "spec_text":"If a device self-test operation is in process, the controller shall not set the Current Device Self-Test Operation field to 0h until a new Self-test Result Data Structure is created. Unused result entries shall have the Device Self-test Result field set to Fh.",
     "spec_text_ko":"장치 self-test 작업이 진행 중이면, 새 Self-test Result Data Structure가 생성될 때까지 컨트롤러는 Current Device Self-Test Operation 필드를 0h로 설정해서는 안 된다. 미사용 결과 항목은 Device Self-test Result 필드가 Fh로 설정되어야 한다.",
     "keyword":"DST in process Current Operation Fh unused","mandatory":"O"},

    # === CSE Commands Supported and Effects ===
    {"id":"REQ-MON-CSE-001","level1":"CSE Commands Supported and Effects","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.6","spec_section":"§5.1.12.1.6",
     "spec_text":"The controller shall support the Commands Supported and Effects log page (LID 05h) to describe the commands that the controller supports and the effects of those commands on the state of the NVM subsystem.",
     "spec_text_ko":"컨트롤러는 컨트롤러가 지원하는 명령과 해당 명령이 NVM 서브시스템 상태에 미치는 영향을 설명하는 Commands Supported and Effects 로그 페이지(LID 05h)를 지원해야 한다.",
     "keyword":"CSE Commands Supported Effects LID 05h","mandatory":"M"},

    # === FIE Feature Identifiers Supported ===
    {"id":"REQ-MON-FIE-001","level1":"FIE Feature Identifiers Supported","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.18","spec_section":"§5.1.12.1.18",
     "spec_text":"If the Feature Identifiers Supported and Effects log page (LID 12h) is supported and the Feature is supported, the scope shall be indicated in the FID Scope field (FSP) for that Feature.",
     "spec_text_ko":"Feature Identifiers Supported and Effects 로그 페이지(LID 12h)가 지원되고 Feature가 지원되는 경우, 해당 Feature의 FID Scope 필드(FSP)에 범위가 표시되어야 한다.",
     "keyword":"FIE Feature Identifiers Supported Effects LID 12h FSP","mandatory":"O"},

    # === TSP Timestamp ===
    {"id":"REQ-MON-TSP-001","level1":"TSP Timestamp","level2":None,
     "derived_from":"NVMe 2.2 §5.1.25.1.7","spec_section":"§5.1.25.1.7",
     "spec_text":"The Timestamp feature (Feature 0Eh) shall allow the host to set and get the controller's timestamp. If the controller maintains the timestamp across Controller Level Reset, it shall also preserve the Timestamp Origin field across that reset.",
     "spec_text_ko":"Timestamp 기능(Feature 0Eh)은 호스트가 컨트롤러의 타임스탬프를 설정하고 가져올 수 있어야 한다. 컨트롤러가 Controller Level Reset에 걸쳐 타임스탬프를 유지하면, 해당 리셋에 걸쳐 Timestamp Origin 필드도 보존해야 한다.",
     "keyword":"Timestamp Feature 0Eh CLR Origin preserve","mandatory":"O"},

    # === EGL Endurance Group Log ===
    {"id":"REQ-MON-EGL-001","level1":"EGL Endurance Group Log","level2":None,
     "derived_from":"NVMe 2.2 §5.1.12.1.10","spec_section":"§5.1.12.1.10",
     "spec_text":"The Endurance Group Information log page (LID 09h) shall report critical warnings for each Endurance Group. If a critical warning bit is set to '1' in all Endurance Groups, the corresponding bit shall be set to '1' in the SMART / Health Information log page.",
     "spec_text_ko":"Endurance Group Information 로그 페이지(LID 09h)는 각 Endurance Group의 critical warnings를 보고해야 한다. 모든 Endurance Group에서 critical warning 비트가 '1'로 설정되면, SMART / Health Information 로그 페이지에서 해당 비트도 '1'로 설정되어야 한다.",
     "keyword":"EGL Endurance Group Information LID 09h Critical Warning SMART","mandatory":"O"},
]

for r in reqs:
    r.setdefault("category","MONITOR")
    r.setdefault("controller_type","BOTH")
    c.execute("""INSERT OR IGNORE INTO requirement
        (id,category,level1,level2,derived_from,spec_section,spec_text,spec_text_ko,
         keyword,controller_type,mandatory,support_status,status,priority,created_at,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (r["id"],r["category"],r["level1"],r["level2"],r["derived_from"],r["spec_section"],
         r["spec_text"],r["spec_text_ko"],r["keyword"],r["controller_type"],r["mandatory"],
         "UNKNOWN","OPEN","NORMAL",now,now))
    print(f"  ADD: {r['id']}")
c.commit(); c.close()
print(f"\nImported {len(reqs)} MONITOR requirements.")
