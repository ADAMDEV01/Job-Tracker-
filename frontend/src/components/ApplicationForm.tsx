import { useState, type FormEvent } from 'react'
import type { Application, ApplicationInput, ApplicationStatus } from '../types'

const statuses: ApplicationStatus[] = [
  'applied',
  'replied',
  'interview',
  'offer',
  'rejected',
  'ghosted',
]

interface Props {
  initial?: Application
  onSubmit: (data: ApplicationInput) => Promise<void>
  onCancel: () => void
}

function toLocalInput(value: string | null | undefined): string {
  if (!value) return ''
  const date = new Date(value)
  const offsetDate = new Date(date.getTime() - date.getTimezoneOffset() * 60_000)
  return offsetDate.toISOString().slice(0, 16)
}

export function ApplicationForm({ initial, onSubmit, onCancel }: Props) {
  const [company, setCompany] = useState(initial?.company ?? '')
  const [role, setRole] = useState(initial?.role ?? '')
  const [platform, setPlatform] = useState(initial?.platform ?? '')
  const [url, setUrl] = useState(initial?.url ?? '')
  const [status, setStatus] = useState<ApplicationStatus>(initial?.status ?? 'applied')
  const [appliedAt, setAppliedAt] = useState(toLocalInput(initial?.applied_at))
  const [followUpAt, setFollowUpAt] = useState(toLocalInput(initial?.follow_up_at))
  const [notes, setNotes] = useState(initial?.notes ?? '')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      await onSubmit({
        company: company.trim(),
        role: role.trim(),
        platform: platform.trim(),
        url: url.trim() || null,
        status,
        applied_at: appliedAt ? new Date(appliedAt).toISOString() : undefined,
        follow_up_at: followUpAt ? new Date(followUpAt).toISOString() : null,
        notes: notes.trim() || null,
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not save application.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="form-grid" onSubmit={submit}>
      <label>
        Company
        <input required maxLength={200} value={company} onChange={(event) => setCompany(event.target.value)} />
      </label>
      <label>
        Job title
        <input required maxLength={200} value={role} onChange={(event) => setRole(event.target.value)} />
      </label>
      <label>
        Platform
        <input required maxLength={100} placeholder="Company website, LinkedIn…" value={platform} onChange={(event) => setPlatform(event.target.value)} />
      </label>
      <label>
        Status
        <select value={status} onChange={(event) => setStatus(event.target.value as ApplicationStatus)}>
          {statuses.map((item) => <option key={item} value={item}>{item}</option>)}
        </select>
      </label>
      <label className="field-full">
        Posting URL
        <input type="url" maxLength={2048} placeholder="https://" value={url} onChange={(event) => setUrl(event.target.value)} />
      </label>
      <label>
        Applied on
        <input type="datetime-local" value={appliedAt} onChange={(event) => setAppliedAt(event.target.value)} />
      </label>
      <label>
        Follow-up date
        <input type="datetime-local" value={followUpAt} onChange={(event) => setFollowUpAt(event.target.value)} />
      </label>
      <label className="field-full">
        Notes
        <textarea rows={3} value={notes} onChange={(event) => setNotes(event.target.value)} />
      </label>
      {error && <p className="form-error field-full" role="alert">{error}</p>}
      <div className="form-actions field-full">
        <button className="button button-quiet" type="button" onClick={onCancel}>Cancel</button>
        <button className="button button-primary" disabled={saving} type="submit">
          {saving ? 'Saving…' : initial ? 'Save changes' : 'Add application'}
        </button>
      </div>
    </form>
  )
}
