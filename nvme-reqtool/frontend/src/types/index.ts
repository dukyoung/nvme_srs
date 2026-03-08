export interface Requirement {
  id: string
  category: string
  level1: string
  derived_from: string | null
  spec_section: string | null
  spec_text: string
  spec_text_ko: string | null
  keyword: string | null
  controller_type: string | null
  mandatory: string | null
  support_status: string | null
  support_note: string | null
  fw_version: string | null
  status: string | null
  priority: string | null
  assigned_to: string | null
  created_at: string | null
  updated_at: string | null
  tc_count: number
}

export interface RequirementUpdate {
  category?: string
  level1?: string
  derived_from?: string
  spec_section?: string
  spec_text?: string
  spec_text_ko?: string
  keyword?: string
  controller_type?: string
  mandatory?: string
  support_status?: string
  support_note?: string
  fw_version?: string
  status?: string
  priority?: string
  assigned_to?: string
}

export interface TestCase {
  id: string
  title: string
  description: string | null
  precondition: string | null
  steps: string | null
  expected: string | null
  category: string | null
  status: string | null
  assigned_to: string | null
  created_at: string | null
  updated_at: string | null
}

export interface CoverageSummary {
  total_requirements: number
  linked_requirements: number
  coverage_percent: number
}

export interface CategoryCoverage {
  category: string
  total: number
  linked: number
  coverage_percent: number
}

export interface SupportStatusSummary {
  supported: number
  partial: number
  not_supported: number
  n_a: number
  unknown: number
}

export interface WsMessage {
  type: string
  req_id?: string
  updated_by?: string
  message?: string
  editors?: Record<string, string>
}

export const SUPPORT_STATUS_OPTIONS = [
  { value: 'SUPPORTED', label: '완전 지원', color: 'bg-green-100 text-green-800' },
  { value: 'PARTIAL', label: '부분 구현', color: 'bg-yellow-100 text-yellow-800' },
  { value: 'NOT_SUPPORTED', label: '미구현', color: 'bg-red-100 text-red-800' },
  { value: 'N_A', label: '해당 없음', color: 'bg-gray-100 text-gray-600' },
  { value: 'UNKNOWN', label: '미검토', color: 'bg-orange-100 text-orange-800' },
] as const

export const CATEGORY_OPTIONS = [
  { value: 'IDENT', label: '1. 식별 및 기능 협상' },
  { value: 'QUEUE', label: '2. 큐 및 명령어 처리' },
  { value: 'DATA_IO', label: '3. 데이터 입출력' },
  { value: 'NS_MGMT', label: '4. 네임스페이스 관리' },
  { value: 'MONITOR', label: '5. 상태 모니터링 및 로그' },
  { value: 'POWER', label: '6. 전원 및 열 관리' },
  { value: 'SECURITY', label: '7. 보안 및 데이터 삭제' },
  { value: 'INTEGRITY', label: '8. 데이터 무결성 및 보호' },
  { value: 'FW_MGMT', label: '9. 펌웨어 관리' },
  { value: 'VIRT', label: '10. 가상화 및 리소스 관리' },
] as const

export const CATEGORY_LABEL_MAP: Record<string, string> = Object.fromEntries(
  CATEGORY_OPTIONS.map((c) => [c.value, c.label]),
)

export const PRIORITY_OPTIONS = ['HIGH', 'NORMAL', 'LOW'] as const

export const TC_STATUS_OPTIONS = ['DRAFT', 'READY', 'PASS', 'FAIL', 'SKIP'] as const
