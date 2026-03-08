# NVMe 2.2 시스템 요구사항 — 카테고리 1: 식별 및 기능 협상

> **Spec 출처**: NVM Express® Base Specification, Revision 2.2 (2025.03.11 Ratified)  
> **대상 컨트롤러**: I/O Controller (PCIe SSD)  
> **작성 기준**: `shall` → "~해야 한다" / `shall not` → "~해서는 안 된다"  
> **초안 작성일**: 2025-03-08  

---

## ID 체계

```
REQ-IDENT-{세부분류}-{3자리 번호}

세부분류:
  CTRL  컨트롤러 타입·모델
  PROP  컨트롤러 속성(Properties / Registers)
  CMD   명령어 지원 의무
  LOG   Log Page 지원 의무
  FTR   Feature 지원 의무
  IDFY  Identify 명령어 동작
  IOSC  I/O Command Set 협상
  INIT  컨트롤러 초기화 시퀀스
```

---

## 상태 범례

| 기호 | 의미 |
|---|---|
| 🔴 OPEN | 검증 케이스 미연결 |
| 🟡 LINKED | 검증 케이스 연결됨 |
| 🟢 VERIFIED | 검증 완료 |

---

## 1. 컨트롤러 모델 및 타입 (CTRL)

### REQ-IDENT-CTRL-001
- **요구사항**: Device는 NVM 서브시스템 내 모든 컨트롤러가 동일한 컨트롤러 모델(static 또는 dynamic)을 지원해야 한다.
- **Spec**: §3.1
- **키워드**: `shall`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CTRL-002
- **요구사항**: Device는 memory-based controller(PCIe)인 경우 static controller model만 지원해야 한다.
- **Spec**: §3.1 Memory-Based Controller Architecture
- **키워드**: `shall`
- **조건**: PCIe 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CTRL-003
- **요구사항**: Device는 Identify Controller data structure의 CNTRLTYPE 필드에 올바른 컨트롤러 타입을 보고해야 한다.
- **Spec**: §3.1.3, Figure 313 CNTRLTYPE 필드
- **키워드**: `정보 정확성`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CTRL-004
- **요구사항**: Device는 round robin 명령어 중재 메커니즘을 지원해야 한다.
- **Spec**: §3.4.4
- **키워드**: `shall`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CTRL-005
- **요구사항**: Device는 Controller Ready With Media Support(CAP.CRMS.CRWMS) 비트를 '1'로 설정해야 한다.
- **Spec**: §3.5.3
- **키워드**: `shall`
- **조건**: NVM Express Base Spec Revision 2.0 이후 준수 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

---

## 2. 컨트롤러 속성 (Properties/Registers) (PROP)

