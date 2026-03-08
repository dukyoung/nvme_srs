import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import type { Requirement, RequirementUpdate } from '../types'

const API = '/api/requirements'

interface Filters {
  category?: string
  status?: string
  support_status?: string
  keyword?: string
  assigned_to?: string
  derived_from?: string
}

export function useRequirements(filters: Filters = {}) {
  return useQuery<Requirement[]>({
    queryKey: ['requirements', filters],
    queryFn: async () => {
      const params = Object.fromEntries(
        Object.entries(filters).filter(([, v]) => v),
      )
      const { data } = await axios.get(API, { params })
      return data
    },
  })
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
