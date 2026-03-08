# NVMe Base Specification 2.2 — 기능 분류 체계

> **대상**: I/O Controller (PCIe SSD) + Admin Controller  
> **기준**: 호스트가 컨트롤러에게 요구하는 기능의 목적 단위  
> **출처**: NVM Express® Base Specification, Revision 2.2 (2025.03.11 Ratified)

---

## 분류 판단 기준 (Classification Rules)

| Level 1 | 판단 기준 한 줄 요약 |
|---|---|
| 1. 식별 및 기능 협상 | 통신 시작 전 "상대방이 무엇을 할 수 있나" 파악 |
| 2. 큐 및 명령어 처리 | 명령어를 주고받는 채널 자체를 관리 |
| 3. 데이터 입출력 | 실제 사용자 데이터를 읽고 씀 (I/O Controller only) |
| 4. 네임스페이스 관리 | 논리적 저장 공간의 생성·삭제·구성 |
| 5. 상태 모니터링 및 로그 | 장치의 현재·과거 상태를 관찰 |
| 6. 전원 및 열 관리 | 전력 소비와 온도를 제어 |
| 7. 보안 및 데이터 삭제 | 데이터 접근 제어 + 안전한 소거 |
| 8. 데이터 무결성 및 보호 | 저장된 데이터가 손상되지 않도록 보장 |
| 9. 펌웨어 관리 | 장치 소프트웨어 갱신 |
| 10. 가상화 및 리소스 관리 | 물리 리소스를 논리적으로 분할·할당 (Admin Controller 중심) |

> **범례**  
> `[M]` Mandatory (I/O Controller 기준) · `[O]` Optional · `[A]` Admin Controller only  
> 명령어 뒤 괄호는 spec 위치 (섹션 번호 또는 Feature ID)

---

## 1. 식별 및 기능 협상 (Identification & Capability Negotiation)

컨트롤러·네임스페이스·서브시스템이 무엇을 지원하는지 파악하고,  
호스트-컨트롤러 간 동작 파라미터를 협상하는 기능 묶음.

### 1.1 컨트롤러 초기화 및 속성 설정

| 기능 | 관련 명령어 / 속성 | 구분 |
|---|---|---|
| 컨트롤러 활성화 및 준비 확인 | CC.EN, CSTS.RDY (§3.5) | [M] |
| 컨트롤러 기능 레지스터 파싱 | CAP (§3.1.4.1) | [M] |
| Controller Ready Mode 선택 | CC.CRIME, CAP.CRMS, CRTO (§3.5.3~4) | [M] |
| 지원 I/O Command Set 협상 | CAP.CSS, CC.CSS (§3.5.1) | [M] |
| 컨트롤러 리셋 처리 | CC.EN=0, NSSR (§3.7) | [M] |
| NVM 서브시스템 셧다운 | CC.SHN, CSTS.SHST, NSSD (§3.6) | [M] |

### 1.2 Identify 명령어

| 기능 | CNS 값 | 구분 |
|---|---|---|
| Identify Controller (I/O Command Set Independent) | CNS 01h (§5.1.13) | [M] |
| Identify Namespace (NVM Command Set) | CNS 00h | [M] |
| Identify Active Namespace ID List | CNS 02h | [M] |
| Identify Namespace ID List (Allocated) | CNS 10h | [O] |
| Identify Controller List (Attached) | CNS 12h | [O] |
| Identify Controller List (NVM Subsystem) | CNS 13h | [O] |
| Identify Primary Controller Capabilities | CNS 14h | [O] |
| Identify Secondary Controller List | CNS 15h | [O] |
| Identify Namespace Granularity List | CNS 16h | [O] |
| Identify UUID List | CNS 17h | [O] |
| Identify Domain List | CNS 1Bh | [O] |
| Identify Endurance Group List | CNS 1Ch (→ I/O Command Set 식별) | [O] |
| Identify I/O Command Set data structure | CNS 1Ch | [O] |
| Identify I/O CS specific Namespace | CNS 05h, 06h | [O] |
| Identify I/O CS specific Controller | CNS 06h | [O] |
| Identify I/O CS Independent Namespace | CNS 08h | [O] |

