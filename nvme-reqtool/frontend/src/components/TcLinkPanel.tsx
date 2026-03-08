import { useState } from 'react'
import { useTestCases, useLinkTestCase, useUnlinkTestCase } from '../hooks/useTestCases'
import type { TestCase } from '../types'

interface Props {
  reqId: string
  linkedTcs: TestCase[]
}

const statusIcon: Record<string, string> = {
  PASS: 'text-green-600',
  FAIL: 'text-red-600',
  READY: 'text-blue-600',
  DRAFT: 'text-gray-400',
  SKIP: 'text-yellow-600',
}

export default function TcLinkPanel({ reqId, linkedTcs }: Props) {
  const { data: allTcs = [] } = useTestCases()
  const linkMut = useLinkTestCase()
  const unlinkMut = useUnlinkTestCase()
  const [showPicker, setShowPicker] = useState(false)

  const linkedIds = new Set(linkedTcs.map((t) => t.id))
  const available = allTcs.filter((t) => !linkedIds.has(t.id))

  return (
    <div>
      <h4 className="font-medium text-sm mb-2">연결된 TestCase</h4>
      {linkedTcs.length === 0 ? (
        <p className="text-sm text-gray-400">연결된 TC가 없습니다.</p>
      ) : (
        <ul className="space-y-1">
          {linkedTcs.map((tc) => (
            <li key={tc.id} className="flex items-center justify-between text-sm bg-gray-50 rounded px-2 py-1">
              <span>
                <span className="font-mono text-xs text-gray-500">{tc.id}</span>{' '}
                {tc.title}{' '}
                <span className={`font-medium ${statusIcon[tc.status || 'DRAFT']}`}>
                  {tc.status}
                </span>
              </span>
              <button
                className="text-red-400 hover:text-red-600 text-xs"
                onClick={() => unlinkMut.mutate({ reqId, tcId: tc.id })}
              >
                해제
              </button>
            </li>
          ))}
        </ul>
      )}

      {!showPicker ? (
        <button
          className="mt-2 text-sm text-blue-600 hover:underline"
          onClick={() => setShowPicker(true)}
        >
          + TC 연결 추가
        </button>
      ) : (
        <div className="mt-2 border rounded p-2 max-h-40 overflow-y-auto">
          {available.length === 0 ? (
            <p className="text-sm text-gray-400">추가 가능한 TC가 없습니다.</p>
          ) : (
            available.map((tc) => (
              <button
                key={tc.id}
                className="block w-full text-left text-sm hover:bg-blue-50 px-2 py-1 rounded"
                onClick={() => {
                  linkMut.mutate({ reqId, tcId: tc.id })
                  setShowPicker(false)
                }}
              >
                {tc.id} - {tc.title}
              </button>
            ))
          )}
          <button
            className="mt-1 text-xs text-gray-400 hover:text-gray-600"
            onClick={() => setShowPicker(false)}
          >
            취소
          </button>
        </div>
      )}
    </div>
  )
}