### REQ-IDENT-PROP-001
- **요구사항**: Device는 CAP(Controller Capabilities) 속성을 지원해야 한다.
- **Spec**: Figure 33 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-002
- **요구사항**: Device는 VS(Version) 속성을 지원해야 한다.
- **Spec**: Figure 33 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-003
- **요구사항**: Device는 CC(Controller Configuration) 속성을 지원해야 한다.
- **Spec**: Figure 33 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-004
- **요구사항**: Device는 CSTS(Controller Status) 속성을 지원해야 한다.
- **Spec**: Figure 33 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-005
- **요구사항**: Device는 CRTO(Controller Ready Timeouts) 속성을 지원해야 한다.
- **Spec**: Figure 33, §3.5.4 — Mandatory (Revision 2.0 이후)
- **키워드**: `Mandatory`
- **조건**: NVM Express Base Spec Revision 2.0 이후 준수 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-006
- **요구사항**: Device는 reserved 속성 및 속성 내 reserved 비트를 읽을 때 '0'을 반환해야 한다.
- **Spec**: §3.1.4
- **키워드**: `shall`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-007
- **요구사항**: Device는 CC.MPS에 CAP.MPSMIN보다 작은 메모리 페이지 크기가 설정되는 경우를 허용해서는 안 된다.
- **Spec**: Figure 36, CAP.MPSMIN
- **키워드**: `shall not`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-008
- **요구사항**: Device는 CC.MPS에 CAP.MPSMAX보다 큰 메모리 페이지 크기가 설정되는 경우를 허용해서는 안 된다.
- **Spec**: Figure 36, CAP.MPSMAX
- **키워드**: `shall not`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-009
- **요구사항**: Device는 CC.EN이 '1'로 설정되면 명령어를 처리해야 한다.
- **Spec**: Figure 41, CC.EN
- **키워드**: `shall`
- **조건**: CC.EN = 1
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-010
- **요구사항**: Device는 CC.EN이 '0'으로 설정되면 명령어를 처리해서도, Completion Queue에 완료 항목을 포스팅해서도 안 된다.
- **Spec**: Figure 41, CC.EN
- **키워드**: `shall not`
- **조건**: CC.EN = 0
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-011
- **요구사항**: Device는 CC.EN '1'→'0' 전환(Controller Reset) 이전에 완료 큐에 포스팅된 명령어 결과에 영향(예: data loss)이 없음을 보장해야 한다.
- **Spec**: Figure 41, CC.EN
- **키워드**: `shall`
- **조건**: Controller Reset 발생 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-012
- **요구사항**: Device는 CC.EN이 '0'으로 클리어되면 재활성화 준비 완료 시점에 CSTS.RDY를 '0'으로 클리어해야 한다.
- **Spec**: Figure 41, CC.EN
- **키워드**: `shall (implied)`
- **조건**: CC.EN = 0 전환 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-013
- **요구사항**: Device는 CC.EN이 '1'로 설정되면 명령어 처리 준비 완료 시점에 CSTS.RDY를 '1'로 설정해야 한다.
- **Spec**: Figure 41, CC.EN
- **키워드**: `shall (implied)`
- **조건**: CC.EN = 1 전환 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-014
- **요구사항**: Device는 CAP.CRMS가 11b가 아닌 경우 CC.CRIME 비트를 read-only '0'으로 유지해야 한다.
- **Spec**: Figure 41, CC.CRIME
- **키워드**: `shall`
- **조건**: CAP.CRMS ≠ 11b
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-015
- **요구사항**: Device는 I/O Queue를 지원하지 않는 경우 CC.IOCQES 및 CC.IOSQES 필드를 read-only 0h로 유지해야 한다.
- **Spec**: Figure 41, CC.IOCQES/IOSQES
- **키워드**: `shall`
- **조건**: I/O Queue 미지원 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-016
- **요구사항**: Device는 CC.IOCQES와 CC.IOSQES를 초기화하지 않은 상태에서 I/O Queue 생성 명령을 수신하면 `Invalid Queue Size` 상태 코드로 abort해야 한다.
- **Spec**: §3.1.4 CC
- **키워드**: `shall`
- **조건**: CC.IOCQES/IOSQES 미초기화 상태에서 I/O Queue 생성 시도 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-017
- **요구사항**: Device는 CC.CSS 필드를 컨트롤러가 비활성화(CC.EN = '0') 상태에서만 변경할 수 있어야 한다.
- **Spec**: Figure 41, CC.CSS
- **키워드**: `shall`
- **조건**: CC.CSS 변경 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-018
- **요구사항**: Device는 셧다운 처리가 완료되기 전에는 CSTS.RDY를 '0'→'1'로 전환해서는 안 된다.
- **Spec**: Figure 42, CSTS.RDY
- **키워드**: `shall`
- **조건**: 셧다운 처리 중
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-019
- **요구사항**: Device는 NVM Subsystem Reset 발생 시 CSTS.ST 비트를 '0'으로 클리어해야 하며, 다른 Controller Level Reset은 이 비트를 변경해서는 안 된다.
- **Spec**: Figure 42, CSTS.ST
- **키워드**: `shall` / `shall not`
- **조건**: Controller Level Reset 발생 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-020
- **요구사항**: Device는 CSTS.SHST가 00b인 상태에서 Controller Level Reset이 발생하면 CSTS.SHST 값을 변경해서는 안 된다.
- **Spec**: Figure 42, CSTS.SHST
- **키워드**: `shall not`
- **조건**: CSTS.SHST = 00b, CLR 발생 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-021
- **요구사항**: Device는 CRTO.CRWMT 값이 CRTO.CRIMT 값보다 크거나 같아야 한다.
- **Spec**: Figure 57, CRTO.CRWMT
- **키워드**: `shall`
- **조건**: CAP.CRMS.CRIMS 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-022
- **요구사항**: Device는 CRTO.CRIMT 필드를 CAP.CRMS.CRIMS 비트가 '0'인 경우 0h로 클리어해야 한다.
- **Spec**: Figure 57, CRTO.CRIMT
- **키워드**: `shall`
- **조건**: CAP.CRMS.CRIMS = 0
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-023
- **요구사항**: Device는 NSSR.NSSRC 필드를 읽을 때 항상 0h를 반환해야 한다.
- **Spec**: Figure 43, NSSR.NSSRC
- **키워드**: `shall`
- **조건**: NSSR 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-024
- **요구사항**: Device는 AQA, ASQ, ACQ 속성이 Controller Reset에 의해 리셋되지 않아야 한다.
- **Spec**: §3.1.4.6~8
- **키워드**: `shall not`
- **조건**: Controller Reset 발생 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-PROP-025
- **요구사항**: Device는 CAP.TO 필드를 Figure 36에 정의된 대로 설정해야 한다.
- **Spec**: §3.5.4
- **키워드**: `shall`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

