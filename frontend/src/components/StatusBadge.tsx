import type { ApplicationStatus } from '../types'

export function StatusBadge({ status }: { status: ApplicationStatus }) {
  return <span className={`status-badge status-${status}`}>{status}</span>
}