### 1.3 Host Behavior / Profile 협상 Features

| 기능 | Feature ID | 구분 |
|---|---|---|
| I/O Command Set Profile 선택 | FID 19h (§5.1.25.1.18) | [O] |
| Host Behavior Support | FID 16h (§5.1.25.1.15) | [O] |
| Enhanced Controller Metadata | FID 7Dh | [O] |
| Controller Metadata | FID 7Eh | [O] |
| Namespace Metadata | FID 7Fh | [O] |
| Host Identifier 등록 | FID 81h (§5.1.25.1.22) | [O] |
| Software Progress Marker | FID 80h (§5.1.25.1.21) | [O] |

---

## 2. 큐 및 명령어 처리 (Queue & Command Management)

호스트-컨트롤러 간 명령어 전달 채널을 설정하고 운영하는 기능 묶음.

### 2.1 큐 생성 및 삭제 (PCIe)

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| Admin Queue 설정 | AQA, ASQ, ACQ 레지스터 (§3.5.1) | [M] |
| I/O Completion Queue 생성 | Create I/O Completion Queue (§5.2.1) | [M] |
| I/O Submission Queue 생성 | Create I/O Submission Queue (§5.2.2) | [M] |
| I/O Completion Queue 삭제 | Delete I/O Completion Queue (§5.2.3) | [M] |
| I/O Submission Queue 삭제 | Delete I/O Submission Queue (§5.2.4) | [M] |
| Doorbell Buffer Config (Shadow Doorbell) | Doorbell Buffer Config (§5.2.5) | [O] |

### 2.2 명령어 중재 (Arbitration)

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Round Robin 중재 | CC.AMS, §3.4.4 | [M] |
| Weighted Round Robin + Urgent Priority 중재 | CC.AMS, §3.4.4 | [O] |
| Arbitration 설정 (Burst, WRR 가중치) | FID 01h (§5.1.25.1.1) | [M] |

### 2.3 명령어 제어

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| 명령어 중단 | Abort (§5.1.1) | [M] |
| I/O 명령어 취소 | Cancel (§7.1) | [O] |
| Fused Operation (두 명령어 원자적 실행) | FUSE 필드, §3.4.2 | [O] |
| Number of Queues 설정 | FID 07h (§5.1.25.1.7) | [M] |
| Interrupt Coalescing 설정 | FID 08h (§5.1.25.1.8) | [O] |
| Interrupt Vector Configuration | FID 09h (§5.1.25.1.9) | [O] |
| SQ Associations (SQ-NVM Set 연결) | §8.1.25 | [O] |
| Asynchronous Event Request | AER (§5.1.2) | [M] |
| Asynchronous Event Configuration | FID 0Bh (§5.1.25.1.11) | [O] |
| Keep Alive (연결 감시) | Keep Alive cmd, FID 0Fh, §3.9 | [O] |

### 2.4 데이터 전송 구조

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| PRP (Physical Region Page) 기반 전송 | §4.3.1 | [M] |
| SGL (Scatter Gather List) 기반 전송 | §4.3.2 | [O] |
| Controller Memory Buffer (CMB) | CMBLOC, CMBSZ, §8.2.1 | [O] |
| Host Memory Buffer (HMB) | FID 0Dh, §8.2.3 | [O] |

---

## 3. 데이터 입출력 (Data I/O)

> **I/O Controller 전용**. Admin Controller는 해당 없음.

실제 사용자 데이터를 읽고 쓰는 기능 묶음.  
NVM Command Set 등 I/O Command Set 명세에 정의되며,  
Base Spec은 공통 프레임워크만 정의한다.

### 3.1 기본 I/O 명령어 (NVM Command Set 기준)

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| 데이터 읽기 | Read (NVM CS) | [M] |
| 데이터 쓰기 | Write (NVM CS) | [M] |
| 쓰기 캐시 동기화 | Flush (§7.2) | [M] |
| Volatile Write Cache 제어 | FID 06h (§5.1.25.1.6) | [O] |

