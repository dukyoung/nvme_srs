# NVMe Requirement Management Tool — 설계 문서

> **대상 독자**: Claude Code에 이 문서를 전달하여 구현을 시작하는 용도  
> **프로젝트 목적**: NVMe Base Spec 2.2 기반 요구사항(REQ) 관리, 당사 제품 지원 범위 기입, TestCase 연결 및 커버리지 추적  
> **팀 규모**: 개발자 10명, 로컬 네트워크 공유  

---

## 1. 기술 스택

| 레이어 | 기술 | 비고 |
|--------|------|------|
| 백엔드 | **FastAPI** + **SQLAlchemy** (async) | Python 3.11+ |
| DB | **SQLite** (단일 파일) | `nvme_req.db` |
| 실시간 | **FastAPI WebSocket** | 편집 중 사용자 표시, 저장 알림 |
| 프론트엔드 | **React 18** + **Vite** | TypeScript |
| UI 테이블 | **TanStack Table v8** | 인라인 편집, 필터, 정렬 |
| 상태관리 | **Zustand** | 전역 필터/선택 상태 |
| HTTP | **Axios** + **React Query** | 캐싱, 낙관적 업데이트 |
| 스타일 | **Tailwind CSS** | |

---

## 2. 디렉터리 구조

```
nvme-reqtool/
├── backend/
│   ├── main.py                  # FastAPI 앱 진입점, CORS, WebSocket
│   ├── database.py              # SQLAlchemy 엔진, 세션
│   ├── models.py                # ORM 모델 (Requirement, TestCase, ...)
│   ├── schemas.py               # Pydantic 스키마 (요청/응답)
│   ├── crud.py                  # DB CRUD 함수
│   ├── routers/
│   │   ├── requirements.py      # /api/requirements
│   │   ├── testcases.py         # /api/testcases
│   │   ├── coverage.py          # /api/coverage
│   │   └── ws.py                # WebSocket /ws
│   ├── seed_data.py             # 초기 REQ 데이터 임포트 (CSV/JSON)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── RequirementsPage.tsx   # REQ 목록 + 인라인 편집
│   │   │   ├── TestCasesPage.tsx      # TC 목록
│   │   │   └── CoveragePage.tsx       # 커버리지 대시보드
│   │   ├── components/
│   │   │   ├── ReqTable.tsx           # TanStack Table 기반 REQ 테이블
│   │   │   ├── ReqEditModal.tsx       # REQ 상세 편집 모달
│   │   │   ├── TcLinkPanel.tsx        # REQ ↔ TC 연결 패널
│   │   │   ├── CoverageBar.tsx        # 커버리지 시각화
│   │   │   └── ActiveEditors.tsx      # 현재 편집 중인 사용자 표시
│   │   ├── hooks/
│   │   │   ├── useRequirements.ts
│   │   │   ├── useTestCases.ts
│   │   │   └── useWebSocket.ts
│   │   ├── store/
│   │   │   └── filterStore.ts         # Zustand 필터 상태
│   │   └── types/
│   │       └── index.ts               # 공유 타입 정의
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│   └── nvme_req_01_identification.csv  # 초기 데이터 (기존 MD에서 변환)
│
├── run.sh          # 백/프론트 동시 실행 스크립트
└── README.md
```

---

## 3. DB 스키마

### 3.1 `requirement` 테이블

```sql
CREATE TABLE requirement (
    id          TEXT PRIMARY KEY,   -- REQ-IDENT-CTRL-001
    category    TEXT NOT NULL,      -- CTRL / PROP / CMD / LOG / FTR / IDFY / IOSC / INIT
    level1      TEXT NOT NULL,      -- 분류 1: 식별 및 기능 협상
    spec_section TEXT,              -- §3.1.2, Figure 313 등
    spec_text   TEXT NOT NULL,      -- 원문 shall 문장 (영문)
    spec_text_ko TEXT,              -- 한국어 번역
    keyword     TEXT,               -- 핵심 키워드
    controller_type TEXT,           -- IO / ADMIN / BOTH
    mandatory   TEXT DEFAULT 'M',   -- M / O / C (조건부)

    -- 당사 제품 관련 필드
    support_status  TEXT DEFAULT 'UNKNOWN',
    -- SUPPORTED     : 완전 구현
    -- PARTIAL       : 부분 구현 (note에 상세)
    -- NOT_SUPPORTED : 미구현
    -- N_A           : 해당 없음
    -- UNKNOWN       : 미검토

    support_note    TEXT,           -- 구현 상세, 제한사항, 관련 코드 위치 등
    fw_version      TEXT,           -- 지원 시작 FW 버전

    -- 관리 필드
    status      TEXT DEFAULT 'OPEN',  -- OPEN / LINKED / VERIFIED
    priority    TEXT DEFAULT 'NORMAL', -- HIGH / NORMAL / LOW
    assigned_to TEXT,               -- 담당자
    created_at  TEXT DEFAULT (datetime('now')),
    updated_at  TEXT DEFAULT (datetime('now'))
);
```

