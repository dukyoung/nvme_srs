import { useState, useMemo } from 'react'
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
  type ColumnDef,
  type SortingState,
} from '@tanstack/react-table'
import type { Requirement } from '../types'
import { SUPPORT_STATUS_OPTIONS, CATEGORY_LABEL_MAP } from '../types'
import { useUpdateRequirement } from '../hooks/useRequirements'

interface Props {
  data: Requirement[]
  onRowClick: (req: Requirement) => void
  editors: Record<string, string>
}

function SupportBadge({ value }: { value: string | null }) {
  const opt = SUPPORT_STATUS_OPTIONS.find((o) => o.value === value)
  if (!opt) return <span className="text-gray-400">-</span>
  return (
    <span className={`px-2 py-0.5 rounded text-xs font-medium ${opt.color}`}>
      {opt.label}
    </span>
  )
}

export default function ReqTable({ data, onRowClick, editors }: Props) {
  const [sorting, setSorting] = useState<SortingState>([])
  const updateReq = useUpdateRequirement()

  const handleInlineChange = (id: string, field: string, value: string) => {
    updateReq.mutate({ id, update: { [field]: value } })
  }

  const columns = useMemo<ColumnDef<Requirement>[]>(
    () => [
      {
        accessorKey: 'id',
        header: 'REQ-ID',
        size: 200,
        cell: ({ row }) => {
          const editing = editors[row.original.id]
          return (
            <div className="flex items-center gap-1">
              <button
                className="text-blue-600 hover:underline font-mono text-xs"
                onClick={() => onRowClick(row.original)}
              >
                {row.original.id}
              </button>
              {editing && (
                <span className="text-[10px] bg-yellow-100 text-yellow-700 px-1 rounded">
                  {editing}
                </span>
              )}
            </div>
          )
        },
      },
      {
        accessorKey: 'category',
        header: '분류',
        size: 100,
        cell: ({ getValue }) => {
          const cat = getValue() as string
          return (
            <span className="text-xs" title={CATEGORY_LABEL_MAP[cat] || cat}>
              {cat}
            </span>
          )
        },
      },
      {
        accessorKey: 'derived_from',
        header: '출처',
        size: 140,
        cell: ({ getValue }) => {
          const val = getValue() as string | null
          return (
            <span className="text-xs font-mono text-gray-600">{val || '-'}</span>
          )
        },
      },
      {
        accessorKey: 'spec_text',
        header: 'Spec 요약',
        size: 300,
        cell: ({ getValue }) => {
          const text = getValue() as string
          return (
            <span className="text-sm" title={text}>
              {text.length > 80 ? text.slice(0, 80) + '...' : text}
            </span>
          )
        },
      },
      {
        accessorKey: 'support_status',
        header: '지원상태',
        size: 120,
        cell: ({ row }) => (
          <select
            className="text-xs border rounded px-1 py-0.5 bg-white"
            value={row.original.support_status || 'UNKNOWN'}
            onClick={(e) => e.stopPropagation()}
            onChange={(e) =>
              handleInlineChange(row.original.id, 'support_status', e.target.value)
            }
          >
            {SUPPORT_STATUS_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        ),
      },
      {
        accessorKey: 'assigned_to',
        header: '담당자',
        size: 100,
        cell: ({ row }) => (
          <input
            className="text-xs border rounded px-1 py-0.5 w-20 bg-white"
            value={row.original.assigned_to || ''}
            onClick={(e) => e.stopPropagation()}
            onChange={(e) =>
              handleInlineChange(row.original.id, 'assigned_to', e.target.value)
            }
            placeholder="-"
          />
        ),
      },
      {
        accessorKey: 'priority',
        header: '우선순위',
        size: 90,
        cell: ({ row }) => (
          <select
            className="text-xs border rounded px-1 py-0.5 bg-white"
            value={row.original.priority || 'NORMAL'}
            onClick={(e) => e.stopPropagation()}
            onChange={(e) =>
              handleInlineChange(row.original.id, 'priority', e.target.value)
            }
          >
            <option value="HIGH">HIGH</option>
            <option value="NORMAL">NORMAL</option>
            <option value="LOW">LOW</option>
          </select>
        ),
      },
      {
        accessorKey: 'tc_count',
        header: 'TC',
        size: 50,
        cell: ({ getValue }) => {
          const count = getValue() as number
          return (
            <span
              className={`text-sm font-medium ${count === 0 ? 'text-red-500' : 'text-green-600'}`}
            >
              {count}
            </span>
          )
        },
      },
    ],
    [editors, onRowClick],
  )

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  })

  return (
    <div className="overflow-x-auto border rounded-lg">
      <table className="w-full text-sm">
        <thead className="bg-gray-100">
          {table.getHeaderGroups().map((hg) => (
            <tr key={hg.id}>
              {hg.headers.map((header) => (
                <th
                  key={header.id}
                  className="px-3 py-2 text-left font-medium text-gray-600 cursor-pointer select-none"
                  style={{ width: header.getSize() }}
                  onClick={header.column.getToggleSortingHandler()}
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                  {{ asc: ' ↑', desc: ' ↓' }[header.column.getIsSorted() as string] ?? ''}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => {
            const isUncovered = row.original.tc_count === 0
            const isUnknown = row.original.support_status === 'UNKNOWN'
            return (
              <tr
                key={row.id}
                className={`border-t hover:bg-blue-50 ${
                  isUncovered && isUnknown
                    ? 'bg-red-50'
                    : isUnknown
                      ? 'bg-orange-50'
                      : ''
                }`}
              >
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="px-3 py-2">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