---

## 3. 필수 Admin 명령어 지원 (CMD)

### REQ-IDENT-CMD-001
- **요구사항**: Device는 Get Log Page 명령어(Opcode 02h)를 지원해야 한다.
- **Spec**: Figure 28 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-002
- **요구사항**: Device는 Identify 명령어(Opcode 06h)를 지원해야 한다.
- **Spec**: Figure 28 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-003
- **요구사항**: Device는 Abort 명령어(Opcode 08h)를 지원해야 한다.
- **Spec**: Figure 28 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-004
- **요구사항**: Device는 임의의 Feature가 구현된 경우 Set Features 명령어(Opcode 09h)를 지원해야 한다.
- **Spec**: Figure 32 Note
- **키워드**: `shall`
- **조건**: Feature 구현 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-005
- **요구사항**: Device는 임의의 Feature가 구현된 경우 Get Features 명령어(Opcode 0Ah)를 지원해야 한다.
- **Spec**: Figure 32 Note
- **키워드**: `shall`
- **조건**: Feature 구현 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-006
- **요구사항**: Device는 Telemetry Log, Firmware Commit, 또는 SMART/Health Critical Warning을 지원하는 경우 Asynchronous Event Request 명령어(Opcode 0Ch)를 지원해야 한다.
- **Spec**: Figure 28 Note 5
- **키워드**: `Mandatory (conditional)`
- **조건**: Telemetry Log / FW Commit / SMART Critical Warning 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-007
- **요구사항**: Device는 PCIe 기반인 경우 Delete I/O Submission Queue 명령어(Opcode 00h)를 지원해야 한다.
- **Spec**: Figure 28 Note 9
- **키워드**: `Mandatory (PCIe)`
- **조건**: PCIe 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-008
- **요구사항**: Device는 PCIe 기반인 경우 Create I/O Submission Queue 명령어(Opcode 01h)를 지원해야 한다.
- **Spec**: Figure 28 Note 9
- **키워드**: `Mandatory (PCIe)`
- **조건**: PCIe 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-009
- **요구사항**: Device는 PCIe 기반인 경우 Delete I/O Completion Queue 명령어(Opcode 04h)를 지원해야 한다.
- **Spec**: Figure 28 Note 9
- **키워드**: `Mandatory (PCIe)`
- **조건**: PCIe 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-010
- **요구사항**: Device는 PCIe 기반인 경우 Create I/O Completion Queue 명령어(Opcode 05h)를 지원해야 한다.
- **Spec**: Figure 28 Note 9
- **키워드**: `Mandatory (PCIe)`
- **조건**: PCIe 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-CMD-011
- **요구사항**: Device는 NVMe Transport에서 Keep Alive를 요구하는 경우 Keep Alive 명령어(Opcode 18h)를 지원해야 한다.
- **Spec**: Figure 28 Note 2, §3.9
- **키워드**: `Mandatory (transport-dependent)`
- **조건**: Transport에서 Keep Alive 요구 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