### 3.2 `test_case` 테이블

```sql
CREATE TABLE test_case (
    id          TEXT PRIMARY KEY,   -- TC-IDENT-001
    title       TEXT NOT NULL,
    description TEXT,
    precondition TEXT,
    steps       TEXT,               -- JSON 배열
    expected    TEXT,
    category    TEXT,
    status      TEXT DEFAULT 'DRAFT', -- DRAFT / READY / PASS / FAIL / SKIP
    assigned_to TEXT,
    created_at  TEXT DEFAULT (datetime('now')),
    updated_at  TEXT DEFAULT (datetime('now'))
);
```

### 3.3 `requirement_testcase` 테이블 (다대다)

```sql
CREATE TABLE requirement_testcase (
    req_id  TEXT REFERENCES requirement(id) ON DELETE CASCADE,
    tc_id   TEXT REFERENCES test_case(id) ON DELETE CASCADE,
    PRIMARY KEY (req_id, tc_id)
);
```

### 3.4 `edit_session` 테이블 (실시간 편집 충돌 방지)

```sql
CREATE TABLE edit_session (
    req_id      TEXT PRIMARY KEY,
    username    TEXT,
    started_at  TEXT
);
```

---

## 4. API 엔드포인트

### 4.1 Requirements

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/requirements` | 목록 조회 (필터: category, status, support_status, keyword) |
| GET | `/api/requirements/{id}` | 단건 조회 |
| POST | `/api/requirements` | 신규 추가 |
| PATCH | `/api/requirements/{id}` | 부분 수정 (인라인 편집용) |
| DELETE | `/api/requirements/{id}` | 삭제 |
| POST | `/api/requirements/import` | CSV/JSON 일괄 임포트 |
| GET | `/api/requirements/export` | CSV 내보내기 |

### 4.2 TestCases

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/testcases` | 목록 조회 |
| POST | `/api/testcases` | 생성 |
| PATCH | `/api/testcases/{id}` | 수정 |
| DELETE | `/api/testcases/{id}` | 삭제 |
| POST | `/api/requirements/{id}/testcases` | REQ에 TC 연결 |
| DELETE | `/api/requirements/{req_id}/testcases/{tc_id}` | 연결 해제 |

### 4.3 Coverage

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/coverage/summary` | 전체 커버리지 요약 |
| GET | `/api/coverage/by-category` | 카테고리별 커버리지 |
| GET | `/api/coverage/uncovered` | TC 미연결 REQ 목록 |
| GET | `/api/coverage/support-status` | 지원 범위 현황 집계 |

### 4.4 WebSocket

```
WS /ws?username={name}
```

**메시지 타입:**

```json
// 클라이언트 → 서버: 편집 시작
{ "type": "EDITING_START", "req_id": "REQ-IDENT-CTRL-001" }

// 클라이언트 → 서버: 편집 종료
{ "type": "EDITING_END", "req_id": "REQ-IDENT-CTRL-001" }

// 서버 → 모든 클라이언트: 변경 알림
{ "type": "REQ_UPDATED", "req_id": "REQ-IDENT-CTRL-001", "updated_by": "덕용" }

// 서버 → 모든 클라이언트: 현재 편집 중인 사용자 목록
{ "type": "ACTIVE_EDITORS", "editors": { "REQ-IDENT-CTRL-001": "김철수" } }
```

---

## 5. 프론트엔드 화면 설계

### 5.1 REQ 목록 페이지 (`/requirements`)

```
┌──────────────────────────────────────────────────────┐
│  NVMe Requirement Manager          [+ 추가] [↑ 가져오기] [↓ 내보내기]  │
├──────────────────────────────────────────────────────┤
│  필터: [카테고리 ▼] [지원상태 ▼] [담당자 ▼] [🔍 검색...]              │
│  정렬: REQ-ID ↑  | 미검토 23개 | 미커버 31개                          │
├──────────┬──────┬─────────────────┬──────────┬───────┤
│ REQ-ID   │ 분류 │ spec_text (요약) │ 지원상태 │ TC수  │
├──────────┼──────┼─────────────────┼──────────┼───────┤
│ CTRL-001 │ CTRL │ 컨트롤러는 shall │ ✅ 완전  │  2    │ ← 클릭 → 모달
│ CTRL-002 │ CTRL │ reserved 비트는  │ ⚠️ 부분  │  1    │
│ PROP-001 │ PROP │ CAP 레지스터는   │ ❓ 미검토 │  0    │ ← 빨간 하이라이트
└──────────┴──────┴─────────────────┴──────────┴───────┘
  👤 김철수가 PROP-003 편집 중...
