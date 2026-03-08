"""Insert Security category requirements: Sanitize & RPMB into DB."""
import sqlite3
import datetime

now = datetime.datetime.now(datetime.UTC).isoformat()
c = sqlite3.connect("nvme_req.db")

reqs = [
    # =============================================
    # Sanitize (level1: SAN Sanitize)
    # =============================================

    # --- Sanitize 기본 지원 ---
    {
        "id": "REQ-SEC-SAN-001",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Command",
        "derived_from": "NVMe 2.2 §8.1.24",
        "spec_section": "§8.1.24",
        "spec_text": "If the Sanitize command is supported, then all controllers in the NVM subsystem shall support the Sanitize Status log page, the Sanitize Operation Completed asynchronous event, and at least one of the following sanitize operation types: Block Erase, Overwrite, or Crypto Erase.",
        "spec_text_ko": "Sanitize 명령이 지원되는 경우, NVM 서브시스템의 모든 컨트롤러는 Sanitize Status 로그 페이지, Sanitize Operation Completed 비동기 이벤트, 그리고 Block Erase/Overwrite/Crypto Erase 중 최소 하나의 sanitize 작업 유형을 지원해야 한다.",
        "keyword": "Sanitize support Block Erase Overwrite Crypto Erase",
        "controller_type": "BOTH",
        "mandatory": "O",
    },
    {
        "id": "REQ-SEC-SAN-002",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Command",
        "derived_from": "NVMe 2.2 §8.1.24",
        "spec_section": "§8.1.24",
        "spec_text": "All controllers in the NVM subsystem shall support the same set of sanitize operation types and shall indicate the supported sanitize operation types in the Sanitize Capabilities field in the Identify Controller data structure.",
        "spec_text_ko": "NVM 서브시스템의 모든 컨트롤러는 동일한 sanitize 작업 유형 세트를 지원해야 하며, Identify Controller 데이터 구조의 Sanitize Capabilities 필드에 지원하는 sanitize 작업 유형을 표시해야 한다.",
        "keyword": "Sanitize Capabilities Identify Controller same types",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-003",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Command",
        "derived_from": "NVMe 2.2 §5.1.22",
        "spec_section": "§5.1.22",
        "spec_text": "If a Sanitize command specifies an unsupported value in the SANACT field, then the controller shall abort the command with a status code of Invalid Field in Command.",
        "spec_text_ko": "Sanitize 명령이 SANACT 필드에 지원되지 않는 값을 지정한 경우, 컨트롤러는 Invalid Field in Command 상태 코드로 명령을 중단해야 한다.",
        "keyword": "SANACT Invalid Field Sanitize command abort",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- Sanitize 시작/완료 ---
    {
        "id": "REQ-SEC-SAN-004",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Command",
        "derived_from": "NVMe 2.2 §5.1.22",
        "spec_section": "§5.1.22",
        "spec_text": "If a sanitize operation starts as a result of a Sanitize command, then the controller shall complete that Sanitize command with a status code of Successful Completion.",
        "spec_text_ko": "Sanitize 명령에 의해 sanitize 작업이 시작되면, 컨트롤러는 해당 Sanitize 명령을 Successful Completion 상태 코드로 완료해야 한다.",
        "keyword": "Sanitize start Successful Completion",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-005",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Command",
        "derived_from": "NVMe 2.2 §5.1.22",
        "spec_section": "§5.1.22",
        "spec_text": "If the controller completes a Sanitize command with any status code other than Successful Completion, then the controller shall not start the sanitize operation, shall not modify the Sanitize Status log page, and shall not alter any user data.",
        "spec_text_ko": "컨트롤러가 Sanitize 명령을 Successful Completion 이외의 상태 코드로 완료한 경우, sanitize 작업을 시작해서는 안 되며, Sanitize Status 로그 페이지를 수정하거나 사용자 데이터를 변경해서는 안 된다.",
        "keyword": "Sanitize failure no start no modify no alter data",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- Sanitize 진행 중 제한 ---
    {
        "id": "REQ-SEC-SAN-006",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Operation",
        "derived_from": "NVMe 2.2 §8.1.24.4",
        "spec_section": "§8.1.24.4",
        "spec_text": "When a sanitize operation starts, all controllers in the NVM subsystem shall abort any command not allowed during a sanitize operation with a status code of Sanitize In Progress, abort device self-test operations in progress, suspend autonomous power state management, and release stream identifiers for any open streams.",
        "spec_text_ko": "sanitize 작업이 시작되면, NVM 서브시스템의 모든 컨트롤러는 sanitize 작업 중 허용되지 않는 모든 명령을 Sanitize In Progress 상태 코드로 중단하고, 진행 중인 self-test 작업을 중단하며, 자율 전원 상태 관리를 일시 중지하고, 열린 스트림의 스트림 식별자를 해제해야 한다.",
        "keyword": "Sanitize In Progress abort commands self-test suspend",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-007",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Operation",
        "derived_from": "NVMe 2.2 §8.1.24.4",
        "spec_section": "§8.1.24.4",
        "spec_text": "During a sanitize operation, all I/O commands other than a Flush command shall be aborted with a status code of Sanitize In Progress. Activation of new firmware is prohibited during a sanitize operation.",
        "spec_text_ko": "sanitize 작업 중, Flush 명령을 제외한 모든 I/O 명령은 Sanitize In Progress 상태 코드로 중단되어야 한다. sanitize 작업 중 새 펌웨어 활성화는 금지된다.",
        "keyword": "Sanitize I/O abort Flush firmware activation prohibited",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-008",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Operation",
        "derived_from": "NVMe 2.2 §8.1.24.4",
        "spec_section": "§8.1.24.4",
        "spec_text": "During a sanitize operation, the Persistent Memory Region shall be prevented from being enabled (i.e., setting PMRCTL.EN to '1' does not result in PMRSTS.NRDY being cleared to '0').",
        "spec_text_ko": "sanitize 작업 중, Persistent Memory Region의 활성화가 방지되어야 한다(PMRCTL.EN을 '1'로 설정해도 PMRSTS.NRDY가 '0'으로 클리어되지 않음).",
        "keyword": "Sanitize PMR enable prevented PMRCTL",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- Sanitize 상태 보고 ---
    {
        "id": "REQ-SEC-SAN-009",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Status",
        "derived_from": "NVMe 2.2 §8.1.24",
        "spec_section": "§8.1.24",
        "spec_text": "The controller shall report that a sanitize operation is in progress if: sanitize processing is in progress (including additional media modification), the sanitization target is in the Media Verification state, or the sanitization target is in the Post-Verification Deallocation state.",
        "spec_text_ko": "컨트롤러는 sanitize 처리가 진행 중이거나(추가 미디어 수정 포함), sanitization 대상이 Media Verification 상태이거나, Post-Verification Deallocation 상태인 경우 sanitize 작업이 진행 중임을 보고해야 한다.",
        "keyword": "Sanitize in progress report Media Verification",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-010",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Status",
        "derived_from": "NVMe 2.2 §8.1.24",
        "spec_section": "§8.1.24",
        "spec_text": "The Sanitize Status log page shall be initialized before any controller in the NVM subsystem is ready and shall be updated when any state transition occurs.",
        "spec_text_ko": "Sanitize Status 로그 페이지는 NVM 서브시스템의 컨트롤러가 준비되기 전에 초기화되어야 하며, 상태 전이가 발생할 때마다 업데이트되어야 한다.",
        "keyword": "Sanitize Status log page initialize update state transition",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-011",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Status",
        "derived_from": "NVMe 2.2 §8.1.24",
        "spec_section": "§8.1.24",
        "spec_text": "The Sanitize Progress (SPROG) field shall not be modified under any conditions not explicitly permitted by this specification.",
        "spec_text_ko": "Sanitize Progress(SPROG) 필드는 이 사양에서 명시적으로 허용하지 않는 조건에서 수정되어서는 안 된다.",
        "keyword": "SPROG Sanitize Progress field modify restriction",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- Sanitize 실패 처리 ---
    {
        "id": "REQ-SEC-SAN-012",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Failure",
        "derived_from": "NVMe 2.2 §8.1.24",
        "spec_section": "§8.1.24",
        "spec_text": "If a sanitize operation fails, all controllers in the NVM subsystem shall abort any command not allowed during a sanitize operation with a status code of Sanitize Failed until a subsequent sanitize operation is started or successful recovery from the failed sanitize operation occurs.",
        "spec_text_ko": "sanitize 작업이 실패하면, NVM 서브시스템의 모든 컨트롤러는 후속 sanitize 작업이 시작되거나 실패한 sanitize 작업으로부터 성공적 복구가 이루어질 때까지 sanitize 작업 중 허용되지 않는 모든 명령을 Sanitize Failed 상태 코드로 중단해야 한다.",
        "keyword": "Sanitize Failed abort commands recovery",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-013",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Failure",
        "derived_from": "NVMe 2.2 §8.1.24.3",
        "spec_section": "§8.1.24.3",
        "spec_text": "In the Restricted Failure state, all controllers shall abort a Sanitize command specifying the SANACT field set to 001b (Exit Failure Mode) with a status code of Sanitize Failed, and shall abort a Sanitize command with the USE bit set to '1' with a status code of Sanitize Failed.",
        "spec_text_ko": "Restricted Failure 상태에서, 모든 컨트롤러는 SANACT 필드가 001b(Exit Failure Mode)로 설정된 Sanitize 명령을 Sanitize Failed 상태 코드로 중단해야 하며, USE 비트가 '1'로 설정된 Sanitize 명령도 Sanitize Failed로 중단해야 한다.",
        "keyword": "Restricted Failure SANACT 001b Exit Failure Mode abort",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-014",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Failure",
        "derived_from": "NVMe 2.2 §8.1.24.3",
        "spec_section": "§8.1.24.3",
        "spec_text": "If any controller in the NVM subsystem performs an Exit Failure Mode action, then the controller shall recover from the sanitization failure by transitioning the Sanitize Operation State Machine to the Idle state and shall complete the Sanitize command with a status code of Successful Completion.",
        "spec_text_ko": "NVM 서브시스템의 컨트롤러가 Exit Failure Mode 동작을 수행하면, 컨트롤러는 Sanitize Operation State Machine을 Idle 상태로 전이하여 sanitization 실패로부터 복구해야 하며, Sanitize 명령을 Successful Completion 상태 코드로 완료해야 한다.",
        "keyword": "Exit Failure Mode recover Idle Successful Completion",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- Sanitize 사전 검증 ---
    {
        "id": "REQ-SEC-SAN-015",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Command",
        "derived_from": "NVMe 2.2 §5.1.22",
        "spec_section": "§5.1.22",
        "spec_text": "If any Persistent Memory Region is enabled in an NVM subsystem, then the controller shall abort any Sanitize command with a status code of Sanitize Prohibited While Persistent Memory Region is Enabled.",
        "spec_text_ko": "NVM 서브시스템에서 Persistent Memory Region이 활성화되어 있는 경우, 컨트롤러는 모든 Sanitize 명령을 Sanitize Prohibited While Persistent Memory Region is Enabled 상태 코드로 중단해야 한다.",
        "keyword": "Sanitize PMR enabled prohibited abort",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-016",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Command",
        "derived_from": "NVMe 2.2 §5.1.22",
        "spec_section": "§5.1.22",
        "spec_text": "If any namespace is write protected in an NVM subsystem, then the controller shall abort any Sanitize command with a status code of Namespace is Write Protected.",
        "spec_text_ko": "NVM 서브시스템에서 네임스페이스가 쓰기 보호된 경우, 컨트롤러는 모든 Sanitize 명령을 Namespace is Write Protected 상태 코드로 중단해야 한다.",
        "keyword": "Sanitize namespace write protected abort",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-SAN-017",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Command",
        "derived_from": "NVMe 2.2 §5.1.22",
        "spec_section": "§5.1.22",
        "spec_text": "If a firmware activation with reset is pending, then the controller shall abort any Sanitize command.",
        "spec_text_ko": "리셋을 동반한 펌웨어 활성화가 보류 중인 경우, 컨트롤러는 모든 Sanitize 명령을 중단해야 한다.",
        "keyword": "Sanitize firmware activation pending abort",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- Sanitize CDW10 파라미터 ---
    {
        "id": "REQ-SEC-SAN-018",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Command",
        "derived_from": "NVMe 2.2 §5.1.22",
        "spec_section": "§5.1.22",
        "spec_text": "The Sanitize command CDW10 shall contain: SANACT field (bits 2:0) specifying the sanitize action, AUSE bit (bit 3) for unrestricted/restricted completion mode, OWPASS field (bits 7:4) for overwrite pass count, OIPBP bit (bit 8) for overwrite invert pattern, NDAS bit (bit 9) for no-deallocate after sanitize, and EMVS bit (bit 10) for entering media verification state.",
        "spec_text_ko": "Sanitize 명령 CDW10은 SANACT 필드(비트 2:0, sanitize 동작 지정), AUSE 비트(비트 3, 비제한/제한 완료 모드), OWPASS 필드(비트 7:4, overwrite 패스 수), OIPBP 비트(비트 8, overwrite 반전 패턴), NDAS 비트(비트 9, sanitize 후 비할당 금지), EMVS 비트(비트 10, media verification 상태 진입)를 포함해야 한다.",
        "keyword": "CDW10 SANACT AUSE OWPASS OIPBP NDAS EMVS",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- Sanitize 비동기 이벤트 ---
    {
        "id": "REQ-SEC-SAN-019",
        "level1": "SAN Sanitize",
        "level2": "Sanitize Status",
        "derived_from": "NVMe 2.2 §8.1.24.2",
        "spec_section": "§8.1.24.2",
        "spec_text": "In Completion Queue Entry Dword 0 for AER related to sanitize: the Log Page Identifier field shall be set to 81h (Sanitize Status log page), the Asynchronous Event Type field shall be set to 110b (I/O Command specific status), and the AEI field shall indicate the specific sanitize event (01h Completed, 02h Completed With Unexpected Deallocation, or 03h Entered Media Verification State).",
        "spec_text_ko": "sanitize 관련 AER의 CQE Dword 0에서: Log Page Identifier 필드는 81h(Sanitize Status 로그 페이지)로 설정되어야 하고, Asynchronous Event Type 필드는 110b(I/O Command specific status)로 설정되어야 하며, AEI 필드는 특정 sanitize 이벤트(01h 완료, 02h 예기치 않은 할당 해제와 함께 완료, 03h Media Verification State 진입)를 나타내야 한다.",
        "keyword": "Sanitize AER LID 81h AET 110b AEI",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # =============================================
    # RPMB (level1: RPMB Replay Protected Memory Block)
    # =============================================

    # --- RPMB 기본 지원 ---
    {
        "id": "REQ-SEC-RPMB-001",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Access",
        "derived_from": "NVMe 2.2 §5.1.13",
        "spec_section": "§5.1.13",
        "spec_text": "If the Number of RPMB Units (NRPMBU) field in Identify Controller is non-zero, then the controller shall support the Security Send and Security Receive commands for RPMB access.",
        "spec_text_ko": "Identify Controller의 NRPMBU(Number of RPMB Units) 필드가 0이 아닌 경우, 컨트롤러는 RPMB 접근을 위한 Security Send 및 Security Receive 명령을 지원해야 한다.",
        "keyword": "RPMB NRPMBU Security Send Security Receive",
        "controller_type": "BOTH",
        "mandatory": "C",
    },
    {
        "id": "REQ-SEC-RPMB-002",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Access",
        "derived_from": "NVMe 2.2 §8.1.21",
        "spec_section": "§8.1.21",
        "spec_text": "All RPMB targets supported shall have the same capabilities as defined in the RPMBS field in the Identify Controller data structure.",
        "spec_text_ko": "지원되는 모든 RPMB 타겟은 Identify Controller 데이터 구조의 RPMBS 필드에 정의된 것과 동일한 기능을 가져야 한다.",
        "keyword": "RPMB targets same capabilities RPMBS",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-RPMB-003",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Access",
        "derived_from": "NVMe 2.2 §8.1.21",
        "spec_section": "§8.1.21",
        "spec_text": "Security Send and Security Receive commands for RPMB do not use the namespace ID field; NSID shall be cleared to 0h.",
        "spec_text_ko": "RPMB용 Security Send 및 Security Receive 명령은 namespace ID 필드를 사용하지 않으며, NSID는 0h로 클리어되어야 한다.",
        "keyword": "RPMB NSID 0h Security Send Receive",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- RPMB Target 검증 ---
    {
        "id": "REQ-SEC-RPMB-004",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Access",
        "derived_from": "NVMe 2.2 §8.1.21",
        "spec_section": "§8.1.21",
        "spec_text": "If the value in the RPMB Target (RBT) field is not equal to the NVMe Security Specific Field (NSSF) in the Security Send or Security Receive command, then the controller shall return an error of Invalid Field in Command.",
        "spec_text_ko": "RPMB Target(RBT) 필드 값이 Security Send 또는 Security Receive 명령의 NSSF(NVMe Security Specific Field)와 같지 않은 경우, 컨트롤러는 Invalid Field in Command 오류를 반환해야 한다.",
        "keyword": "RPMB RBT NSSF validation Invalid Field",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- RPMB 명령 완료 ---
    {
        "id": "REQ-SEC-RPMB-005",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Access",
        "derived_from": "NVMe 2.2 §8.1.21",
        "spec_section": "§8.1.21",
        "spec_text": "The controller shall not return successful completion of a Security Send or Security Receive command for RPMB access until the requested RPMB Request/Response Message Type indicated is completed.",
        "spec_text_ko": "컨트롤러는 요청된 RPMB Request/Response Message Type이 완료될 때까지 RPMB 접근을 위한 Security Send 또는 Security Receive 명령의 성공적 완료를 반환해서는 안 된다.",
        "keyword": "RPMB completion Security Send Receive blocking",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- RPMB Authentication Key ---
    {
        "id": "REQ-SEC-RPMB-006",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Authentication",
        "derived_from": "NVMe 2.2 §8.1.21",
        "spec_section": "§8.1.21",
        "spec_text": "Once the authentication key is programmed, the RPMB Operation Result Operation Status field shall not be set to 07h (Authentication Key not yet programmed).",
        "spec_text_ko": "인증 키가 프로그래밍된 후, RPMB Operation Result의 Operation Status 필드는 07h(Authentication Key not yet programmed)로 설정되어서는 안 된다.",
        "keyword": "RPMB authentication key programmed status 07h",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- RPMB Write Counter ---
    {
        "id": "REQ-SEC-RPMB-007",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Authentication",
        "derived_from": "NVMe 2.2 §8.1.21",
        "spec_section": "§8.1.21",
        "spec_text": "After the write counter has reached the maximum value of FFFFFFFFh, the controller shall no longer increment to prevent overflow.",
        "spec_text_ko": "쓰기 카운터가 최대값 FFFFFFFFh에 도달한 후, 컨트롤러는 오버플로우를 방지하기 위해 더 이상 증가시켜서는 안 된다.",
        "keyword": "RPMB write counter FFFFFFFFh overflow prevent",
        "controller_type": "BOTH",
        "mandatory": "M",
    },

    # --- RPMB Boot Partition 쓰기 보호 ---
    {
        "id": "REQ-SEC-RPMB-008",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Boot Partition",
        "derived_from": "NVMe 2.2 §8.1.21",
        "spec_section": "§8.1.21",
        "spec_text": "A controller that supports both Boot Partitions and RPMB shall support at least one of the following Boot Partition write protection mechanisms: Set Features Boot Partition Write Protection or RPMB Boot Partition Write Protection.",
        "spec_text_ko": "Boot Partition과 RPMB를 모두 지원하는 컨트롤러는 Set Features Boot Partition Write Protection 또는 RPMB Boot Partition Write Protection 중 최소 하나의 Boot Partition 쓰기 보호 메커니즘을 지원해야 한다.",
        "keyword": "RPMB Boot Partition write protection mechanism",
        "controller_type": "BOTH",
        "mandatory": "C",
    },
    {
        "id": "REQ-SEC-RPMB-009",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Boot Partition",
        "derived_from": "NVMe 2.2 §8.1.21",
        "spec_section": "§8.1.21",
        "spec_text": "Once enabled, the controller shall prevent disabling RPMB Boot Partition Write Protection. If Set Features Boot Partition Write Protection is also supported, the Authenticated Data Write that enables RPMB Boot Partition Write Protection shall also result in the controller changing Boot Partition protection state values to 100b.",
        "spec_text_ko": "RPMB Boot Partition Write Protection이 활성화된 후, 컨트롤러는 비활성화를 방지해야 한다. Set Features Boot Partition Write Protection도 지원되는 경우, RPMB Boot Partition Write Protection을 활성화하는 Authenticated Data Write는 Boot Partition 보호 상태 값을 100b로 변경해야 한다.",
        "keyword": "RPMB Boot Partition Write Protection disable prevent 100b",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
    {
        "id": "REQ-SEC-RPMB-010",
        "level1": "RPMB Replay Protected Memory Block",
        "level2": "RPMB Boot Partition",
        "derived_from": "NVMe 2.2 §5.1.25",
        "spec_section": "§5.1.25",
        "spec_text": "If the Boot Partition Write Protection Enable bit is set to '1' in the RPMB Device Configuration Block, then the controller shall return a value of 100b for both the Boot Partition 0 and Boot Partition 1 Write Protection State fields as a result of the Get Features command. A Set Features command with either field set to 100b shall be aborted with Invalid Field in Command.",
        "spec_text_ko": "RPMB Device Configuration Block에서 Boot Partition Write Protection Enable 비트가 '1'로 설정된 경우, 컨트롤러는 Get Features 명령 결과로 Boot Partition 0 및 Boot Partition 1 Write Protection State 필드에 100b 값을 반환해야 한다. 어느 필드든 100b로 설정된 Set Features 명령은 Invalid Field in Command로 중단되어야 한다.",
        "keyword": "RPMB BPPED Get Features 100b Set Features abort",
        "controller_type": "BOTH",
        "mandatory": "M",
    },
]

for r in reqs:
    r.setdefault("category", "SECURITY")
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
print(f"\nImported {len(reqs)} Security requirements.")
