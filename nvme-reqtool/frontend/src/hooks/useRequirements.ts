import { useMemo } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import type { Requirement, RequirementUpdate } from '../types'

const API = '/api/requirements'

interface Filters {
  category?: string
  level1?: string
  level2?: string
  status?: string
  support_status?: string
  keyword?: string
  assigned_to?: string
  derived_from?: string
}

/** 전체 데이터를 한 번만 fetch (staleTime 길게) */
function useAllRequirements() {
  return useQuery<Requirement[]>({
    queryKey: ['requirements'],
    queryFn: async () => {
      const { data } = await axios.get(API)
      return data
    },
    staleTime: 30_000,
  })
}

/** 클라이언트 사이드 필터링 */
export function useRequirements(filters: Filters = {}) {
  const { data: all = [], isLoading, error } = useAllRequirements()

  const filtered = useMemo(() => {
    let result = all
    if (filters.category) {
      result = result.filter((r) => r.category === filters.category)
    }
    if (filters.level1) {
      result = result.filter((r) => r.level1 === filters.level1)
    }
    if (filters.level2) {
      result = result.filter((r) => r.level2 === filters.level2)
    }
    if (filters.status) {
      result = result.filter((r) => r.status === filters.status)
    }
    if (filters.support_status) {
      result = result.filter((r) => r.support_status === filters.support_status)
    }
    if (filters.assigned_to) {
      result = result.filter((r) => r.assigned_to === filters.assigned_to)
    }
    if (filters.derived_from) {
      const q = filters.derived_from.toLowerCase()
      result = result.filter((r) => r.derived_from?.toLowerCase().includes(q))
    }
    if (filters.keyword) {
      const q = filters.keyword.toLowerCase()
      result = result.filter(
        (r) =>
          r.id.toLowerCase().includes(q) ||
          r.spec_text.toLowerCase().includes(q) ||
          r.spec_text_ko?.toLowerCase().includes(q) ||
          r.keyword?.toLowerCase().includes(q) ||
          r.derived_from?.toLowerCase().includes(q),
      )
    }
    return result
  }, [all, filters.category, filters.level1, filters.level2, filters.status, filters.support_status, filters.assigned_to, filters.derived_from, filters.keyword])

  return { data: filtered, isLoading, error }
}

export function useRequirement(id: string) {
  return useQuery<Requirement>({
    queryKey: ['requirement', id],
    queryFn: async () => {
      const { data } = await axios.get(`${API}/${id}`)
      return data
    },
    enabled: !!id,
  })
}

export function useUpdateRequirement() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async ({ id, update }: { id: string; update: RequirementUpdate }) => {
      const { data } = await axios.patch(`${API}/${id}`, update)
      return data
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['requirements'] })
      qc.invalidateQueries({ queryKey: ['requirement'] })
    },
  })
}

export function useDeleteRequirement() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (id: string) => {
      await axios.delete(`${API}/${id}`)
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['requirements'] })
    },
  })
}

export function useImportRequirements() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: async (file: File) => {
      const form = new FormData()
      form.append('file', file)
      const { data } = await axios.post(`${API}/import`, form)
      return data
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['requirements'] })
    },
  })
}