### 3.2 고급 I/O 기능

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Dataset Management (Deallocate/TRIM) | Dataset Management (NVM CS) | [O] |
| Compare (Read-Compare) | Compare (NVM CS) | [O] |
| Write Zeroes | Write Zeroes (NVM CS) | [O] |
| Write Uncorrectable | Write Uncorrectable (NVM CS) | [O] |
| I/O Management Receive (Reclaim Unit Handle 상태 조회) | §7.3 | [O] |
| I/O Management Send (Reclaim Unit Handle 업데이트) | §7.4 | [O] |
| Directives (스트림 힌트 등) | Directive Send/Receive (§5.1.6, §5.1.7), §8.1.8 | [O] |
| Flexible Data Placement (FDP) | FID 1Dh, 1Eh, §8.1.10 | [O] |
| Host-Initiated Refresh Operation | §8.1.11 | [O] |
| Read Recovery Level | FID (NVM CS), §8.1.20 | [O] |

---

## 4. 네임스페이스 관리 (Namespace Management)

논리적 저장 공간(Namespace, NVM Set, Endurance Group, Domain)의  
생성·삭제·구성·할당을 다루는 기능 묶음.

### 4.1 네임스페이스 생성·삭제·연결

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| Namespace 생성 / 삭제 | Namespace Management (§5.1.18, §8.1.15) | [O] |
| Namespace 컨트롤러 연결 / 해제 | Namespace Attachment (§5.1.19) | [O] |
| Namespace Write Protection 설정 | FID 84h, §8.1.16 | [O] |
| Format NVM (LBA format 변경 포함) | Format NVM (§5.1.10) | [O] |

### 4.2 NVM Set / Endurance Group / Domain 관리

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| NVM Set / Endurance Group / Domain 생성·삭제 | Capacity Management (§5.1.3, §8.1.4) | [O] |
| Endurance Group Event Configuration 설정 | FID 18h (§5.1.25.1.17) | [O] |
| Supported Capacity Configuration List 조회 | Get Log Page LID 1Bh (§5.1.12.1.14) | [O] |
| Media Unit Status 조회 | Get Log Page LID 1Ah (§5.1.12.1.13) | [O] |
| Spinup Control | FID 1Ah (§5.1.25.1.19) | [O] |

### 4.3 Reservations (다중 호스트 네임스페이스 접근 제어)

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| Reservation 등록 | Reservation Register (§7.6) | [O] |
| Reservation 획득 | Reservation Acquire (§7.5) | [O] |
| Reservation 해제 | Reservation Release (§7.7) | [O] |
| Reservation 상태 조회 | Reservation Report (§7.8) | [O] |
| Reservation Notification Mask 설정 | FID 82h (§5.1.25.1.23) | [O] |
| Reservation Persistence 설정 | FID 83h (§5.1.25.1.24) | [O] |
| Reservation Notification Log 조회 | Get Log Page LID 0Dh (§5.1.12.1.9) | [O] |

### 4.4 Dispersed Namespaces / Boot Partition

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Dispersed Namespace 구성 | §8.1.9 | [O] |
| Boot Partition 읽기 / 쓰기 | BPINFO, BPRSEL, BPMBL 레지스터, §8.1.3 | [O] |
| Boot Partition Write Protection | FID 85h (§5.1.25.1.26) | [O] |
| Admin Label (Namespace) | FID 1Fh | [O] |

---

## 5. 상태 모니터링 및 로그 (Monitoring & Logging)

장치의 현재 상태, 이력, 이벤트를 관찰하는 기능 묶음.  
**검증 시나리오 설계 시**: Sanitize, Format NVM 등 다른 분류의 기능 검증에도  
이 분류의 Log Page / AER을 함께 사용한다.

### 5.1 Get Log Page — 필수 / 공통 로그

| 로그 이름 | LID | 구분 |
|---|---|---|
| Supported Log Pages | 00h (§5.1.12.1.1) | [M] |
| Error Information | 01h (§5.1.12.1.2) | [M] |
| SMART / Health Information | 02h (§5.1.12.1.3) | [M] |
| Firmware Slot Information | 03h (§5.1.12.1.4) | [M] |
| Commands Supported and Effects | 05h (§5.1.12.1.6) | [O] |
| Feature Identifiers Supported and Effects | 12h (§5.1.12.1.18) | [O] |
| Persistent Event Log | 0Dh (§5.1.12.1.8) | [O] |

