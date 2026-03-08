interface Props {
  editors: Record<string, string>
}

export default function ActiveEditors({ editors }: Props) {
  const entries = Object.entries(editors)
  if (entries.length === 0) return null

  return (
    <div className="flex items-center gap-2 text-sm text-gray-500 mt-2">
      <span className="inline-block w-2 h-2 rounded-full bg-green-500 animate-pulse" />
      {entries.map(([reqId, user]) => (
        <span key={reqId} className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded">
          {user} - {reqId} 편집 중
        </span>
      ))}
    </div>
  )
}
