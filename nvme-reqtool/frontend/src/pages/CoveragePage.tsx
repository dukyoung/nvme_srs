import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import CoverageBar from '../components/CoverageBar'
import type { CoverageSummary, CategoryCoverage, SupportStatusSummary, Requirement } from '../types'

export default function CoveragePage() {
  const { data: summary } = useQuery<CoverageSummary>({
    queryKey: ['coverage-summary'],
    queryFn: () => axios.get('/api/coverage/summary').then((r) => r.data),
  })

  const { data: byCategory = [] } = useQuery<CategoryCoverage[]>({
    queryKey: ['coverage-by-category'],
    queryFn: () => axios.get('/api/coverage/by-category').then((r) => r.data),
  })

  const { data: supportStatus } = useQuery<SupportStatusSummary>({
    queryKey: ['coverage-support-status'],
    queryFn: () => axios.get('/api/coverage/support-status').then((r) => r.data),
  })

  const { data: uncovered = [] } = useQuery<Requirement[]>({
    queryKey: ['coverage-uncovered'],
    queryFn: () => axios.get('/api/coverage/uncovered').then((r) => r.data),
  })

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">커버리지 현황</h1>

      {/* Summary */}
      {summary && (
        <div className="border rounded-lg p-4 bg-white">
          <div className="flex flex-wrap gap-6 text-sm">
            <div>
              전체 REQ: <span className="font-bold">{summary.total_requirements}</span>개
            </div>
            <div>
              TC 연결됨: <span className="font-bold text-green-600">{summary.linked_requirements}</span>개 (
              {summary.coverage_percent}%)
            </div>
            {supportStatus && (
              <>
                <div>
                  지원 완전: <span className="font-bold text-green-600">{supportStatus.supported}</span>
                </div>
                <div>
                  부분: <span className="font-bold text-yellow-600">{supportStatus.partial}</span>
                </div>
                <div>
                  미검토: <span className="font-bold text-orange-600">{supportStatus.unknown}</span>
                </div>
                <div>
                  미지원: <span className="font-bold text-red-600">{supportStatus.not_supported}</span>
                </div>
              </>
            )}
          </div>
          <div className="mt-3">
            <CoverageBar
              label="전체"
              percent={summary.coverage_percent}
              linked={summary.linked_requirements}
              total={summary.total_requirements}
            />
          </div>
        </div>
      )}

      {/* By Category */}
      {byCategory.length > 0 && (
        <div className="border rounded-lg p-4 bg-white">
          <h2 className="text-sm font-semibold mb-3">카테고리별</h2>
          <div className="space-y-1">
            {byCategory.map((c) => (
              <CoverageBar
                key={c.category}
                label={c.category}
                percent={c.coverage_percent}
                linked={c.linked}
                total={c.total}
              />
            ))}
          </div>
        </div>
      )}

      {/* Uncovered */}
      {uncovered.length > 0 && (
        <div className="border rounded-lg p-4 bg-white">
          <h2 className="text-sm font-semibold mb-2">
            TC 미연결 REQ ({uncovered.length}개)
          </h2>
          <div className="max-h-60 overflow-y-auto">
            <table className="w-full text-sm">
              <tbody>
                {uncovered.map((r) => (
                  <tr key={r.id} className="border-t hover:bg-red-50">
                    <td className="px-2 py-1 font-mono text-xs text-gray-500 w-48">{r.id}</td>
                    <td className="px-2 py-1">
                      {r.spec_text.length > 60 ? r.spec_text.slice(0, 60) + '...' : r.spec_text}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