### 5.2 Get Log Page — 자가 진단 / 진단 로그

| 로그 이름 | LID | 구분 |
|---|---|---|
| Device Self-test | 06h (§5.1.12.1.7) | [O] |
| Telemetry Host-Initiated | 07h (§5.1.12.1.7) | [O] |
| Telemetry Controller-Initiated | 08h (§5.1.12.1.7) | [O] |
| Rotational Media Information | 16h (§5.1.12.1.21) | [O] |

### 5.3 Get Log Page — 용량 / 내구성 로그

| 로그 이름 | LID | 구분 |
|---|---|---|
| Endurance Group Information | 09h (§5.1.12.1.10) | [O] |
| Endurance Group Event Aggregate | 0Fh (§5.1.12.1.11) | [O] |
| Predictable Latency Per NVM Set | 0Ah (§5.1.12.1.11) | [O] |
| Predictable Latency Event Aggregate | 0Bh (§5.1.12.1.12) | [O] |
| Media Unit Status | 1Ah (§5.1.12.1.13) | [O] |
| Supported Capacity Configuration List | 1Bh (§5.1.12.1.14) | [O] |

### 5.4 Get Log Page — 접근 / 경로 로그

| 로그 이름 | LID | 구분 |
|---|---|---|
| Asymmetric Namespace Access (ANA) | 0Ch (§5.1.12.1.7) | [O] |
| LBA Status Information | 0Eh (§5.1.12.1.10) | [O] |
| Command and Feature Lockdown | 13h (§5.1.12.1.19) | [O] |
| FDP Configurations | 20h (§5.1.12.1.22) | [O] |
| FDP Usage Statistics | 21h (§5.1.12.1.23) | [O] |
| FDP Events | 22h (§5.1.12.1.24) | [O] |
| Reachability Groups | 17h (§5.1.12.1) | [O] |
| Reachability Associations | 18h (§5.1.12.1) | [O] |

### 5.5 비동기 이벤트 (AER)

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Asynchronous Event Request 등록 | AER (§5.1.2) | [M] |
| Error Status 이벤트 수신 | §5.1.2 | [M] |
| SMART / Health Status 이벤트 수신 | §5.1.2 | [O] |
| Notice 이벤트 수신 (NS 변경, FW 활성화 등) | §5.1.2 | [O] |
| I/O Command Set 특정 이벤트 수신 | §5.1.2 | [O] |
| AER Configuration 설정 | FID 0Bh (§5.1.25.1.11) | [O] |

### 5.6 자가 진단 명령어

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| Device Self-test 실행 (Short/Extended) | Device Self-test (§5.1.5, §8.1.7) | [O] |
| Timestamp 설정 / 조회 | FID 0Eh (§5.1.25.1.13) | [O] |
| Telemetry 데이터 수집 | Telemetry Host-Initiated log, §8.1.26 | [O] |
| NVMe-MI Receive / Send | §5.1.20, §5.1.21 | [O] |
| Reachability Reporting | §8.1.19 | [O] |

---

## 6. 전원 및 열 관리 (Power & Thermal Management)

전력 소비를 줄이고 열을 제어하는 기능 묶음.

### 6.1 전원 상태 관리

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Power State 전환 (수동) | FID 02h (§5.1.25.1.2) | [M] |
| Autonomous Power State Transition (APST) | FID 0Ch (§5.1.25.1.12) | [O] |
| Non-Operational Power State Config | FID 11h (§5.1.25.1.16) | [O] |
| Power State Descriptor (Identify Controller) | NPSS, PSD (§5.1.13) | [M] |
| Runtime D3 (RTD3) 진입 / 복귀 | RTD3R, RTD3E (§5.1.13) | [O] |
| Power Loss Signaling | FID 1Bh, §8.2.5 | [O] |
| Spinup Control (미디어 스핀업) | FID 1Ah (§5.1.25.1.19) | [O] |

### 6.2 열 관리

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Temperature Threshold 설정 | FID 04h (§5.1.25.1.3) | [M] |
| Temperature Threshold Hysteresis | FID 04h (§5.1.25.1.3) | [O] |
| Host Controlled Thermal Management (HCTM) | FID 10h (§5.1.25.1.14) | [O] |
| SMART 온도 모니터링 | Get Log Page LID 02h | [M] |

