interface Props {
  label: string
  percent: number
  linked: number
  total: number
}

export default function CoverageBar({ label, percent, linked, total }: Props) {
  const barColor =
    percent >= 80 ? 'bg-green-500' : percent >= 50 ? 'bg-yellow-500' : 'bg-red-500'

  return (
    <div className="flex items-center gap-3 py-1">
      <span className="w-16 text-sm font-medium text-gray-700">{label}</span>
      <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
        <div
          className={`${barColor} h-full rounded-full transition-all`}
          style={{ width: `${percent}%` }}
        />
      </div>
      <span className="text-sm text-gray-600 w-28 text-right">
        {percent}% ({linked}/{total})
      </span>
    </div>
  )
}
