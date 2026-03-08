"""Insert SECURITY (SEC, LCK) and INTEGRITY (MUS, EGR, VWC, RRL) requirements."""
import sqlite3, datetime
now = datetime.datetime.now(datetime.UTC).isoformat()
c = sqlite3.connect("nvme_req.db")

reqs = [
    # === SECURITY / SEC Security Send/Receive ===
    {"id":"REQ-SEC-SEC-001","category":"SECURITY","level1":"SEC Security Send/Receive","level2":None,
     "derived_from":"NVMe 2.2 §5.1.23","spec_section":"§5.1.23",
     "spec_text":"The controller shall support the Security Receive command. A Security Receive command with the Security Protocol field cleared to 00h shall return information about the security protocols supported by the controller.",
     "spec_text_ko":"컨트롤러는 Security Receive 명령을 지원해야 한다. Security Protocol 필드가 00h로 클리어된 Security Receive 명령은 컨트롤러가 지원하는 보안 프로토콜에 대한 정보를 반환해야 한다.",
     "keyword":"Security Receive Protocol 00h supported protocols","mandatory":"O"},
    {"id":"REQ-SEC-SEC-002","category":"SECURITY","level1":"SEC Security Send/Receive","level2":None,
     "derived_from":"NVMe 2.2 §5.1.23","spec_section":"§5.1.23",
     "spec_text":"The controller shall abort the Security Receive command with a status code of Invalid Field in Command if an unsupported value of the Security Protocol is specified.",
     "spec_text_ko":"지원되지 않는 Security Protocol 값이 지정된 경우, 컨트롤러는 Invalid Field in Command 상태 코드로 Security Receive 명령을 중단해야 한다.",
     "keyword":"Security Receive unsupported protocol abort","mandatory":"M"},
    {"id":"REQ-SEC-SEC-003","category":"SECURITY","level1":"SEC Security Send/Receive","level2":None,
     "derived_from":"NVMe 2.2 §5.1.24","spec_section":"§5.1.24",
     "spec_text":"The controller shall support the Security Send command. The controller shall abort the command with Invalid Field in Command if a reserved value of the Security Protocol is specified.",
     "spec_text_ko":"컨트롤러는 Security Send 명령을 지원해야 한다. 예약된 Security Protocol 값이 지정된 경우, 컨트롤러는 Invalid Field in Command로 명령을 중단해야 한다.",
     "keyword":"Security Send reserved protocol abort","mandatory":"O"},

    # === SECURITY / LCK Lockdown ===
    {"id":"REQ-SEC-LCK-001","category":"SECURITY","level1":"LCK Lockdown","level2":None,
     "derived_from":"NVMe 2.2 §5.1.15","spec_section":"§5.1.15",
     "spec_text":"If the Command and Feature Lockdown capability is supported (CFLS bit in OACS is '1'), the controller shall support the Lockdown command and the Command and Feature Lockdown log page (LID 14h).",
     "spec_text_ko":"Command and Feature Lockdown 기능이 지원되는 경우(OACS의 CFLS 비트가 '1'), 컨트롤러는 Lockdown 명령과 Command and Feature Lockdown 로그 페이지(LID 14h)를 지원해야 한다.",
     "keyword":"Lockdown CFLS OACS LID 14h","mandatory":"O"},
    {"id":"REQ-SEC-LCK-002","category":"SECURITY","level1":"LCK Lockdown","level2":None,
     "derived_from":"NVMe 2.2 §8.1.5","spec_section":"§8.1.5",
     "spec_text":"The prohibiting of execution of a command as part of Lockdown shall persist until a power cycle of the NVM subsystem or further being allowed by a follow-on Lockdown command.",
     "spec_text_ko":"Lockdown의 일부로서 명령 실행 금지는 NVM 서브시스템의 전원 사이클 또는 후속 Lockdown 명령에 의한 허용까지 유지되어야 한다.",
     "keyword":"Lockdown persist power cycle follow-on","mandatory":"M"},
    {"id":"REQ-SEC-LCK-003","category":"SECURITY","level1":"LCK Lockdown","level2":None,
     "derived_from":"NVMe 2.2 §8.1.5","spec_section":"§8.1.5",
     "spec_text":"If a prohibited Admin Command Set command or Feature Identifier is processed by a controller, it shall be aborted with a status code of Command Prohibited by Command and Feature Lockdown.",
     "spec_text_ko":"금지된 Admin Command Set 명령 또는 Feature Identifier가 컨트롤러에 의해 처리되면, Command Prohibited by Command and Feature Lockdown 상태 코드로 중단되어야 한다.",
     "keyword":"Lockdown prohibited command abort","mandatory":"M"},
    {"id":"REQ-SEC-LCK-004","category":"SECURITY","level1":"LCK Lockdown","level2":None,
     "derived_from":"NVMe 2.2 §5.1.15","spec_section":"§5.1.15",
     "spec_text":"If the Lockdown command specifies a command opcode or Feature Identifier that is not supported as being prohibitable, it shall be aborted with Prohibition of Command Execution Not Supported.",
     "spec_text_ko":"Lockdown 명령이 금지 가능으로 지원되지 않는 명령 opcode 또는 Feature Identifier를 지정하면, Prohibition of Command Execution Not Supported로 중단되어야 한다.",
     "keyword":"Lockdown unsupported prohibitable abort","mandatory":"M"},

    # === INTEGRITY / MUS Media Unit Status ===
    {"id":"REQ-INT-MUS-001","category":"INTEGRITY","level1":"MUS Media Unit Status","level2":None,
     "derived_from":"NVMe 2.2 §8.1.12","spec_section":"§8.1.12",
     "spec_text":"A controller supporting Fixed Capacity Management shall support the Media Unit Status log page (LID 10h).",
     "spec_text_ko":"Fixed Capacity Management를 지원하는 컨트롤러는 Media Unit Status 로그 페이지(LID 10h)를 지원해야 한다.",
     "keyword":"MUS Media Unit Status LID 10h Fixed Capacity","mandatory":"O"},

    # === INTEGRITY / EGR Endurance Group ===
    {"id":"REQ-INT-EGR-001","category":"INTEGRITY","level1":"EGR Endurance Group","level2":None,
     "derived_from":"NVMe 2.2 §5.1.25.1.16","spec_section":"§5.1.25.1.16",
     "spec_text":"The Endurance Group Event Configuration feature (Feature 18h) shall allow configuration of critical warning events per Endurance Group. If a reserved bit is set in the Endurance Group Critical Warnings field, the Set Features command shall be aborted with Invalid Field in Command.",
     "spec_text_ko":"Endurance Group Event Configuration 기능(Feature 18h)은 Endurance Group별 critical warning 이벤트 구성을 허용해야 한다. Endurance Group Critical Warnings 필드에 예약 비트가 설정되면, Set Features 명령은 Invalid Field in Command로 중단되어야 한다.",
     "keyword":"EGR Event Configuration Feature 18h Critical Warnings","mandatory":"O"},
    {"id":"REQ-INT-EGR-002","category":"INTEGRITY","level1":"EGR Endurance Group","level2":None,
     "derived_from":"NVMe 2.2 §5.1.25.1.16","spec_section":"§5.1.25.1.16",
     "spec_text":"If the Endurance Group Identifier specifies an Endurance Group that does not exist, the Set Features or Get Features command shall be aborted with Invalid Field in Command.",
     "spec_text_ko":"Endurance Group Identifier가 존재하지 않는 Endurance Group을 지정하면, Set Features 또는 Get Features 명령은 Invalid Field in Command로 중단되어야 한다.",
     "keyword":"EGR Identifier nonexistent abort Invalid Field","mandatory":"M"},

    # === INTEGRITY / VWC Volatile Write Cache ===
    {"id":"REQ-INT-VWC-001","category":"INTEGRITY","level1":"VWC Volatile Write Cache","level2":None,
     "derived_from":"NVMe 2.2 §5.1.25.1.4","spec_section":"§5.1.25.1.4",
     "spec_text":"If a volatile write cache is present (VWC field in Identify Controller), then the Volatile Write Cache feature (Feature 06h) shall be supported.",
     "spec_text_ko":"휘발성 쓰기 캐시가 존재하는 경우(Identify Controller의 VWC 필드), Volatile Write Cache 기능(Feature 06h)이 지원되어야 한다.",
     "keyword":"VWC Volatile Write Cache Feature 06h","mandatory":"M"},
    {"id":"REQ-INT-VWC-002","category":"INTEGRITY","level1":"VWC Volatile Write Cache","level2":None,
     "derived_from":"NVMe 2.2 §5.1.25.1.4","spec_section":"§5.1.25.1.4",
     "spec_text":"If a volatile write cache is not present, a Set Features or Get Features command specifying the Volatile Write Cache feature shall abort with Invalid Field in Command.",
     "spec_text_ko":"휘발성 쓰기 캐시가 존재하지 않는 경우, Volatile Write Cache 기능을 지정하는 Set Features 또는 Get Features 명령은 Invalid Field in Command로 중단되어야 한다.",
     "keyword":"VWC not present Set Get Features abort","mandatory":"M"},
    {"id":"REQ-INT-VWC-003","category":"INTEGRITY","level1":"VWC Volatile Write Cache","level2":None,
     "derived_from":"NVMe 2.2 §5.1.25.1.4","spec_section":"§5.1.25.1.4",
     "spec_text":"If a volatile write cache is present and disabled (WCE bit cleared to '0'), then user data written by any command shall be persistent.",
     "spec_text_ko":"휘발성 쓰기 캐시가 존재하고 비활성화된 경우(WCE 비트가 '0'으로 클리어), 모든 명령에 의해 기록된 사용자 데이터는 영구적이어야 한다.",
     "keyword":"VWC disabled WCE persistent data","mandatory":"M"},

    # === INTEGRITY / RRL Read Recovery Level ===
    {"id":"REQ-INT-RRL-001","category":"INTEGRITY","level1":"RRL Read Recovery Level","level2":None,
     "derived_from":"NVMe 2.2 §5.1.25.1.11","spec_section":"§5.1.25.1.11",
     "spec_text":"The Read Recovery Level Config feature (Feature 12h) is used to configure the Read Recovery Level. Modifying the Read Recovery Level shall have no effect on the data contained in any associated namespace.",
     "spec_text_ko":"Read Recovery Level Config 기능(Feature 12h)은 Read Recovery Level을 구성하는 데 사용된다. Read Recovery Level 수정은 관련 네임스페이스에 포함된 데이터에 영향을 미치지 않아야 한다.",
     "keyword":"RRL Read Recovery Level Feature 12h no effect data","mandatory":"O"},
]

for r in reqs:
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
print(f"\nImported {len(reqs)} SECURITY + INTEGRITY requirements.")