### 6.3 지연 시간 예측 모드

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Predictable Latency Mode Config | FID 13h (§5.1.25.1.17) | [O] |
| Predictable Latency Mode Window | FID 14h (§5.1.25.1.17) | [O] |
| Predictable Latency Per NVM Set Log | Get Log Page LID 0Ah | [O] |

---

## 7. 보안 및 데이터 삭제 (Security & Sanitization)

데이터에 대한 접근을 제어하고 안전하게 소거하는 기능 묶음.

### 7.1 TCG / 보안 프로토콜

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| 보안 프로토콜 데이터 수신 (TCG 등) | Security Receive (§5.1.22) | [O] |
| 보안 프로토콜 데이터 전송 (TCG 등) | Security Send (§5.1.23) | [O] |
| RPMB (Replay Protected Memory Block) | Security Send/Receive + §8.1.21 | [O] |

### 7.2 Sanitize (보안 삭제)

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Sanitize 실행 (Block Erase / Overwrite / Crypto Erase / Exit Failure) | Sanitize (§5.1.22, §8.1.22) | [O] |
| Sanitize Config (No-Deallocate 정책) | FID 17h (§5.1.25.1.15) | [O] |
| Sanitize 지원 여부 확인 | Identify Controller (SANICAP) | [O] |
| Sanitize 진행 상태 확인 | Get Log Page LID 02h (SMART, SSTAT 필드) | [O] |
| Sanitize 이벤트 수신 | AER Notice (Event 09h, 0Ah) | [O] |

> **검증 시나리오 구성 예시**  
> Sanitize 검증 = Identify(SANICAP 확인) → Sanitize 명령 실행 → Get Log Page(SMART, SSTAT 폴링) → AER 수신 확인 → Identify(용량 확인)

### 7.3 명령어 / 기능 잠금 (Lockdown)

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| 명령어 / Feature 실행 금지 설정 | Lockdown (§5.1.16) | [O] |
| Command and Feature Lockdown Log | Get Log Page LID 13h (§5.1.12.1.19) | [O] |

### 7.4 Key Per I/O

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| I/O 명령어별 암호화 키 지정 | Key Per I/O (§8.1.13) | [O] |

---

## 8. 데이터 무결성 및 보호 (Data Integrity & Protection)

저장된 데이터가 손상되지 않도록 보장하는 기능 묶음.

### 8.1 End-to-End 데이터 보호 (PI)

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Protection Information (Type 1/2/3) 지원 | Identify Namespace (DPS 필드), NVM CS | [O] |
| Guard Check / Reference Tag Check / Application Tag Check | NVM CS Read/Write 명령어 | [O] |

### 8.2 에러 복구 및 처리

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Error Recovery 설정 (DULBE, TLER) | FID (NVM CS), §9 | [O] |
| Media and Data Error 처리 | §9.2 | [M] |
| Controller Fatal Status 처리 | CSTS.CFS, §9.5 | [M] |
| Communication Loss 처리 | §9.6 | [M] |
| LBA Status Information Log | Get Log Page LID 0Eh | [O] |
| Read Recovery Level | FID (NVM CS), §8.1.20 | [O] |

### 8.3 Atomic / Fused 동작 무결성

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Atomic Write 단위 보장 | AWUN, AWUPF (Identify Controller), NVM CS | [O] |
| Fused Operation (Compare-and-Write) | FUSE 필드, §3.4.2 | [O] |

### 8.4 Persistent Memory Region (PMR)

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| PMR 활성화 및 사용 | PMRCAP, PMRCTL, PMRSTS, §8.2.4 | [O] |

---

## 9. 펌웨어 관리 (Firmware Management)

장치 소프트웨어를 갱신하는 기능 묶음.

### 9.1 펌웨어 업데이트 프로세스

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| 펌웨어 이미지 다운로드 | Firmware Image Download (§5.1.9) | [O] |
| 펌웨어 슬롯 커밋 및 활성화 | Firmware Commit (§5.1.8, §3.11) | [O] |
| 펌웨어 슬롯 정보 조회 | Get Log Page LID 03h (§5.1.12.1.4) | [O] |
| 펌웨어 활성화 이벤트 수신 | AER Notice (Firmware Activation Starting) | [O] |

