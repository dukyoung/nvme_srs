"""Insert all remaining requirements: DATA_IO, NS_MGMT, MONITOR, SECURITY(SEC/LCK),
   INTEGRITY, FW_MGMT(BP), VIRT(HMB), RESET(SDN/PCIE/LCM) into DB."""
import sqlite3
import datetime

now = datetime.datetime.now(datetime.UTC).isoformat()
c = sqlite3.connect("nvme_req.db")

reqs = [
    # =============================================
    # DATA_IO - Flush
    # =============================================
    {
        "id": "REQ-DIO-FLS-001", "category": "DATA_IO",
        "level1": "FLS Flush", "level2": None,
        "derived_from": "NVMe 2.2 §7.2", "spec_section": "§7.2",
        "spec_text": "If a volatile write cache is enabled, then the Flush command shall commit data and metadata associated with the specified namespace(s) to non-volatile storage media.",
        "spec_text_ko": "휘발성 쓰기 캐시가 활성화된 경우, Flush 명령은 지정된 네임스페이스와 관련된 데이터 및 메타데이터를 비휘발성 저장 미디어에 커밋해야 한다.",
        "keyword": "Flush commit volatile write cache non-volatile",
        "mandatory": "M",
    },
    {
        "id": "REQ-DIO-FLS-002", "category": "DATA_IO",
        "level1": "FLS Flush", "level2": None,
        "derived_from": "NVMe 2.2 §7.2", "spec_section": "§7.2",
        "spec_text": "If the Flush Behavior (FB) field is set to 11b and NSID is FFFFFFFFh, then the Flush command shall apply to all namespaces attached to the controller. If FB is set to 10b and NSID is FFFFFFFFh, the controller shall abort with Invalid Namespace or Format.",
        "spec_text_ko": "FB 필드가 11b이고 NSID가 FFFFFFFFh인 경우, Flush 명령은 컨트롤러에 부착된 모든 네임스페이스에 적용되어야 한다. FB가 10b이고 NSID가 FFFFFFFFh인 경우 Invalid Namespace or Format으로 중단해야 한다.",
        "keyword": "Flush FB field FFFFFFFFh all namespaces",
        "mandatory": "M",
    },
    {
        "id": "REQ-DIO-FLS-003", "category": "DATA_IO",
        "level1": "FLS Flush", "level2": None,
        "derived_from": "NVMe 2.2 §7.2", "spec_section": "§7.2",
        "spec_text": "If a volatile write cache is not present or not enabled, then Flush commands shall have no effect and shall complete successfully if a sanitize operation is not in progress.",
        "spec_text_ko": "휘발성 쓰기 캐시가 없거나 활성화되지 않은 경우, Flush 명령은 효과가 없어야 하며 sanitize 작업이 진행 중이지 않으면 성공적으로 완료되어야 한다.",
        "keyword": "Flush no cache no effect complete successfully",
        "mandatory": "M",
    },

    # =============================================
    # NS_MGMT - Namespace Management
    # =============================================
    {
        "id": "REQ-NS-NSM-001", "category": "NS_MGMT",
        "level1": "NSM Namespace Management", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.21", "spec_section": "§5.1.21",
        "spec_text": "If the Namespace Management command is supported, then the Namespace Attachment command shall also be supported. The controller shall set the NMS bit to '1' in the OACS field and support the Attached Namespace Attribute Changed asynchronous event.",
        "spec_text_ko": "Namespace Management 명령이 지원되는 경우, Namespace Attachment 명령도 지원되어야 한다. 컨트롤러는 OACS 필드에 NMS 비트를 '1'로 설정하고 Attached Namespace Attribute Changed 비동기 이벤트를 지원해야 한다.",
        "keyword": "Namespace Management NMS OACS Attachment",
        "mandatory": "O",
    },
    {
        "id": "REQ-NS-NSM-002", "category": "NS_MGMT",
        "level1": "NSM Namespace Management", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.21", "spec_section": "§5.1.21",
        "spec_text": "For the Create operation, the controller shall select an available Namespace Identifier to use for the operation.",
        "spec_text_ko": "Create 작업의 경우, 컨트롤러는 작업에 사용할 수 있는 Namespace Identifier를 선택해야 한다.",
        "keyword": "Namespace Create NSID select available",
        "mandatory": "M",
    },
    {
        "id": "REQ-NS-NSM-003", "category": "NS_MGMT",
        "level1": "NSM Namespace Management", "level2": None,
        "derived_from": "NVMe 2.2 §8.1.14", "spec_section": "§8.1.14",
        "spec_text": "If both NVM Set Identifier and Endurance Group Identifier are cleared to 0h in a create operation, the controller shall choose the Endurance Group and NVM Set from which to allocate capacity. If NVM Set Identifier is non-zero and Endurance Group Identifier is 0h, the controller shall abort with Invalid Field in Command.",
        "spec_text_ko": "Create 작업에서 NVM Set Identifier와 Endurance Group Identifier가 모두 0h인 경우, 컨트롤러는 용량을 할당할 Endurance Group과 NVM Set을 선택해야 한다. NVM Set Identifier가 0이 아니고 Endurance Group Identifier가 0h인 경우 Invalid Field in Command로 중단해야 한다.",
        "keyword": "Namespace Create NVM Set Endurance Group selection",
        "mandatory": "M",
    },

    # === NSA Namespace Attachment ===
    {
        "id": "REQ-NS-NSA-001", "category": "NS_MGMT",
        "level1": "NSA Namespace Attachment", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.20", "spec_section": "§5.1.20",
        "spec_text": "If MAXDNA is non-zero and attaching a namespace causes the sum of attached namespaces across all I/O controllers in the Domain to exceed MAXDNA, the controller shall abort with Namespace Attachment Limit Exceeded.",
        "spec_text_ko": "MAXDNA가 0이 아니고 네임스페이스 부착 시 도메인 내 모든 I/O 컨트롤러의 부착된 네임스페이스 합계가 MAXDNA를 초과하면, 컨트롤러는 Namespace Attachment Limit Exceeded로 중단해야 한다.",
        "keyword": "Namespace Attachment MAXDNA limit exceeded",
        "mandatory": "M",
    },
    {
        "id": "REQ-NS-NSA-002", "category": "NS_MGMT",
        "level1": "NSA Namespace Attachment", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.20", "spec_section": "§5.1.20",
        "spec_text": "If an attempt is made to attach a namespace to a controller that does not support the corresponding I/O Command Set, then the command shall be aborted with I/O Command Set Not Supported. If the I/O Command Set is not enabled, the command shall be aborted with I/O Command Set Not Enabled.",
        "spec_text_ko": "해당 I/O Command Set을 지원하지 않는 컨트롤러에 네임스페이스 부착을 시도하면 I/O Command Set Not Supported로 중단되어야 한다. I/O Command Set이 활성화되지 않으면 I/O Command Set Not Enabled로 중단되어야 한다.",
        "keyword": "Namespace Attachment I/O Command Set validation",
        "mandatory": "M",
    },

    # === FMT Format NVM ===
    {
        "id": "REQ-NS-FMT-001", "category": "NS_MGMT",
        "level1": "FMT Format NVM", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.10", "spec_section": "§5.1.10",
        "spec_text": "After the Format NVM command successfully completes, the controller shall not return any user data that was previously contained in an affected namespace.",
        "spec_text_ko": "Format NVM 명령이 성공적으로 완료된 후, 컨트롤러는 영향을 받는 네임스페이스에 이전에 포함된 사용자 데이터를 반환해서는 안 된다.",
        "keyword": "Format NVM no previous user data",
        "mandatory": "M",
    },
    {
        "id": "REQ-NS-FMT-002", "category": "NS_MGMT",
        "level1": "FMT Format NVM", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.10", "spec_section": "§5.1.10",
        "spec_text": "If there are I/O commands being processed for a namespace, then a Format NVM command affecting that namespace may be aborted with Command Sequence Error. If a Format NVM command is in progress, I/O commands for affected namespaces may be aborted with Format in Progress.",
        "spec_text_ko": "네임스페이스에 대해 I/O 명령이 처리 중이면, 해당 네임스페이스에 영향을 미치는 Format NVM 명령은 Command Sequence Error로 중단될 수 있다. Format NVM 명령이 진행 중이면 영향을 받는 네임스페이스에 대한 I/O 명령은 Format in Progress로 중단될 수 있다.",
        "keyword": "Format NVM Command Sequence Error Format in Progress",
        "mandatory": "M",
    },
    {
        "id": "REQ-NS-FMT-003", "category": "NS_MGMT",
        "level1": "FMT Format NVM", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.10", "spec_section": "§5.1.10",
        "spec_text": "If the format operation scope includes any namespace that is write protected, the controller shall abort the Format NVM command with Namespace is Write Protected. If an unsupported User Data Format is selected, the controller shall abort with Invalid Format.",
        "spec_text_ko": "포맷 작업 범위에 쓰기 보호된 네임스페이스가 포함되면, 컨트롤러는 Namespace is Write Protected로 Format NVM 명령을 중단해야 한다. 지원되지 않는 User Data Format이 선택되면 Invalid Format으로 중단해야 한다.",
        "keyword": "Format NVM Write Protected Invalid Format",
        "mandatory": "M",
    },

    # === WPR Namespace Write Protection ===
    {
        "id": "REQ-NS-WPR-001", "category": "NS_MGMT",
        "level1": "WPR Namespace Write Protection", "level2": None,
        "derived_from": "NVMe 2.2 §8.1.15", "spec_section": "§8.1.15",
        "spec_text": "If Namespace Write Protection is supported, the controller shall indicate the level of support in the NWPC field: No Write Protect and Write Protect Support bit set to '1', and optionally Write Protect Until Power Cycle Support and Permanent Write Protect Support bits.",
        "spec_text_ko": "Namespace Write Protection이 지원되는 경우, 컨트롤러는 NWPC 필드에 지원 수준을 표시해야 한다: No Write Protect and Write Protect Support 비트를 '1'로 설정하고, 선택적으로 Write Protect Until Power Cycle Support 및 Permanent Write Protect Support 비트를 설정한다.",
        "keyword": "Namespace Write Protection NWPC capability",
        "mandatory": "O",
    },
    {
        "id": "REQ-NS-WPR-002", "category": "NS_MGMT",
        "level1": "WPR Namespace Write Protection", "level2": None,
        "derived_from": "NVMe 2.2 §8.1.15", "spec_section": "§8.1.15",
        "spec_text": "If any controller in the NVM subsystem supports Namespace Write Protection, then the write protection state of a namespace shall be enforced by any controller to which that namespace is attached.",
        "spec_text_ko": "NVM 서브시스템의 컨트롤러가 Namespace Write Protection을 지원하는 경우, 네임스페이스의 쓰기 보호 상태는 해당 네임스페이스가 부착된 모든 컨트롤러에 의해 적용되어야 한다.",
        "keyword": "Namespace Write Protection enforce all controllers",
        "mandatory": "M",
    },
    {
        "id": "REQ-NS-WPR-003", "category": "NS_MGMT",
        "level1": "WPR Namespace Write Protection", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.1.31", "spec_section": "§5.1.25.1.31",
        "spec_text": "If a Set Features command changes the namespace to a write protected state, then the controller shall commit all volatile write cache data and metadata associated with the specified namespace to non-volatile storage media as part of transitioning to the write protected state.",
        "spec_text_ko": "Set Features 명령이 네임스페이스를 쓰기 보호 상태로 변경하면, 컨트롤러는 쓰기 보호 상태 전환의 일부로 지정된 네임스페이스와 관련된 모든 휘발성 쓰기 캐시 데이터 및 메타데이터를 비휘발성 저장 미디어에 커밋해야 한다.",
        "keyword": "Write Protection flush cache state transition",
        "mandatory": "M",
    },

    # =============================================
    # MONITOR
    # =============================================
    # --- ERR Error Information ---
    {
        "id": "REQ-MON-ERR-001", "category": "MONITOR",
        "level1": "ERR Error Information", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.2", "spec_section": "§5.1.12.1.2",
        "spec_text": "The controller shall support the Error Information log page (LID 01h). If the error is not specific to a particular command, the SQID and CID fields shall be set to FFFFh.",
        "spec_text_ko": "컨트롤러는 Error Information 로그 페이지(LID 01h)를 지원해야 한다. 오류가 특정 명령과 관련이 없는 경우, SQID 및 CID 필드는 FFFFh로 설정되어야 한다.",
        "keyword": "Error Information LID 01h SQID CID FFFFh",
        "mandatory": "M",
    },

    # --- SMT SMART/Health ---
    {
        "id": "REQ-MON-SMT-001", "category": "MONITOR",
        "level1": "SMT SMART Health Information", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.3", "spec_section": "§5.1.12.1.3",
        "spec_text": "The controller shall support the SMART / Health Information log page (LID 02h). If a namespace ID other than 0h or FFFFFFFFh is specified, the controller shall abort with Invalid Field in Command.",
        "spec_text_ko": "컨트롤러는 SMART / Health Information 로그 페이지(LID 02h)를 지원해야 한다. 0h 또는 FFFFFFFFh 이외의 네임스페이스 ID가 지정되면 Invalid Field in Command로 중단해야 한다.",
        "keyword": "SMART Health LID 02h NSID validation",
        "mandatory": "M",
    },
    {
        "id": "REQ-MON-SMT-002", "category": "MONITOR",
        "level1": "SMT SMART Health Information", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.3", "spec_section": "§5.1.12.1.3",
        "spec_text": "The controller shall not set the All Media Read-Only bit to '1' in the Critical Warning field if the read-only condition is a result of a change in the write protection state of a namespace. The Percentage Used field shall be updated once per power-on hour.",
        "spec_text_ko": "컨트롤러는 읽기 전용 상태가 네임스페이스 쓰기 보호 상태 변경의 결과인 경우 Critical Warning 필드의 All Media Read-Only 비트를 '1'로 설정해서는 안 된다. Percentage Used 필드는 전원 가동 시간당 한 번 업데이트되어야 한다.",
        "keyword": "SMART Critical Warning Read-Only Percentage Used",
        "mandatory": "M",
    },

    # --- TLM Telemetry ---
    {
        "id": "REQ-MON-TLM-001", "category": "MONITOR",
        "level1": "TLM Telemetry", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.8", "spec_section": "§5.1.12.1.8",
        "spec_text": "The Telemetry Host-Initiated log page header shall always be available even if there is no data. The controller shall initiate a capture of internal state if it processes a Get Log Page command with the Create Telemetry Host-Initiated Data bit set to '1'.",
        "spec_text_ko": "Telemetry Host-Initiated 로그 페이지 헤더는 데이터가 없더라도 항상 사용 가능해야 한다. 컨트롤러는 Create Telemetry Host-Initiated Data 비트가 '1'로 설정된 Get Log Page 명령을 처리하면 내부 상태 캡처를 시작해야 한다.",
        "keyword": "Telemetry Host-Initiated LID 07h capture internal state",
        "mandatory": "O",
    },
    {
        "id": "REQ-MON-TLM-002", "category": "MONITOR",
        "level1": "TLM Telemetry", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.9", "spec_section": "§5.1.12.1.9",
        "spec_text": "The Telemetry Controller-Initiated Data for Data Area 1 through Data Area 3 shall persist across all resets. The controller shall return data for all blocks requested. If a data transfer is not a multiple of 512 bytes, the controller shall abort with Invalid Field in Command.",
        "spec_text_ko": "Telemetry Controller-Initiated Data Area 1~3의 데이터는 모든 리셋에 걸쳐 유지되어야 한다. 컨트롤러는 요청된 모든 블록의 데이터를 반환해야 한다. 데이터 전송이 512바이트의 배수가 아니면 Invalid Field in Command로 중단해야 한다.",
        "keyword": "Telemetry Controller-Initiated LID 08h persist resets 512 bytes",
        "mandatory": "O",
    },

    # --- DST Device Self-Test ---
    {
        "id": "REQ-MON-DST-001", "category": "MONITOR",
        "level1": "DST Device Self-Test", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.5", "spec_section": "§5.1.5",
        "spec_text": "If Device Self-Test is supported, the controller shall support the Device Self-test log page (LID 06h). Unused Self-test Result Data Structure fields shall have the Device Self-test Result field set to Fh and Self-test Code field cleared to 0h.",
        "spec_text_ko": "Device Self-Test가 지원되는 경우, 컨트롤러는 Device Self-test 로그 페이지(LID 06h)를 지원해야 한다. 사용되지 않는 Self-test Result Data Structure 필드는 Device Self-test Result 필드를 Fh로, Self-test Code 필드를 0h로 설정해야 한다.",
        "keyword": "Device Self-Test LID 06h Result Fh",
        "mandatory": "O",
    },
    {
        "id": "REQ-MON-DST-002", "category": "MONITOR",
        "level1": "DST Device Self-Test", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.7", "spec_section": "§5.1.12.1.7",
        "spec_text": "If a device self-test operation is in progress (Current Device Self-Test Operation field set to 1h or 2h), the controller shall not set this field to 0h until a new Self-test Result Data Structure is created.",
        "spec_text_ko": "장치 자가 테스트 작업이 진행 중인 경우(Current Device Self-Test Operation 필드가 1h 또는 2h), 컨트롤러는 새로운 Self-test Result Data Structure가 생성될 때까지 이 필드를 0h로 설정해서는 안 된다.",
        "keyword": "Device Self-Test in progress no clear until new result",
        "mandatory": "O",
    },

    # --- CSE Commands Supported and Effects ---
    {
        "id": "REQ-MON-CSE-001", "category": "MONITOR",
        "level1": "CSE Commands Supported and Effects", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.6", "spec_section": "§5.1.12.1.6",
        "spec_text": "The controller shall support the Commands Supported and Effects log page (LID 05h) to describe the commands the controller supports and the effects of those commands on the state of the NVM subsystem.",
        "spec_text_ko": "컨트롤러는 컨트롤러가 지원하는 명령과 해당 명령이 NVM 서브시스템 상태에 미치는 영향을 설명하는 Commands Supported and Effects 로그 페이지(LID 05h)를 지원해야 한다.",
        "keyword": "Commands Supported Effects LID 05h",
        "mandatory": "M",
    },

    # --- FIE Feature Identifiers Supported ---
    {
        "id": "REQ-MON-FIE-001", "category": "MONITOR",
        "level1": "FIE Feature Identifiers Supported", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.18", "spec_section": "§5.1.12.1.18",
        "spec_text": "If the Feature Identifiers Supported and Effects log page is supported and a Feature is supported, then the scope shall be indicated in the FID Scope field (FSP) for that Feature.",
        "spec_text_ko": "Feature Identifiers Supported and Effects 로그 페이지가 지원되고 Feature가 지원되는 경우, 해당 Feature의 FID Scope 필드(FSP)에 범위가 표시되어야 한다.",
        "keyword": "Feature Identifiers Supported LID 12h FSP scope",
        "mandatory": "M",
    },

    # --- TSP Timestamp ---
    {
        "id": "REQ-MON-TSP-001", "category": "MONITOR",
        "level1": "TSP Timestamp", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.1.7", "spec_section": "§5.1.25.1.7",
        "spec_text": "The Timestamp feature (Feature 0Eh) shall return the timestamp using the Timestamp data structure. If the controller maintains the timestamp value across Controller Level Reset, then the controller shall also preserve the Timestamp Origin field across that reset.",
        "spec_text_ko": "Timestamp 기능(Feature 0Eh)은 Timestamp 데이터 구조를 사용하여 타임스탬프를 반환해야 한다. 컨트롤러가 Controller Level Reset에 걸쳐 타임스탬프 값을 유지하면, 해당 리셋에 걸쳐 Timestamp Origin 필드도 보존해야 한다.",
        "keyword": "Timestamp Feature 0Eh Origin field preserve reset",
        "mandatory": "O",
    },

    # --- PEL Persistent Event Log ---
    {
        "id": "REQ-MON-PEL-001", "category": "MONITOR",
        "level1": "PEL Persistent Event Log", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.14", "spec_section": "§5.1.12.1.14",
        "spec_text": "The information in the Persistent Event log page (LID 0Dh) shall be retained across power cycles and resets. The controller shall log all supported events at each occurrence unless the frequency exceeds a vendor specific threshold.",
        "spec_text_ko": "Persistent Event 로그 페이지(LID 0Dh)의 정보는 전원 사이클 및 리셋에 걸쳐 유지되어야 한다. 컨트롤러는 빈도가 벤더 고유 임계값을 초과하지 않는 한 각 발생 시 지원되는 모든 이벤트를 기록해야 한다.",
        "keyword": "Persistent Event Log LID 0Dh retain power cycles",
        "mandatory": "O",
    },
    {
        "id": "REQ-MON-PEL-002", "category": "MONITOR",
        "level1": "PEL Persistent Event Log", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.14", "spec_section": "§5.1.12.1.14",
        "spec_text": "If the controller does not have a persistent event log reporting context, then the controller shall abort the Get Log Page command with Command Sequence Error. A Power-on or Reset event shall be recorded when an NVM Subsystem Reset or Controller Level Reset is completed.",
        "spec_text_ko": "컨트롤러에 persistent event log 보고 컨텍스트가 없으면 Get Log Page 명령을 Command Sequence Error로 중단해야 한다. Power-on 또는 Reset 이벤트는 NVM Subsystem Reset 또는 Controller Level Reset 완료 시 기록되어야 한다.",
        "keyword": "Persistent Event Log context Command Sequence Error Power-on Reset",
        "mandatory": "O",
    },

    # --- EGL Endurance Group Log ---
    {
        "id": "REQ-MON-EGL-001", "category": "MONITOR",
        "level1": "EGL Endurance Group Log", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.10", "spec_section": "§5.1.12.1.10",
        "spec_text": "If a Critical Warning bit is set to '1' in all Endurance Groups in the NVM subsystem, then the corresponding bit shall be set to '1' in the Critical Warning field of the SMART / Health Information log page. The Percentage Used field shall be updated once per power-on hour.",
        "spec_text_ko": "NVM 서브시스템의 모든 Endurance Group에서 Critical Warning 비트가 '1'로 설정되면, SMART / Health Information 로그 페이지의 Critical Warning 필드에서 해당 비트가 '1'로 설정되어야 한다. Percentage Used 필드는 전원 가동 시간당 한 번 업데이트되어야 한다.",
        "keyword": "Endurance Group LID 09h Critical Warning SMART",
        "mandatory": "O",
    },

    # =============================================
    # SECURITY - SEC Security Send/Receive
    # =============================================
    {
        "id": "REQ-SEC-SEC-001", "category": "SECURITY",
        "level1": "SEC Security Send/Receive", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.23", "spec_section": "§5.1.23",
        "spec_text": "The controller shall abort the Security Receive command with Invalid Field in Command if an unsupported value of the Security Protocol is specified. A Security Receive with Security Protocol 00h shall return information about the security protocols supported.",
        "spec_text_ko": "컨트롤러는 지원되지 않는 Security Protocol 값이 지정된 경우 Security Receive 명령을 Invalid Field in Command로 중단해야 한다. Security Protocol 00h인 Security Receive는 지원되는 보안 프로토콜 정보를 반환해야 한다.",
        "keyword": "Security Receive Protocol 00h Invalid Field",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SEC-002", "category": "SECURITY",
        "level1": "SEC Security Send/Receive", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.24", "spec_section": "§5.1.24",
        "spec_text": "The controller shall abort the Security Send command with Invalid Field in Command if a reserved value of the Security Protocol is specified.",
        "spec_text_ko": "컨트롤러는 Security Protocol의 예약된 값이 지정된 경우 Security Send 명령을 Invalid Field in Command로 중단해야 한다.",
        "keyword": "Security Send reserved Protocol Invalid Field",
        "mandatory": "M",
    },

    # === LCK Lockdown ===
    {
        "id": "REQ-SEC-LCK-001", "category": "SECURITY",
        "level1": "LCK Lockdown", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.15", "spec_section": "§5.1.15",
        "spec_text": "If the Command and Feature Lockdown capability is supported (CFLS bit in OACS set to '1'), the controller shall support the Lockdown command and the Command and Feature Lockdown log page.",
        "spec_text_ko": "Command and Feature Lockdown 기능이 지원되는 경우(OACS의 CFLS 비트가 '1'), 컨트롤러는 Lockdown 명령과 Command and Feature Lockdown 로그 페이지를 지원해야 한다.",
        "keyword": "Lockdown CFLS OACS log page",
        "mandatory": "O",
    },
    {
        "id": "REQ-SEC-LCK-002", "category": "SECURITY",
        "level1": "LCK Lockdown", "level2": None,
        "derived_from": "NVMe 2.2 §8.1.5", "spec_section": "§8.1.5",
        "spec_text": "The prohibiting of execution of a command shall persist until power cycle or further being allowed by a follow-on Lockdown command. If a prohibited command is processed, the controller shall abort it with Command Prohibited by Command and Feature Lockdown.",
        "spec_text_ko": "명령 실행 금지는 전원 사이클 또는 후속 Lockdown 명령에 의해 허용될 때까지 유지되어야 한다. 금지된 명령이 처리되면, 컨트롤러는 Command Prohibited by Command and Feature Lockdown으로 중단해야 한다.",
        "keyword": "Lockdown prohibit persist power cycle Command Prohibited",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-LCK-003", "category": "SECURITY",
        "level1": "LCK Lockdown", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.15", "spec_section": "§5.1.15",
        "spec_text": "If the Lockdown command specifies a command opcode or Feature Identifier that is not supported as being prohibitable, the command shall be aborted with Prohibition of Command Execution Not Supported.",
        "spec_text_ko": "Lockdown 명령이 금지 가능하지 않은 명령 opcode 또는 Feature Identifier를 지정하면, 명령은 Prohibition of Command Execution Not Supported로 중단되어야 한다.",
        "keyword": "Lockdown prohibitable Not Supported",
        "mandatory": "M",
    },

    # =============================================
    # INTEGRITY
    # =============================================
    {
        "id": "REQ-INT-VWC-001", "category": "INTEGRITY",
        "level1": "VWC Volatile Write Cache", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.1.4", "spec_section": "§5.1.25.1.4",
        "spec_text": "If a volatile write cache is present (VWC field in Identify Controller), then the Volatile Write Cache feature (Feature 06h) shall be supported. If not present, Set/Get Features for VWC shall abort with Invalid Field in Command.",
        "spec_text_ko": "휘발성 쓰기 캐시가 있는 경우(Identify Controller의 VWC 필드), Volatile Write Cache 기능(Feature 06h)이 지원되어야 한다. 없는 경우 VWC에 대한 Set/Get Features는 Invalid Field in Command로 중단되어야 한다.",
        "keyword": "VWC Feature 06h volatile write cache present",
        "mandatory": "C",
    },
    {
        "id": "REQ-INT-VWC-002", "category": "INTEGRITY",
        "level1": "VWC Volatile Write Cache", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.1.4", "spec_section": "§5.1.25.1.4",
        "spec_text": "If a volatile write cache is present and disabled (WCE bit cleared to '0'), then the user data written by any command to a namespace shall be persistent.",
        "spec_text_ko": "휘발성 쓰기 캐시가 있고 비활성화된 경우(WCE 비트가 '0'으로 클리어), 네임스페이스에 대한 모든 명령으로 기록된 사용자 데이터는 영구적이어야 한다.",
        "keyword": "VWC disabled WCE persistent data",
        "mandatory": "M",
    },
    {
        "id": "REQ-INT-RRL-001", "category": "INTEGRITY",
        "level1": "RRL Read Recovery Level", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.1.11", "spec_section": "§5.1.25.1.11",
        "spec_text": "The Read Recovery Level Config feature (Feature 12h) is used to configure the Read Recovery Level. Modifying the Read Recovery Level shall have no effect on the data contained in any associated namespace.",
        "spec_text_ko": "Read Recovery Level Config 기능(Feature 12h)은 Read Recovery Level을 구성하는 데 사용된다. Read Recovery Level 수정은 관련 네임스페이스에 포함된 데이터에 영향을 미쳐서는 안 된다.",
        "keyword": "RRL Read Recovery Level Feature 12h no data effect",
        "mandatory": "O",
    },
    {
        "id": "REQ-INT-EGR-001", "category": "INTEGRITY",
        "level1": "EGR Endurance Group", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.1.16", "spec_section": "§5.1.25.1.16",
        "spec_text": "If a bit is set to '1' in the Endurance Group Critical Warnings field which corresponds to a reserved bit in the Critical Warning field, then the Set Features command shall be aborted with Invalid Field in Command. If the Endurance Group Identifier specifies a non-existent group, the command shall be aborted with Invalid Field in Command.",
        "spec_text_ko": "Endurance Group Critical Warnings 필드에서 Critical Warning 필드의 예약된 비트에 해당하는 비트가 '1'로 설정되면, Set Features 명령은 Invalid Field in Command로 중단되어야 한다. Endurance Group Identifier가 존재하지 않는 그룹을 지정하면 명령은 Invalid Field in Command로 중단되어야 한다.",
        "keyword": "Endurance Group Event Config Feature 18h validation",
        "mandatory": "O",
    },
    {
        "id": "REQ-INT-MUS-001", "category": "INTEGRITY",
        "level1": "MUS Media Unit Status", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.12.1.16", "spec_section": "§5.1.12.1.16",
        "spec_text": "A controller supporting Fixed Capacity Management shall support the Media Unit Status log page (LID 10h) and shall set the Fixed Capacity Management bit to '1' in the CTRATT field of the Identify Controller data structure.",
        "spec_text_ko": "Fixed Capacity Management을 지원하는 컨트롤러는 Media Unit Status 로그 페이지(LID 10h)를 지원해야 하며, Identify Controller 데이터 구조의 CTRATT 필드에 Fixed Capacity Management 비트를 '1'로 설정해야 한다.",
        "keyword": "Media Unit Status LID 10h Fixed Capacity CTRATT",
        "mandatory": "O",
    },

    # =============================================
    # FW_MGMT - BP Boot Partition
    # =============================================
    {
        "id": "REQ-FW-BP-001", "category": "FW_MGMT",
        "level1": "BP Boot Partition", "level2": "Management",
        "derived_from": "NVMe 2.2 §8.1.2", "spec_section": "§8.1.2",
        "spec_text": "If the controller does not support the Boot Partitions feature, then the BPINFO, BPRSEL, and BPMBL properties shall be cleared to 0h.",
        "spec_text_ko": "컨트롤러가 Boot Partitions 기능을 지원하지 않는 경우, BPINFO, BPRSEL, BPMBL 속성은 0h로 클리어되어야 한다.",
        "keyword": "Boot Partition BPINFO BPRSEL BPMBL not supported",
        "mandatory": "M",
    },
    {
        "id": "REQ-FW-BP-002", "category": "FW_MGMT",
        "level1": "BP Boot Partition", "level2": "Management",
        "derived_from": "NVMe 2.2 §3.1.4", "spec_section": "§3.1.4",
        "spec_text": "If the host attempts to read beyond the end of a Boot Partition (offset + size > partition size in bytes), the controller shall not transfer data and shall report an error in the BPINFO.BRS field.",
        "spec_text_ko": "호스트가 Boot Partition의 끝을 넘어 읽기를 시도하면(오프셋 + 크기 > 파티션 크기), 컨트롤러는 데이터를 전송하지 않고 BPINFO.BRS 필드에 오류를 보고해야 한다.",
        "keyword": "Boot Partition read beyond BPINFO.BRS error",
        "mandatory": "M",
    },
    {
        "id": "REQ-FW-BP-003", "category": "FW_MGMT",
        "level1": "BP Boot Partition", "level2": "Write Protection",
        "derived_from": "NVMe 2.2 §8.1.3", "spec_section": "§8.1.3",
        "spec_text": "A controller that supports Boot Partitions and RPMB shall support at least one Boot Partition write protection mechanism. A controller that supports Boot Partitions without RPMB shall support Set Features Boot Partition Write Protection.",
        "spec_text_ko": "Boot Partition과 RPMB를 지원하는 컨트롤러는 최소 하나의 Boot Partition 쓰기 보호 메커니즘을 지원해야 한다. RPMB 없이 Boot Partition을 지원하는 컨트롤러는 Set Features Boot Partition Write Protection을 지원해야 한다.",
        "keyword": "Boot Partition Write Protection RPMB mechanism",
        "mandatory": "C",
    },
    {
        "id": "REQ-FW-BP-004", "category": "FW_MGMT",
        "level1": "BP Boot Partition", "level2": "Write Protection",
        "derived_from": "NVMe 2.2 §8.1.3", "spec_section": "§8.1.3",
        "spec_text": "If any Boot Partition is shared across multiple controllers, then the write protection state shall be enforced by all controllers that share that Boot Partition.",
        "spec_text_ko": "Boot Partition이 여러 컨트롤러 간 공유되는 경우, 쓰기 보호 상태는 해당 Boot Partition을 공유하는 모든 컨트롤러에 의해 적용되어야 한다.",
        "keyword": "Boot Partition shared controllers enforce write protection",
        "mandatory": "M",
    },

    # =============================================
    # VIRT - HMB Host Memory Buffer
    # =============================================
    {
        "id": "REQ-VIRT-HMB-001", "category": "VIRT",
        "level1": "HMB Host Memory Buffer", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.2.4", "spec_section": "§5.1.25.2.4",
        "spec_text": "If the Host Memory Buffer (Feature 0Dh) EHM bit is set to '1', the host memory buffer shall be enabled. If cleared to '0', the host memory buffer shall be disabled and the controller shall not use it.",
        "spec_text_ko": "Host Memory Buffer(Feature 0Dh) EHM 비트가 '1'로 설정되면, 호스트 메모리 버퍼가 활성화되어야 한다. '0'으로 클리어되면 호스트 메모리 버퍼가 비활성화되고 컨트롤러는 사용해서는 안 된다.",
        "keyword": "HMB Feature 0Dh EHM enable disable",
        "mandatory": "O",
    },
    {
        "id": "REQ-VIRT-HMB-002", "category": "VIRT",
        "level1": "HMB Host Memory Buffer", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.2.4", "spec_section": "§5.1.25.2.4",
        "spec_text": "If the host memory buffer is enabled, then a Set Features command to enable it again (EHM bit set to '1') shall abort with Command Sequence Error.",
        "spec_text_ko": "호스트 메모리 버퍼가 활성화된 상태에서 다시 활성화하려는 Set Features 명령(EHM 비트 '1')은 Command Sequence Error로 중단되어야 한다.",
        "keyword": "HMB already enabled Command Sequence Error",
        "mandatory": "M",
    },
    {
        "id": "REQ-VIRT-HMB-003", "category": "VIRT",
        "level1": "HMB Host Memory Buffer", "level2": None,
        "derived_from": "NVMe 2.2 §5.1.25.2.4", "spec_section": "§5.1.25.2.4",
        "spec_text": "After successful completion of a Set Features command that disables the host memory buffer, the controller shall not access any data in the host memory buffer until it has been re-enabled. If the Host Memory Descriptor List Entry Count is 0h, the controller shall abort with Invalid Field in Command.",
        "spec_text_ko": "호스트 메모리 버퍼를 비활성화하는 Set Features 명령이 성공적으로 완료된 후, 컨트롤러는 재활성화될 때까지 호스트 메모리 버퍼의 데이터에 접근해서는 안 된다. Host Memory Descriptor List Entry Count가 0h이면 Invalid Field in Command로 중단해야 한다.",
        "keyword": "HMB disable no access Descriptor List Count validation",
        "mandatory": "M",
    },

    # =============================================
    # RESET - SDN Shutdown
    # =============================================
    {
        "id": "REQ-RESET-SDN-001", "category": "RESET",
        "level1": "SDN Shutdown", "level2": None,
        "derived_from": "NVMe 2.2 §3.6", "spec_section": "§3.6",
        "spec_text": "If CSTS.SHST is set to 00b and an outstanding AER command exists with Normal NVM Subsystem Shutdown notification enabled, the controller shall issue a Normal NVM Subsystem Shutdown event prior to shutting down.",
        "spec_text_ko": "CSTS.SHST가 00b이고 미처리 AER 명령이 있으며 Normal NVM Subsystem Shutdown 알림이 활성화된 경우, 컨트롤러는 종료 전에 Normal NVM Subsystem Shutdown 이벤트를 발행해야 한다.",
        "keyword": "Shutdown Normal NVM Subsystem event AER CSTS.SHST",
        "mandatory": "M",
    },
    {
        "id": "REQ-RESET-SDN-002", "category": "RESET",
        "level1": "SDN Shutdown", "level2": None,
        "derived_from": "NVMe 2.2 §3.6", "spec_section": "§3.6",
        "spec_text": "The NVM subsystem shall not set CSTS.SHST to 10b on any controller until the entire NVM subsystem is ready to be powered off. The NVM subsystem shall indicate shutdown processing is complete by setting CSTS.SHST to 10b on all controllers.",
        "spec_text_ko": "NVM 서브시스템은 전체 NVM 서브시스템이 전원 끄기 준비가 될 때까지 어떤 컨트롤러에서도 CSTS.SHST를 10b로 설정해서는 안 된다. NVM 서브시스템은 모든 컨트롤러에서 CSTS.SHST를 10b로 설정하여 종료 처리 완료를 표시해야 한다.",
        "keyword": "Shutdown CSTS.SHST 10b all controllers ready",
        "mandatory": "M",
    },
    {
        "id": "REQ-RESET-SDN-003", "category": "RESET",
        "level1": "SDN Shutdown", "level2": None,
        "derived_from": "NVMe 2.2 §3.6", "spec_section": "§3.6",
        "spec_text": "An NVM Subsystem Reset shall abort any in progress NVM Subsystem Shutdown. A Controller Level Reset initiated by any other method shall not abort any in progress NVM Subsystem Shutdown.",
        "spec_text_ko": "NVM Subsystem Reset은 진행 중인 NVM Subsystem Shutdown을 중단해야 한다. 다른 방법으로 시작된 Controller Level Reset은 진행 중인 NVM Subsystem Shutdown을 중단해서는 안 된다.",
        "keyword": "Shutdown abort NVM Subsystem Reset CLR no abort",
        "mandatory": "M",
    },

    # === PCIE PCIe Reset ===
    {
        "id": "REQ-RESET-PCIE-001", "category": "RESET",
        "level1": "PCIE PCIe Reset", "level2": None,
        "derived_from": "NVMe 2.2 §3.7.2", "spec_section": "§3.7.2",
        "spec_text": "In all Controller Level Reset cases except a Controller Reset, the controller properties defined by the transport (e.g., PCIe registers defined by PCIe Base Specification) shall be reset as defined by the applicable NVMe Transport binding specification.",
        "spec_text_ko": "Controller Reset을 제외한 모든 Controller Level Reset 경우에, 전송 계층이 정의한 컨트롤러 속성(예: PCIe Base Specification이 정의한 PCIe 레지스터)은 해당 NVMe Transport 바인딩 사양에 따라 리셋되어야 한다.",
        "keyword": "PCIe Reset transport properties binding specification",
        "mandatory": "M",
    },

    # === LCM Life Cycle Management ===
    {
        "id": "REQ-RESET-LCM-001", "category": "RESET",
        "level1": "LCM Life Cycle Management", "level2": None,
        "derived_from": "NVMe 2.2 §3.1", "spec_section": "§3.1",
        "spec_text": "Memory-based controllers shall support only the static controller model.",
        "spec_text_ko": "메모리 기반 컨트롤러는 정적 컨트롤러 모델만 지원해야 한다.",
        "keyword": "Life Cycle static controller model memory-based",
        "mandatory": "M",
    },
]

for r in reqs:
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
print(f"\nImported {len(reqs)} requirements.")