---

## 4. 필수 Log Page 지원 (LOG)

### REQ-IDENT-LOG-001
- **요구사항**: Device는 Supported Log Pages log page(LID 00h)를 지원해야 한다.
- **Spec**: Figure 31 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-LOG-002
- **요구사항**: Device는 Error Information log page(LID 01h)를 지원해야 한다.
- **Spec**: Figure 31 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-LOG-003
- **요구사항**: Device는 SMART/Health Information log page(LID 02h, Controller scope)를 지원해야 한다.
- **Spec**: Figure 31 — I/O Controller: Mandatory (Controller scope)
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-LOG-004
- **요구사항**: Device는 Firmware Slot Information log page(LID 03h)를 지원해야 한다.
- **Spec**: Figure 31 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-LOG-005
- **요구사항**: Device는 Commands Supported and Effects log page(LID 05h)를 지원해야 한다.
- **Spec**: Figure 31 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-LOG-006
- **요구사항**: Device는 Feature Identifiers Supported and Effects log page(LID 12h)를 지원해야 한다.
- **Spec**: Figure 31 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-LOG-007
- **요구사항**: Device는 NVMe-MI Send/Receive 명령어를 지원하는 경우 NVMe-MI Commands Supported and Effects log page(LID 13h)를 지원해야 한다.
- **Spec**: Figure 31 Note 7
- **키워드**: `Mandatory (conditional)`
- **조건**: NVMe-MI Send/Receive 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-LOG-008
- **요구사항**: Device는 Reachability Reporting을 지원하는 경우 Reachability Groups log page(LID 1Ah)를 지원해야 한다.
- **Spec**: Figure 31 — Mandatory if Reachability Reporting supported
- **키워드**: `Mandatory (conditional)`
- **조건**: Reachability Reporting 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-LOG-009
- **요구사항**: Device는 Reachability Reporting을 지원하는 경우 Reachability Associations log page(LID 1Bh)를 지원해야 한다.
- **Spec**: Figure 31 — Mandatory if Reachability Reporting supported
- **키워드**: `Mandatory (conditional)`
- **조건**: Reachability Reporting 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

---

## 5. 필수 Feature 지원 (FTR)

