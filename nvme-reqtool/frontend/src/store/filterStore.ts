import { create } from 'zustand'

interface FilterState {
  category: string
  supportStatus: string
  assignedTo: string
  keyword: string
  derivedFrom: string
  setCategory: (v: string) => void
  setSupportStatus: (v: string) => void
  setAssignedTo: (v: string) => void
  setKeyword: (v: string) => void
  setDerivedFrom: (v: string) => void
  reset: () => void
}

export const useFilterStore = create<FilterState>((set) => ({
  category: '',
  supportStatus: '',
  assignedTo: '',
  keyword: '',
  derivedFrom: '',
  setCategory: (category) => set({ category }),
  setSupportStatus: (supportStatus) => set({ supportStatus }),
  setAssignedTo: (assignedTo) => set({ assignedTo }),
  setKeyword: (keyword) => set({ keyword }),
  setDerivedFrom: (derivedFrom) => set({ derivedFrom }),
  reset: () => set({ category: '', supportStatus: '', assignedTo: '', keyword: '', derivedFrom: '' }),
}))
