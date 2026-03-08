import { create } from 'zustand'

interface FilterState {
  category: string
  level1: string
  level2: string
  supportStatus: string
  assignedTo: string
  keyword: string
  derivedFrom: string
  setCategory: (v: string) => void
  setLevel1: (v: string) => void
  setLevel2: (v: string) => void
  setSupportStatus: (v: string) => void
  setAssignedTo: (v: string) => void
  setKeyword: (v: string) => void
  setDerivedFrom: (v: string) => void
  reset: () => void
}

export const useFilterStore = create<FilterState>((set) => ({
  category: '',
  level1: '',
  level2: '',
  supportStatus: '',
  assignedTo: '',
  keyword: '',
  derivedFrom: '',
  setCategory: (category) => set({ category, level1: '', level2: '' }),
  setLevel1: (level1) => set({ level1, level2: '' }),
  setLevel2: (level2) => set({ level2 }),
  setSupportStatus: (supportStatus) => set({ supportStatus }),
  setAssignedTo: (assignedTo) => set({ assignedTo }),
  setKeyword: (keyword) => set({ keyword }),
  setDerivedFrom: (derivedFrom) => set({ derivedFrom }),
  reset: () => set({ category: '', level1: '', level2: '', supportStatus: '', assignedTo: '', keyword: '', derivedFrom: '' }),
}))