### REQ-IDENT-FTR-001
- **요구사항**: Device는 Arbitration Feature(FID 01h)를 지원해야 한다.
- **Spec**: Figure 32 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-FTR-002
- **요구사항**: Device는 Power Management Feature(FID 02h)를 지원해야 한다.
- **Spec**: Figure 32 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-FTR-003
- **요구사항**: Device는 Temperature Threshold Feature(FID 04h)를 지원해야 한다.
- **Spec**: Figure 32 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-FTR-004
- **요구사항**: Device는 Number of Queues Feature(FID 07h)를 지원해야 한다.
- **Spec**: Figure 32 — I/O Controller: Mandatory
- **키워드**: `Mandatory`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-FTR-005
- **요구사항**: Device는 PCIe 기반인 경우 Interrupt Coalescing Feature(FID 08h)를 지원해야 한다.
- **Spec**: Figure 32 Note 2
- **키워드**: `Mandatory (PCIe)`
- **조건**: PCIe 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-FTR-006
- **요구사항**: Device는 PCIe 기반인 경우 Interrupt Vector Configuration Feature(FID 09h)를 지원해야 한다.
- **Spec**: Figure 32 Note 2
- **키워드**: `Mandatory (PCIe)`
- **조건**: PCIe 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-FTR-007
- **요구사항**: Device는 Telemetry Log, Firmware Commit, 또는 SMART/Health Critical Warning을 지원하는 경우 Asynchronous Event Configuration Feature(FID 0Bh)를 지원해야 한다.
- **Spec**: Figure 32 Note 8
- **키워드**: `Mandatory (conditional)`
- **조건**: Telemetry / FW Commit / SMART Critical Warning 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-FTR-008
- **요구사항**: Device는 NVMe Transport에서 Keep Alive를 요구하는 경우 Keep Alive Timer Feature(FID 0Fh)를 지원해야 한다.
- **Spec**: Figure 32 Note 7
- **키워드**: `Mandatory (transport-dependent)`
- **조건**: Transport에서 Keep Alive 요구 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

---

## 6. Identify 명령어 동작 (IDFY)

### REQ-IDENT-IDFY-001
- **요구사항**: Device는 지원하지 않는 CNS 값이 지정된 Identify 명령어를 `Invalid Field in Command` 상태 코드로 abort해야 한다.
- **Spec**: §5.1.13
- **키워드**: `shall`
- **조건**: 지원하지 않는 CNS 값 수신 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IDFY-002
- **요구사항**: Device는 지정된 namespace가 CNS 값이 요구하는 I/O Command Set과 연관되지 않은 경우 Identify 명령어를 `Invalid I/O Command Set` 상태 코드로 abort해야 한다.
- **Spec**: §5.1.13
- **키워드**: `shall`
- **조건**: NSID가 CNS 요구 I/O CS와 불일치 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IDFY-003
- **요구사항**: Device는 Identify 명령어에서 반환할 항목이 부족한 경우 미사용 부분을 0으로 채워 반환해야 한다.
- **Spec**: §5.1.13
- **키워드**: `shall (implied)`
- **조건**: 반환 항목 부족 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IDFY-004
- **요구사항**: Device는 Identify에서 CNTID 필드가 사용되지 않는 CNS 값에 대해 해당 필드를 무시해야 한다.
- **Spec**: Figure 308, CDW10.CNTID
- **키워드**: `shall`
- **조건**: CNTID 미사용 CNS 값 수신 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IDFY-005
- **요구사항**: Device는 Identify Controller(CNS 01h)의 IEEE 필드에 유효한 IEEE/RAC 할당 식별자를 설정해야 한다.
- **Spec**: Figure 313, IEEE field
- **키워드**: `shall`
- **조건**: 무조건
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IDFY-006
- **요구사항**: Device는 NVM Express Base Specification Revision 1.2 이후를 준수하는 경우 Identify Controller(CNS 01h)의 VER 필드에 0이 아닌 값을 보고해야 한다.
- **Spec**: Figure 313, VER field
- **키워드**: `shall`
- **조건**: Rev 1.2+ 준수 컨트롤러
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IDFY-007
- **요구사항**: Device는 선택적 비동기 이벤트를 호스트 소프트웨어가 활성화하기 전에 전송해서는 안 된다.
- **Spec**: Figure 313, OAES field
- **키워드**: `shall not`
- **조건**: AER 활성화 전
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IDFY-008
- **요구사항**: Device는 Namespace Management를 지원하는 경우 Identify 명령어의 CDW10.CNTID 필드를 지원해야 한다.
- **Spec**: Figure 308
- **키워드**: `shall`
- **조건**: Namespace Management 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IDFY-009
- **요구사항**: Device는 Identify 명령어에서 PRP를 사용하는 경우 PRP List 포인터를 사용해서는 안 된다(데이터 버퍼가 페이지 경계를 하나 이상 넘을 수 없기 때문).
- **Spec**: Figure 307
- **키워드**: `shall not`
- **조건**: PRP 사용 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