### 9.2 Boot Partition 펌웨어

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Boot Partition 이미지 쓰기 | Boot Partition Write (§8.1.3) | [O] |
| Boot Partition 이미지 읽기 | Boot Partition Read (§8.1.3) | [O] |
| Boot Partition Write Protection | FID 85h (§5.1.25.1.26) | [O] |

---

## 10. 가상화 및 리소스 관리 (Virtualization & Resource Management)

> Admin Controller 중심 기능. I/O Controller는 일부만 해당.

물리 리소스를 논리적으로 분할·할당하고, 라이브 마이그레이션 등  
고급 인프라 운영을 지원하는 기능 묶음.

### 10.1 SR-IOV / 가상화 (PCIe)

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| Primary / Secondary Controller 관리 | Virtualization Management (§5.2.6, §8.2.6) | [A] |
| Secondary Controller 리소스 할당 (VQ, VI) | Virtualization Management | [A] |
| Secondary Controller 활성화 / 비활성화 | Virtualization Management | [A] |

### 10.2 Controller Data Queue (CDQ)

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| Controller Data Queue 생성 / 삭제 | Controller Data Queue (§5.1.4, §8.1.6) | [O] |
| CDQ 이벤트 수신 | AER (CDQ Tail Pointer 이벤트) | [O] |
| CDQ 설정 | FID 21h (§5.1.25.1.20) | [O] |

### 10.3 Host Managed Live Migration

| 기능 | 관련 명령어 | 구분 |
|---|---|---|
| Migration 데이터 수신 | Migration Receive (§5.1.17, §8.1.12) | [O] |
| Migration 데이터 전송 | Migration Send (§5.1.17, §8.1.12) | [O] |
| Migration 진행 추적 | Track Receive / Track Send (§5.1.27, §5.1.28) | [O] |

### 10.4 Management Addresses

| 기능 | 관련 내용 | 구분 |
|---|---|---|
| Embedded Management Controller Address | FID 78h, §8.1.14 | [O] |
| Host Management Agent Address | FID 79h, §8.1.14 | [O] |

---

## 부록: 분류 경계 결정 사항 (Boundary Decisions)

애매한 기능들에 대한 귀속 판단을 명시해 새로운 기능 추가 시 일관성을 유지한다.

| 기능 | 귀속 분류 | 판단 근거 |
|---|---|---|
| Format NVM | **4. 네임스페이스 관리** | LBA format 변경이 주 목적; 보안 삭제 목적일 때는 7번과 cross-ref |
| Sanitize Status 확인 (Get Log) | **7. 보안 및 데이터 삭제** (검증 시나리오 내 포함) | Sanitize 검증 시나리오의 일부이므로 7번 범위로 묶음; 로그 명령 자체는 5번 |
| Device Self-test | **5. 상태 모니터링 및 로그** | 실행 목적이 "장치 상태 진단"이므로 모니터링 범주 |
| Reservations | **4. 네임스페이스 관리** | Namespace에 종속된 속성; 접근 제어가 목적이더라도 Namespace 속성으로 분류 |
| Keep Alive | **2. 큐 및 명령어 처리** | 연결 감시는 통신 채널 관리의 일부 |
| Error Recovery Feature | **8. 데이터 무결성 및 보호** | 데이터 손상 방지가 목적 |
| Persistent Event Log | **5. 상태 모니터링 및 로그** | 이력 관찰 목적 |
| Predictable Latency Mode | **6. 전원 및 열 관리** | QoS/레이턴시 제어는 성능 vs 전력 트레이드오프 관리의 일부 |
| Boot Partition | **4. 네임스페이스 관리** (저장 공간 측면) / **9. 펌웨어 관리** (이미지 측면) | 저장 공간 할당은 4번, 이미지 내용은 9번으로 분리 |
| ANA (Asymmetric Namespace Access) | **5. 상태 모니터링 및 로그** | 경로 상태 관찰이 목적 |