```

**인라인 편집**: `지원상태`, `담당자`, `우선순위` 는 셀 클릭으로 바로 수정  
**상세 편집**: REQ-ID 클릭 → 모달에서 `spec_text`, `support_note`, `TC 연결` 관리

### 5.2 커버리지 대시보드 (`/coverage`)

```
┌─────────────────────────────────────────────────────┐
│  커버리지 현황                                        │
├─────────────────────────────────────────────────────┤
│  전체 REQ: 75개   TC 연결됨: 44개 (59%)  ██████░░░░ │
│  지원 완전: 31개  부분: 12개  미검토: 23개  미지원: 9개│
├──────────────────────────────────────────────────────┤
│  카테고리별                                           │
│  CTRL ████████░░ 80%  (4/5)                          │
│  PROP ██████░░░░ 60%  (15/25)                        │
│  CMD  ████░░░░░░ 40%  (4/11)                         │
│  ...                                                  │
├──────────────────────────────────────────────────────┤
│  ⚠️ TC 미연결 REQ (31개)   [TC 연결하러 가기 →]      │
│  REQ-IDENT-PROP-003  CAP.CSS 비트 설정 shall...      │
│  REQ-IDENT-CMD-007   Get Log Page mandatory...        │
└──────────────────────────────────────────────────────┘
```

### 5.3 REQ 상세 편집 모달

```
┌─────────────────────────────────────────────────────┐
│  REQ-IDENT-CTRL-001                          [✕ 닫기] │
├─────────────────────────────────────────────────────┤
│  [Spec 원문]                                          │
│  The controller shall support both Static and        │
│  Dynamic controller models.                          │
│                                                       │
│  [한국어]  컨트롤러는 Static 및 Dynamic 컨트롤러 모델 │
│            을 모두 지원해야 한다.                     │
│                                                       │
│  Spec 섹션: §3.1.3    컨트롤러 타입: BOTH            │
│  필수 여부: M (Mandatory)                             │
├─────────────────────────────────────────────────────┤
│  [당사 지원 범위]                                     │
│  지원 상태: [✅ 완전 지원        ▼]                   │
│  FW 버전:   [v2.1.0              ]                    │
│  메모:      [Static/Dynamic 모두 구현. 관련 코드:     │
│              ctrl_init.c:234     ]                    │
├─────────────────────────────────────────────────────┤
│  [연결된 TestCase]                                    │
│  TC-IDENT-001  컨트롤러 모델 타입 확인    ✅ PASS     │
│  TC-IDENT-002  Static→Dynamic 전환 테스트 📋 READY   │
│  [+ TC 연결 추가]                                     │
├─────────────────────────────────────────────────────┤
│  담당자: 덕용  우선순위: HIGH   [저장]  [삭제]        │
└─────────────────────────────────────────────────────┘
```

---

## 6. 실행 방법

### 6.1 설치

```bash
# 백엔드
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 프론트엔드
cd frontend
npm install
```

### 6.2 초기 데이터 로드

```bash
# 기존 nvme_req_01_identification.md의 REQ 75개를 CSV로 변환 후 임포트
cd backend
python seed_data.py --input ../data/nvme_req_01_identification.csv
```

### 6.3 실행

```bash
# 백엔드 (포트 8000)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 프론트엔드 (포트 5173)
cd frontend
npm run dev

# 또는 한번에 (run.sh)
./run.sh
```

### 6.4 팀원 접속

```
# 호스트 PC의 로컬 IP 확인 후 팀원에게 공유
http://192.168.x.x:5173
```

---

## 7. Claude Code 구현 순서 (권장)

Claude Code에 이 문서를 전달한 후 아래 순서로 구현을 요청하세요.

```
1단계: 프로젝트 초기화
  "nvme-reqtool 디렉터리 구조를 만들고, backend requirements.txt와
   frontend package.json을 생성해줘."

2단계: 백엔드 기반
  "database.py, models.py, schemas.py를 설계 문서 스키마대로 구현해줘."

3단계: API 라우터
  "requirements.py 라우터를 만들어줘. CRUD + CSV 임포트/내보내기 포함."

4단계: WebSocket
  "ws.py WebSocket 라우터를 만들어줘. 편집 중 사용자 표시와
   변경 브로드캐스트 기능 포함."

5단계: 프론트 기반
  "React + Vite + TanStack Table 기반 ReqTable 컴포넌트를 만들어줘.
   인라인 편집(지원상태, 담당자), 필터, 정렬 포함."

6단계: 모달 + TC 연결
  "ReqEditModal과 TcLinkPanel 컴포넌트를 만들어줘."

7단계: 커버리지 대시보드
  "CoveragePage를 만들어줘. 카테고리별 바 차트와 미커버 REQ 목록 포함."

8단계: 시드 데이터
  "seed_data.py를 만들어줘. nvme_req_01_identification.md 파일을
   파싱해서 DB에 임포트하는 스크립트."
```

---

## 8. 향후 확장 포인트

- **HIL 시뮬레이터 연동**: TC 실행 결과를 REST API로 자동 업데이트 (`PATCH /api/testcases/{id}` status 필드)
- **Spec 버전 관리**: NVMe 2.3 등 신규 스펙 변경사항 diff 추적
- **REQ 자동 추출**: pdfplumber로 shall 문장 추출 → 미등록 REQ 제안 기능
- **보고서 출력**: 커버리지 현황을 PDF/Excel로 내보내기
