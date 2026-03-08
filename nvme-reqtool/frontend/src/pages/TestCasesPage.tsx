import { useState } from 'react'
import { useTestCases, useCreateTestCase, useUpdateTestCase } from '../hooks/useTestCases'
import type { TestCase } from '../types'
import { TC_STATUS_OPTIONS } from '../types'

export default function TestCasesPage() {
  const { data: testcases = [], isLoading } = useTestCases()
  const createMut = useCreateTestCase()
  const updateMut = useUpdateTestCase()
  const [showForm, setShowForm] = useState(false)
  const [newTc, setNewTc] = useState({ id: '', title: '', description: '', category: '' })

  const handleCreate = () => {
    if (!newTc.id || !newTc.title) return
    createMut.mutate(
      { id: newTc.id, title: newTc.title, description: newTc.description, category: newTc.category },
      {
        onSuccess: () => {
          setNewTc({ id: '', title: '', description: '', category: '' })
          setShowForm(false)
        },
      },
    )
  }

  const handleStatusChange = (tc: TestCase, status: string) => {
    updateMut.mutate({ id: tc.id, update: { status } })
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold">TestCase 관리</h1>
        <button
          className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={() => setShowForm(!showForm)}
        >
          + 추가
        </button>
      </div>

      {showForm && (
        <div className="border rounded p-4 mb-4 bg-gray-50 space-y-2">
          <div className="grid grid-cols-2 gap-3">
            <input
              className="border rounded px-2 py-1 text-sm"
              placeholder="TC ID (예: TC-IDENT-001)"
              value={newTc.id}
              onChange={(e) => setNewTc({ ...newTc, id: e.target.value })}
            />
            <input
              className="border rounded px-2 py-1 text-sm"
              placeholder="카테고리"
              value={newTc.category}
              onChange={(e) => setNewTc({ ...newTc, category: e.target.value })}
            />
          </div>
          <input
            className="border rounded px-2 py-1 text-sm w-full"
            placeholder="제목"
            value={newTc.title}
            onChange={(e) => setNewTc({ ...newTc, title: e.target.value })}
          />
          <textarea
            className="border rounded px-2 py-1 text-sm w-full"
            rows={2}
            placeholder="설명"
            value={newTc.description}
            onChange={(e) => setNewTc({ ...newTc, description: e.target.value })}
          />
          <div className="flex gap-2">
            <button className="px-3 py-1 text-sm bg-blue-600 text-white rounded" onClick={handleCreate}>
              생성
            </button>
            <button className="px-3 py-1 text-sm text-gray-600" onClick={() => setShowForm(false)}>
              취소
            </button>
          </div>
        </div>
      )}

      {isLoading ? (
        <p className="text-gray-400">로딩 중...</p>
      ) : testcases.length === 0 ? (
        <p className="text-gray-400">등록된 TestCase가 없습니다.</p>
      ) : (
        <div className="overflow-x-auto border rounded-lg">
          <table className="w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-3 py-2 text-left">TC-ID</th>
                <th className="px-3 py-2 text-left">제목</th>
                <th className="px-3 py-2 text-left">카테고리</th>
                <th className="px-3 py-2 text-left">상태</th>
                <th className="px-3 py-2 text-left">담당자</th>
              </tr>
            </thead>
            <tbody>
              {testcases.map((tc) => (
                <tr key={tc.id} className="border-t hover:bg-blue-50">
                  <td className="px-3 py-2 font-mono text-xs">{tc.id}</td>
                  <td className="px-3 py-2">{tc.title}</td>
                  <td className="px-3 py-2">{tc.category || '-'}</td>
                  <td className="px-3 py-2">
                    <select
                      className="text-xs border rounded px-1 py-0.5"
                      value={tc.status || 'DRAFT'}
                      onChange={(e) => handleStatusChange(tc, e.target.value)}
                    >
                      {TC_STATUS_OPTIONS.map((s) => (
                        <option key={s} value={s}>
                          {s}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td className="px-3 py-2">{tc.assigned_to || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
