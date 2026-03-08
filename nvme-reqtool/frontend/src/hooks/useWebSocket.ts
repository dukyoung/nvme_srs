import { useEffect, useRef, useState, useCallback } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import type { WsMessage } from '../types'

export function useWebSocket(username: string) {
  const wsRef = useRef<WebSocket | null>(null)
  const [editors, setEditors] = useState<Record<string, string>>({})
  const [connected, setConnected] = useState(false)
  const qc = useQueryClient()

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const host = window.location.host
    const ws = new WebSocket(`${protocol}://${host}/ws?username=${encodeURIComponent(username)}`)
    wsRef.current = ws

    ws.onopen = () => setConnected(true)
    ws.onclose = () => {
      setConnected(false)
      wsRef.current = null
    }

    ws.onmessage = (ev) => {
      const msg: WsMessage = JSON.parse(ev.data)
      if (msg.type === 'ACTIVE_EDITORS' && msg.editors) {
        setEditors(msg.editors)
      } else if (msg.type === 'REQ_UPDATED') {
        qc.invalidateQueries({ queryKey: ['requirements'] })
        qc.invalidateQueries({ queryKey: ['requirement'] })
      }
    }

    return () => {
      ws.close()
    }
  }, [username, qc])

  const send = useCallback((msg: WsMessage) => {
    wsRef.current?.send(JSON.stringify(msg))
  }, [])

  return { editors, connected, send }
}
