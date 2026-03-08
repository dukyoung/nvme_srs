import { useState, useRef } from 'react'
import { useRequirements, useImportRequirements } from '../hooks/useRequirements'
import { useFilterStore } from '../store/filterStore'
import ReqTable from '../components/ReqTable'
import ReqEditModal from '../components/ReqEditModal'
import ActiveEditors from '../components/ActiveEditors'
import type { Requirement, WsMessage } from '../types'
import { CATEGORY_OPTIONS } from '../types'

interface Props {
  editors: Record<string, string>
  sendWs: (msg: WsMessage) => void
}

export default function RequirementsPage({ editors, sendWs }: Props) {
  const { category, supportStatus, assignedTo, keyword, derivedFrom, setCategory, setSupportStatus, setAssignedTo, setKeyword, setDerivedFrom } =
    useFilterStore()

  const { data: requirements = [], isLoading } = useRequirements({
    category: category || undefined,
    support_status: supportStatus || undefined,
    assigned_to: assignedTo || undefined,
    keyword: keyword || undefined,
    derived_from: derivedFrom || undefined,
  })

  const importMut = useImportRequirements()
  const fileRef = useRef<HTMLInputElement>(null)
  const [selectedReqId, setSelectedReqId] = useState<string | null>(null)

  const unknownCount = requirements.filter((r) => r.support_status === 'UNKNOWN').length
  const uncoveredCount = requirements.filter((r) => r.tc_count === 0).length

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      importMut.mutate(file)
      e.target.value = ''
    }
  }

  const handleExport = () => {
    window.open('/api/requirements/export', '_blank')
  }

  return (
    <div>
      {/* Toolbar */}
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold">NVMe Requirement Manager</h1>
        <div className="flex gap-2">
          <input ref={fileRef} type="file" accept=".csv" className="hidden" onChange={handleImport} />
          <button
            className="px-3 py-1.5 text-sm border rounded hover:bg-gray-50"
            onClick={() => fileRef.current?.click()}
          >
            가져오기
          </button>
          <button className="px-3 py-1.5 text-sm border rounded hover:bg-gray-50" onClick={handleExport}>
            내보내기
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-3 mb-3">
        <select
          className="border rounded px-2 py-1 text-sm"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="">전체 카테고리</option>
          {CATEGORY_OPTIONS.map((c) => (
            <option key={c.value} value={c.value}>
              {c.label}
            </option>
          ))}
        </select>

        <select
          className="border rounded px-2 py-1 text-sm"
          value={supportStatus}
          onChange={(e) => setSupportStatus(e.target.value)}
        >
          <option value="">전체 지원상태</option>
          <option value="SUPPORTED">완전 지원</option>
          <option value="PARTIAL">부분 구현</option>
          <option value="NOT_SUPPORTED">미구현</option>
          <option value="N_A">해당 없음</option>
          <option value="UNKNOWN">미검토</option>
        </select>

        <input
          className="border rounded px-2 py-1 text-sm w-48"
          placeholder="검색 (ID, 본문, 키워드, 출처)..."
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />

        <input
          className="border rounded px-2 py-1 text-sm w-36"
          placeholder="출처 (§5.1.1...)"
          value={derivedFrom}
          onChange={(e) => setDerivedFrom(e.target.value)}
        />

        <input
          className="border rounded px-2 py-1 text-sm w-28"
          placeholder="담당자"
          value={assignedTo}
          onChange={(e) => setAssignedTo(e.target.value)}
        />

        <span className="text-sm text-gray-500 ml-auto">
          미검토 <span className="font-medium text-orange-600">{unknownCount}</span>개 | 미커버{' '}
          <span className="font-medium text-red-600">{uncoveredCount}</span>개 | 전체{' '}
          <span className="font-medium">{requirements.length}</span>개
        </span>
      </div>

      {/* Table */}
      {isLoading ? (
        <p className="text-gray-400">로딩 중...</p>
      ) : (
        <ReqTable data={requirements} onRowClick={(r) => setSelectedReqId(r.id)} editors={editors} />
      )}

      <ActiveEditors editors={editors} />

      {/* Modal */}
      {selectedReqId && (
        <ReqEditModal reqId={selectedReqId} onClose={() => setSelectedReqId(null)} onSendWs={sendWs} />
      )}
    </div>
  )
}
