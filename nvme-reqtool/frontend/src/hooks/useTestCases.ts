import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import type { TestCase } from '../types'

export function useTestCases(category?: string, status?: string) {
  return useQuery<TestCase[]>({
    queryKey: ['testcases', category, status],
    queryFn: async () => {
      const params: Record<string, string> = {}
      if (category) params.category = category
      if (status) params.status = status
      const { data } = await axios.get('/api/testcases', { params })
      return data
    },
  })
}

export function useCreateTestCase() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (tc: Partial<TestCase> & { id: string; title: string }) => {
      const { data } = await axios.post('/api/testcases', tc)
      return data
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['testcases'] }),
  })
}

export function useUpdateTestCase() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ id, update }: { id: string; update: Partial<TestCase> }) => {
      const { data } = await axios.patch(`/api/testcases/${id}`, update)
      return data
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['testcases'] }),
  })
}

export function useLinkTestCase() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ reqId, tcId }: { reqId: string; tcId: string }) => {
      await axios.post(`/api/requirements/${reqId}/testcases?tc_id=${tcId}`)
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['requirements'] })
      qc.invalidateQueries({ queryKey: ['requirement'] })
    },
  })
}

export function useUnlinkTestCase() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ reqId, tcId }: { reqId: string; tcId: string }) => {
      await axios.delete(`/api/requirements/${reqId}/testcases/${tcId}`)
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['requirements'] })
      qc.invalidateQueries({ queryKey: ['requirement'] })
    },
  })
}
