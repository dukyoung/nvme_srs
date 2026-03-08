import { useState, useEffect } from 'react'
import { useRequirement, useUpdateRequirement, useDeleteRequirement } from '../hooks/useRequirements'
import { SUPPORT_STATUS_OPTIONS } from '../types'
import type { TestCase } from '../types'
import TcLinkPanel from './TcLinkPanel'

interface Props {
  reqId: string
  onClose: () => void
  onSendWs: (msg: { type: string; req_id: string }) => void
}

export default function ReqEditModal({ reqId, onClose, onSendWs }: Props) {
  const { data: req, isLoading } = useRequirement(reqId)
  const updateMut = useUpdateRequirement()
  const deleteMut = useDeleteRequirement()

  const [supportStatus, setSupportStatus] = useState('')
  const [supportNote, setSupportNote] = useState('')
  const [fwVersion, setFwVersion] = useState('')
  const [priority, setPriority] = useState('NORMAL')
  const [assignedTo, setAssignedTo] = useState('')

  useEffect(() => {
    if (req) {
      setSupportStatus(req.support_status || 'UNKNOWN')
      setSupportNote(req.support_note || '')
      setFwVersion(req.fw_version || '')
      setPriority(req.priority || 'NORMAL')
      setAssignedTo(req.assigned_to || '')
      onSendWs({ type: 'EDITING_START', req_id: reqId })
    }
    return () => {
      onSendWs({ type: 'EDITING_END', req_id: reqId })
    }
  }, [req?.id])

  if (isLoading || !req) {
    return (
      <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6">로딩 중...</div>
      </div>
    )
  }

  const handleSave = () => {
    updateMut.mutate(
      {
        id: reqId,
        update: {
          support_status: supportStatus,
          support_note: supportNote,
          fw_version: fwVersion,
          priority,
          assigned_to: assignedTo || undefined,
        },
      },
      {
        onSuccess: () => {
          onSendWs({ type: 'REQ_UPDATED', req_id: reqId })
          onClose()
        },
      },
    )
  }

  const handleDelete = () => {
    if (confirm(`${reqId}를 삭제하시겠습니까?`)) {
      deleteMut.mutate(reqId, { onSuccess: onClose })
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50" onClick={onClose}>
      <div
        className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto m-4"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b">
          <h2 className="text-lg font-bold font-mono">{req.id}</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-xl">
            &times;
          </button>
        </div>

        <div className="px-6 py-4 space-y-4">
          {/* Spec text */}
          <div>
            <label className="text-xs font-medium text-gray-500">Spec 원문</label>
            <p className="text-sm bg-gray-50 rounded p-2 mt-1">{req.spec_text}</p>
          </div>

          {req.spec_text_ko && (
            <div>
              <label className="text-xs font-medium text-gray-500">한국어</label>
              <p className="text-sm bg-gray-50 rounded p-2 mt-1">{req.spec_text_ko}</p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-gray-500">출처 (Derived From):</span>{' '}
              <span className="font-medium font-mono text-blue-700">{req.derived_from || '-'}</span>
            </div>
            <div>
              <span className="text-gray-500">Spec 섹션:</span>{' '}
              <span className="font-medium">{req.spec_section || '-'}</span>
            </div>
            <div>
              <span className="text-gray-500">컨트롤러 타입:</span>{' '}
              <span className="font-medium">{req.controller_type || '-'}</span>
            </div>
            <div>
              <span className="text-gray-500">필수 여부:</span>{' '}
              <span className="font-medium">{req.mandatory || '-'}</span>
            </div>
          </div>

          <hr />

          {/* Support section */}
          <div>
            <h3 className="text-sm font-semibold mb-2">당사 지원 범위</h3>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-gray-500">지원 상태</label>
                <select
                  className="w-full border rounded px-2 py-1 text-sm mt-1"
                  value={supportStatus}
                  onChange={(e) => setSupportStatus(e.target.value)}
                >
                  {SUPPORT_STATUS_OPTIONS.map((o) => (
                    <option key={o.value} value={o.value}>
                      {o.label}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-xs text-gray-500">FW 버전</label>
                <input
                  className="w-full border rounded px-2 py-1 text-sm mt-1"
                  value={fwVersion}
                  onChange={(e) => setFwVersion(e.target.value)}
                  placeholder="v2.1.0"
                />
              </div>
            </div>
            <div className="mt-2">
              <label className="text-xs text-gray-500">메모</label>
              <textarea
                className="w-full border rounded px-2 py-1 text-sm mt-1"
                rows={3}
                value={supportNote}
                onChange={(e) => setSupportNote(e.target.value)}
                placeholder="구현 상세, 제한사항, 관련 코드 위치 등"
              />
            </div>
          </div>

          <hr />

          {/* TestCase links */}
          <TcLinkPanel reqId={reqId} linkedTcs={(req as any).test_cases || []} />

          <hr />

          {/* Meta */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-gray-500">담당자</label>
              <input
                className="w-full border rounded px-2 py-1 text-sm mt-1"
                value={assignedTo}
                onChange={(e) => setAssignedTo(e.target.value)}
              />
            </div>
            <div>
              <label className="text-xs text-gray-500">우선순위</label>
              <select
                className="w-full border rounded px-2 py-1 text-sm mt-1"
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
              >
                <option value="HIGH">HIGH</option>
                <option value="NORMAL">NORMAL</option>
                <option value="LOW">LOW</option>
              </select>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-between px-6 py-4 border-t">
          <button
            onClick={handleDelete}
            className="px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded"
          >
            삭제
          </button>
          <div className="flex gap-2">
            <button onClick={onClose} className="px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded">
              취소
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              disabled={updateMut.isPending}
            >
              저장
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