---

## 7. I/O Command Set 협상 (IOSC)

### REQ-IDENT-IOSC-001
- **요구사항**: Device는 NVM Command Set 이외의 I/O Command Set을 지원하는 경우 CAP.CSS.IOCSS 비트를 '1'로 설정해야 한다.
- **Spec**: Figure 36, CAP.CSS
- **키워드**: `shall`
- **조건**: NVM CS 외 I/O CS 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IOSC-002
- **요구사항**: Device는 지원하는 I/O Command Set과 동시 지원 가능한 조합을 Identify I/O Command Set data structure(CNS 1Ch)에 올바르게 보고해야 한다.
- **Spec**: §3.1.3.1
- **키워드**: `정보 정확성`
- **조건**: I/O CS 지원 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-IOSC-003
- **요구사항**: Device는 CC.CSS = 111b(Admin only mode)에서 I/O Command Set specific Admin 명령어를 수신하면 `Invalid Command Opcode` 상태 코드로 abort해야 한다.
- **Spec**: Figure 41, CC.CSS 값 111b
- **키워드**: `shall (implied)`
- **조건**: CC.CSS = 111b
- **검증 케이스**: —
- **상태**: 🔴 OPEN

---

## 8. 컨트롤러 초기화 시퀀스 (INIT)

### REQ-IDENT-INIT-001
- **요구사항**: Device는 §3.5.1에서 정의한 초기화 절차 완료 후 Admin 및 I/O 명령어를 처리할 준비가 되어야 한다.
- **Spec**: §3.5.1
- **키워드**: `shall`
- **조건**: 초기화 완료 후
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-INIT-002
- **요구사항**: Device는 Controller Ready With Media mode에서 CSTS.RDY가 '1'이 될 때까지 모든 명령어를 에러 없이 처리할 수 있어야 하고, 모든 attached namespace와 Admin 명령어에 필요한 미디어가 준비되어야 한다.
- **Spec**: §3.5.3
- **키워드**: `shall`
- **조건**: Controller Ready With Media mode
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-INIT-003
- **요구사항**: Device는 Controller Ready Independent of Media mode에서 CC.EN 전환 후 CRTO.CRWMT 이내에 모든 I/O 명령어를 에러 없이 처리할 수 있어야 한다.
- **Spec**: §3.5.3
- **키워드**: `shall`
- **조건**: Controller Ready Independent of Media mode
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-INIT-004
- **요구사항**: Device는 초기화 실패로 인해 타임아웃이 발생하더라도 CC.EN 전환 후 CRTO.CRWMT 이내에 반드시 CSTS.RDY를 '1'로 설정해야 한다.
- **Spec**: §3.5.4
- **키워드**: `shall`
- **조건**: 초기화 에러 발생 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

### REQ-IDENT-INIT-005
- **요구사항**: Device는 초기화 중 Controller Ready Timeout이 초과되고 Persistent Event log page가 지원되는 경우, NVM Subsystem Hardware Error Event(Controller Ready Timeout Exceeded)를 기록해야 한다.
- **Spec**: §3.5.4
- **키워드**: `shall`
- **조건**: Persistent Event log 지원 + 초기화 timeout 발생 시
- **검증 케이스**: —
- **상태**: 🔴 OPEN

---

## 요구사항 통계

