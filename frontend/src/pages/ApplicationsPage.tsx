import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { api } from '../api'
import { ApplicationForm } from '../components/ApplicationForm'
import { ApplicationTable } from '../components/ApplicationTable'
import { Modal } from '../components/Modal'
import type {
  Application,
  ApplicationInput,
  ApplicationSort,
  ApplicationStatus,
} from '../types'

const statuses: ApplicationStatus[] = ['applied', 'replied', 'interview', 'offer', 'rejected', 'ghosted']
const sortOptions: { value: ApplicationSort; label: string }[] = [
  { value: 'applied_at', label: 'Application date' },
  { value: 'company', label: 'Company' },
  { value: 'last_update_at', label: 'Last updated' },
]

export function ApplicationsPage() {
  const queryClient = useQueryClient()
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('')
  const [platform, setPlatform] = useState('')
  const [sortBy, setSortBy] = useState<ApplicationSort>('applied_at')
  const [order, setOrder] = useState<'asc' | 'desc'>('desc')
  const [page, setPage] = useState(1)
  const [editing, setEditing] = useState<Application | 'new' | null>(null)

  const params = new URLSearchParams({
    page: String(page),
    page_size: '20',
    sort_by: sortBy,
    order,
  })
  if (search.trim()) params.set('search', search.trim())
  if (status) params.set('status', status)
  if (platform.trim()) params.set('platform', platform.trim())

  const query = useQuery({
    queryKey: ['applications', params.toString()],
    queryFn: () => api.applications(params),
  })
  const saveMutation = useMutation({
    mutationFn: (data: ApplicationInput) =>
      editing && editing !== 'new'
        ? api.updateApplication(editing.id, data)
        : api.createApplication(data),
    onSuccess: async () => {
      await queryClient.invalidateQueries()
      setEditing(null)
    },
  })
  const deleteMutation = useMutation({
    mutationFn: api.deleteApplication,
    onSuccess: () => queryClient.invalidateQueries(),
  })

  const applications = query.data?.items ?? []
  return (
    <div className="page-stack">
      <section className="page-heading compact-heading">
        <div><p className="eyebrow">OPPORTUNITY PIPELINE</p><h1>Applications</h1><p className="muted">Keep every role and next step in one place.</p></div>
        <button className="button button-primary" onClick={() => setEditing('new')} type="button">＋ Add application</button>
      </section>
      <section className="panel table-panel">
        <div className="filter-bar">
          <label className="search-field"><span aria-hidden="true">⌕</span><input aria-label="Search company or role" placeholder="Search company or role" value={search} onChange={(event) => { setSearch(event.target.value); setPage(1) }} /></label>
          <label className="filter-control"><span>Status</span><select value={status} onChange={(event) => { setStatus(event.target.value); setPage(1) }}><option value="">All statuses</option>{statuses.map((item) => <option key={item}>{item}</option>)}</select></label>
          <label className="filter-control"><span>Platform</span><input placeholder="Any platform" value={platform} onChange={(event) => { setPlatform(event.target.value); setPage(1) }} /></label>
          <label className="filter-control"><span>Sort by</span><select value={sortBy} onChange={(event) => setSortBy(event.target.value as ApplicationSort)}>{sortOptions.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>
          <button className="button button-quiet sort-order" onClick={() => setOrder(order === 'asc' ? 'desc' : 'asc')} type="button" aria-label={`Sort ${order === 'asc' ? 'descending' : 'ascending'}`}>{order === 'asc' ? '↑ Asc' : '↓ Desc'}</button>
        </div>
        {query.error && <div className="error-banner" role="alert">{query.error.message}</div>}
        {deleteMutation.error && <div className="error-banner" role="alert">{deleteMutation.error.message}</div>}
        {query.isLoading ? <div className="loading-line">Loading applications…</div> : (
          <ApplicationTable
            applications={applications}
            onEdit={setEditing}
            onDelete={(application) => {
              if (window.confirm(`Delete the ${application.role} application at ${application.company}? This cannot be undone.`)) {
                deleteMutation.mutate(application.id)
              }
            }}
          />
        )}
        {query.data && query.data.pages > 1 && (
          <div className="pagination">
            <span>Page {query.data.page} of {query.data.pages} · {query.data.total} applications</span>
            <div>
              <button className="button button-quiet" disabled={page <= 1} onClick={() => setPage(page - 1)} type="button">Previous</button>
              <button className="button button-quiet" disabled={page >= query.data.pages} onClick={() => setPage(page + 1)} type="button">Next</button>
            </div>
          </div>
        )}
      </section>
      {editing && (
        <Modal onClose={() => setEditing(null)} title={editing === 'new' ? 'Add an application' : 'Edit application'}>
          <ApplicationForm initial={editing === 'new' ? undefined : editing} onCancel={() => setEditing(null)} onSubmit={async (data) => { await saveMutation.mutateAsync(data) }} />
        </Modal>
      )}
    </div>
  )
}
