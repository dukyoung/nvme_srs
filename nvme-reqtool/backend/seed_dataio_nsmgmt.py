"""Insert DATA_IO and NS_MGMT requirements into DB."""
import sqlite3, datetime
now = datetime.datetime.now(datetime.UTC).isoformat()
c = sqlite3.connect("nvme_req.db")

reqs = [
    # === DATA_IO / FLS Flush ===
    {"id":"REQ-DIO-FLS-001","category":"DATA_IO","level1":"FLS Flush","level2":None,
     "derived_from":"NVMe 2.2 §7.2","spec_section":"§7.2",
     "spec_text":"If a volatile write cache is enabled, then the Flush command shall commit data and metadata associated with the specified namespace(s) to non-volatile storage media.",
     "spec_text_ko":"휘발성 쓰기 캐시가 활성화된 경우, Flush 명령은 지정된 네임스페이스와 관련된 데이터 및 메타데이터를 비휘발성 저장 매체에 커밋해야 한다.",
     "keyword":"Flush commit volatile write cache non-volatile","mandatory":"M"},
    {"id":"REQ-DIO-FLS-002","category":"DATA_IO","level1":"FLS Flush","level2":None,
     "derived_from":"NVMe 2.2 §7.2","spec_section":"§7.2",
     "spec_text":"If the Flush Behavior (FB) field is set to 11b and the specified NSID is FFFFFFFFh, then the Flush command shall apply to all namespaces attached to the controller.",
     "spec_text_ko":"FB 필드가 11b로 설정되고 NSID가 FFFFFFFFh인 경우, Flush 명령은 컨트롤러에 부착된 모든 네임스페이스에 적용되어야 한다.",
     "keyword":"Flush FB 11b FFFFFFFFh all namespaces","mandatory":"M"},
    {"id":"REQ-DIO-FLS-003","category":"DATA_IO","level1":"FLS Flush","level2":None,
     "derived_from":"NVMe 2.2 §7.2","spec_section":"§7.2",
     "spec_text":"If the FB field is set to 10b and the specified NSID is FFFFFFFFh, then the controller shall abort the command with a status code of Invalid Namespace or Format.",
     "spec_text_ko":"FB 필드가 10b로 설정되고 NSID가 FFFFFFFFh인 경우, 컨트롤러는 Invalid Namespace or Format 상태 코드로 명령을 중단해야 한다.",
     "keyword":"Flush FB 10b FFFFFFFFh abort Invalid Namespace","mandatory":"M"},
    {"id":"REQ-DIO-FLS-004","category":"DATA_IO","level1":"FLS Flush","level2":None,
     "derived_from":"NVMe 2.2 §7.2","spec_section":"§7.2",
     "spec_text":"If a volatile write cache is not present or not enabled, then Flush commands shall have no effect and shall complete successfully if a sanitize operation is not in progress.",
     "spec_text_ko":"휘발성 쓰기 캐시가 존재하지 않거나 활성화되지 않은 경우, Flush 명령은 효과가 없어야 하며, sanitize 작업이 진행 중이 아니면 성공적으로 완료되어야 한다.",
     "keyword":"Flush no cache no effect complete successfully","mandatory":"M"},

    # === NS_MGMT / NSM Namespace Management ===
    {"id":"REQ-NS-NSM-001","category":"NS_MGMT","level1":"NSM Namespace Management","level2":None,
     "derived_from":"NVMe 2.2 §8.1.14","spec_section":"§8.1.14",
     "spec_text":"If the Namespace Management capability is supported, the controller shall support the Namespace Management command and the Namespace Attachment command, set the NMS bit to '1' in OACS, and support the Attached Namespace Attribute Changed asynchronous event.",
     "spec_text_ko":"Namespace Management 기능이 지원되는 경우, 컨트롤러는 Namespace Management 명령과 Namespace Attachment 명령을 지원하고, OACS에서 NMS 비트를 '1'로 설정하며, Attached Namespace Attribute Changed 비동기 이벤트를 지원해야 한다.",
     "keyword":"NSM NMS OACS Namespace Management Attachment","mandatory":"O"},
    {"id":"REQ-NS-NSM-002","category":"NS_MGMT","level1":"NSM Namespace Management","level2":None,
     "derived_from":"NVMe 2.2 §5.1.21","spec_section":"§5.1.21",
     "spec_text":"For the Create operation, the controller shall select an available Namespace Identifier to use for the operation.",
     "spec_text_ko":"Create 작업의 경우, 컨트롤러는 작업에 사용할 사용 가능한 Namespace Identifier를 선택해야 한다.",
     "keyword":"NSM Create NSID select available","mandatory":"M"},
    {"id":"REQ-NS-NSM-003","category":"NS_MGMT","level1":"NSM Namespace Management","level2":None,
     "derived_from":"NVMe 2.2 §8.1.14","spec_section":"§8.1.14",
     "spec_text":"If both NVM Set Identifier and Endurance Group Identifier are cleared to 0h in a create operation, the controller shall choose the Endurance Group and the NVM Set from which to allocate capacity.",
     "spec_text_ko":"Create 작업에서 NVM Set Identifier와 Endurance Group Identifier가 모두 0h로 클리어된 경우, 컨트롤러는 용량을 할당할 Endurance Group과 NVM Set을 선택해야 한다.",
     "keyword":"NSM Create NVMSETID ENDGID 0h choose","mandatory":"M"},
    {"id":"REQ-NS-NSM-004","category":"NS_MGMT","level1":"NSM Namespace Management","level2":None,
     "derived_from":"NVMe 2.2 §8.1.14","spec_section":"§8.1.14",
     "spec_text":"If NVM Set Identifier is non-zero and Endurance Group Identifier is cleared to 0h in a create operation, the controller shall abort the command with a status code of Invalid Field in Command.",
     "spec_text_ko":"Create 작업에서 NVM Set Identifier가 0이 아니고 Endurance Group Identifier가 0h로 클리어된 경우, 컨트롤러는 Invalid Field in Command 상태 코드로 명령을 중단해야 한다.",
     "keyword":"NSM Create NVMSETID nonzero ENDGID 0h abort","mandatory":"M"},

    # === NS_MGMT / NSA Namespace Attachment ===
    {"id":"REQ-NS-NSA-001","category":"NS_MGMT","level1":"NSA Namespace Attachment","level2":None,
     "derived_from":"NVMe 2.2 §5.1.20","spec_section":"§5.1.20",
     "spec_text":"If MAXDNA is non-zero and attaching the namespace causes the sum of attached namespaces across all I/O controllers in the Domain to exceed MAXDNA, the controller shall abort the command with Namespace Attachment Limit Exceeded.",
     "spec_text_ko":"MAXDNA가 0이 아니고 네임스페이스 부착으로 도메인 내 모든 I/O 컨트롤러의 부착된 네임스페이스 합계가 MAXDNA를 초과하면, 컨트롤러는 Namespace Attachment Limit Exceeded로 명령을 중단해야 한다.",
     "keyword":"NSA MAXDNA Attachment Limit Exceeded","mandatory":"M"},
    {"id":"REQ-NS-NSA-002","category":"NS_MGMT","level1":"NSA Namespace Attachment","level2":None,
     "derived_from":"NVMe 2.2 §5.1.20","spec_section":"§5.1.20",
     "spec_text":"If an attempt is made to attach a namespace to a controller that does not support the corresponding I/O Command Set, then the command shall be aborted with a status code of I/O Command Set Not Supported.",
     "spec_text_ko":"해당 I/O Command Set을 지원하지 않는 컨트롤러에 네임스페이스를 부착하려고 시도하면, I/O Command Set Not Supported 상태 코드로 명령이 중단되어야 한다.",
     "keyword":"NSA I/O Command Set Not Supported abort","mandatory":"M"},

    # === NS_MGMT / FMT Format NVM ===
    {"id":"REQ-NS-FMT-001","category":"NS_MGMT","level1":"FMT Format NVM","level2":None,
     "derived_from":"NVMe 2.2 §5.1.10","spec_section":"§5.1.10",
     "spec_text":"After the Format NVM command successfully completes, the controller shall not return any user data that was previously contained in an affected namespace.",
     "spec_text_ko":"Format NVM 명령이 성공적으로 완료된 후, 컨트롤러는 영향받은 네임스페이스에 이전에 포함된 사용자 데이터를 반환해서는 안 된다.",
     "keyword":"Format NVM no previous user data","mandatory":"M"},
    {"id":"REQ-NS-FMT-002","category":"NS_MGMT","level1":"FMT Format NVM","level2":None,
     "derived_from":"NVMe 2.2 §5.1.10","spec_section":"§5.1.10",
     "spec_text":"If there are I/O commands being processed for a namespace, a Format NVM command affecting that namespace may be aborted with a status code of Command Sequence Error.",
     "spec_text_ko":"네임스페이스에 대해 I/O 명령이 처리 중인 경우, 해당 네임스페이스에 영향을 미치는 Format NVM 명령은 Command Sequence Error 상태 코드로 중단될 수 있다.",
     "keyword":"Format NVM I/O commands Command Sequence Error","mandatory":"M"},
    {"id":"REQ-NS-FMT-003","category":"NS_MGMT","level1":"FMT Format NVM","level2":None,
     "derived_from":"NVMe 2.2 §5.1.10","spec_section":"§5.1.10",
     "spec_text":"If a Format NVM command is in progress, an I/O command for any affected namespace may be aborted with a status code of Format in Progress.",
     "spec_text_ko":"Format NVM 명령이 진행 중인 경우, 영향받는 네임스페이스에 대한 I/O 명령은 Format in Progress 상태 코드로 중단될 수 있다.",
     "keyword":"Format NVM in progress I/O abort","mandatory":"M"},
    {"id":"REQ-NS-FMT-004","category":"NS_MGMT","level1":"FMT Format NVM","level2":None,
     "derived_from":"NVMe 2.2 §5.1.10","spec_section":"§5.1.10",
     "spec_text":"If the format operation scope includes any namespace that is write protected, the controller shall abort the Format NVM command with a status code of Namespace is Write Protected.",
     "spec_text_ko":"포맷 작업 범위에 쓰기 보호된 네임스페이스가 포함된 경우, 컨트롤러는 Namespace is Write Protected 상태 코드로 Format NVM 명령을 중단해야 한다.",
     "keyword":"Format NVM write protected abort","mandatory":"M"},
    {"id":"REQ-NS-FMT-005","category":"NS_MGMT","level1":"FMT Format NVM","level2":None,
     "derived_from":"NVMe 2.2 §5.1.10","spec_section":"§5.1.10",
     "spec_text":"If an unsupported User Data Format is selected, the controller shall abort the command with a status code of Invalid Format.",
     "spec_text_ko":"지원되지 않는 User Data Format이 선택된 경우, 컨트롤러는 Invalid Format 상태 코드로 명령을 중단해야 한다.",
     "keyword":"Format NVM unsupported Invalid Format abort","mandatory":"M"},

    # === NS_MGMT / WPR Namespace Write Protection ===
    {"id":"REQ-NS-WPR-001","category":"NS_MGMT","level1":"WPR Namespace Write Protection","level2":None,
     "derived_from":"NVMe 2.2 §8.1.15","spec_section":"§8.1.15",
     "spec_text":"If Namespace Write Protection is supported, the controller shall indicate the level of support in the NWPC field of Identify Controller and support the Namespace Write Protection Config feature (Feature 84h).",
     "spec_text_ko":"Namespace Write Protection이 지원되는 경우, 컨트롤러는 Identify Controller의 NWPC 필드에 지원 수준을 표시하고 Namespace Write Protection Config 기능(Feature 84h)을 지원해야 한다.",
     "keyword":"WPR NWPC Identify Controller Feature 84h","mandatory":"O"},
    {"id":"REQ-NS-WPR-002","category":"NS_MGMT","level1":"WPR Namespace Write Protection","level2":None,
     "derived_from":"NVMe 2.2 §8.1.15","spec_section":"§8.1.15",
     "spec_text":"If any controller in the NVM subsystem supports Namespace Write Protection, then the write protection state of a namespace shall be enforced by any controller to which that namespace is attached.",
     "spec_text_ko":"NVM 서브시스템의 컨트롤러가 Namespace Write Protection을 지원하는 경우, 네임스페이스의 쓰기 보호 상태는 해당 네임스페이스가 부착된 모든 컨트롤러에 의해 강제되어야 한다.",
     "keyword":"WPR multi-controller enforcement","mandatory":"M"},
    {"id":"REQ-NS-WPR-003","category":"NS_MGMT","level1":"WPR Namespace Write Protection","level2":None,
     "derived_from":"NVMe 2.2 §8.1.15","spec_section":"§8.1.15",
     "spec_text":"Commands that specify an NSID for a write protected namespace and would modify it shall be aborted with a status code of Namespace Is Write Protected.",
     "spec_text_ko":"쓰기 보호된 네임스페이스의 NSID를 지정하고 이를 수정하려는 명령은 Namespace Is Write Protected 상태 코드로 중단되어야 한다.",
     "keyword":"WPR Namespace Is Write Protected abort","mandatory":"M"},
    {"id":"REQ-NS-WPR-004","category":"NS_MGMT","level1":"WPR Namespace Write Protection","level2":None,
     "derived_from":"NVMe 2.2 §5.1.25.1.31","spec_section":"§5.1.25.1.31",
     "spec_text":"If a Set Features command changes the namespace to a write protected state, the controller shall commit all volatile write cache data and metadata associated with the specified namespace to non-volatile storage media as part of transitioning to the write protected state.",
     "spec_text_ko":"Set Features 명령이 네임스페이스를 쓰기 보호 상태로 변경하면, 컨트롤러는 쓰기 보호 상태로 전환하는 과정에서 지정된 네임스페이스와 관련된 모든 휘발성 쓰기 캐시 데이터 및 메타데이터를 비휘발성 저장 매체에 커밋해야 한다.",
     "keyword":"WPR write cache flush state transition","mandatory":"M"},
    {"id":"REQ-NS-WPR-005","category":"NS_MGMT","level1":"WPR Namespace Write Protection","level2":None,
     "derived_from":"NVMe 2.2 §5.1.25.1.31","spec_section":"§5.1.25.1.31",
     "spec_text":"If a Set Features command attempts to change the write protection state of a namespace in the Write Protect Until Power Cycle state or Permanent Write Protect state, the controller shall abort the command with Feature Not Changeable.",
     "spec_text_ko":"Write Protect Until Power Cycle 또는 Permanent Write Protect 상태의 네임스페이스에 대해 쓰기 보호 상태 변경을 시도하는 Set Features 명령이 있으면, 컨트롤러는 Feature Not Changeable로 명령을 중단해야 한다.",
     "keyword":"WPR Feature Not Changeable Permanent Write Protect","mandatory":"M"},
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
print(f"\nImported {len(reqs)} DATA_IO + NS_MGMT requirements.")