| 분류 | 총 개수 | 🔴 OPEN | 🟡 LINKED | 🟢 VERIFIED |
|---|---|---|---|---|
| CTRL (컨트롤러 타입·모델) | 5 | 5 | 0 | 0 |
| PROP (속성/레지스터) | 25 | 25 | 0 | 0 |
| CMD (명령어 지원) | 11 | 11 | 0 | 0 |
| LOG (Log Page 지원) | 9 | 9 | 0 | 0 |
| FTR (Feature 지원) | 8 | 8 | 0 | 0 |
| IDFY (Identify 동작) | 9 | 9 | 0 | 0 |
| IOSC (I/O CS 협상) | 3 | 3 | 0 | 0 |
| INIT (초기화 시퀀스) | 5 | 5 | 0 | 0 |
| **합계** | **75** | **75** | **0** | **0** |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| 0.1 | 2025-03-08 | 초안 작성 (NVMe 2.2 spec §3.1~3.5, §5.1.13 기반) |

---

## Appendix: Spec 누락 방지 방법 (Coverage Gap Analysis)

### 방법 1: shall 문장 기계적 전수 추출 (추천 ★★★)

PDF에서 대상 섹션의 shall 문장을 전수 추출하고 각 REQ-ID와 1:1 매핑한다.  
매핑되지 않은 shall 문장이 누락 후보다.

```python
import pdfplumber, re

with pdfplumber.open("spec.pdf") as pdf:
    for page in pdf.pages[57:133]:   # §3.1~3.5 범위
        text = page.extract_text() or ""
        sentences = re.split(r'(?<=[.;])\s+', text)
        for s in sentences:
            if " shall " in s.lower():
                print(s.strip())
```

---

### 방법 2: Figure(표) 기반 Mandatory 항목 체크리스트

spec의 핵심 표는 Mandatory/Optional/Prohibited를 체계적으로 정의한다.  
각 표의 Mandatory 행을 REQ-ID와 1:1 대응시켜 누락 여부를 확인한다.

| 체크 대상 표 | REQ 분류 | 이번 문서 커버 |
|---|---|---|
| Figure 28: Admin Command Support | REQ-IDENT-CMD | ✅ |
| Figure 31: Log Page Support | REQ-IDENT-LOG | ✅ |
| Figure 32: Feature Support | REQ-IDENT-FTR | ✅ |
| Figure 33: Property Definition | REQ-IDENT-PROP | ✅ |
| Figure 36~57: 각 Register 정의 | REQ-IDENT-PROP | ✅ (주요 shall만 추출) |
| Figure 311: Identify CNS Values | REQ-IDENT-IDFY | ✅ |

---

### 방법 3: DB 역추적 — 미연결 REQ 자동 조회

```sql
-- 커버되지 않은 요구사항 조회
SELECT r.req_id, r.category, r.requirement
FROM requirements r
LEFT JOIN test_case_requirement tcr ON r.req_id = tcr.req_id
WHERE tcr.req_id IS NULL
ORDER BY r.category, r.req_id;

-- 카테고리별 커버리지 비율
SELECT r.category,
       COUNT(*) AS total,
       SUM(CASE WHEN tcr.req_id IS NOT NULL THEN 1 ELSE 0 END) AS covered,
       ROUND(100.0 * SUM(CASE WHEN tcr.req_id IS NOT NULL THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS coverage_pct
FROM requirements r
LEFT JOIN test_case_requirement tcr ON r.req_id = tcr.req_id
GROUP BY r.category;
```

---

### 현재 미커버 영역 (후속 추출 필요)

| 섹션 | 내용 |
|---|---|
| Figure 313 세부 필드 | Identify Controller Data Structure 각 필드별 shall (수십 개) |
| §5.1.13 CNS 00h, 05h, 08h | Identify Namespace Data Structure 관련 shall |
| Figure 32 NVM CS 참조 항목 | FID 03h, 05h, 0Ah, 15h 등 NVM Command Set Spec 위임 항목 |
| §3.1.4 optional 레지스터 | CMBLOC, CMBSZ, BPRSEL 등 조건부 shall |
