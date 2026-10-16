import { Link } from 'react-router-dom'
import type { Application } from '../types'
import { StatusBadge } from './StatusBadge'

export function ApplicationTable({
  applications,
  onEdit,
  onDelete,
}: {
  applications: Application[]
  onEdit?: (application: Application) => void
  onDelete?: (application: Application) => void
}) {
  if (applications.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">↗</div>
        <h3>No applications yet</h3>
        <p>Add your first role to start tracking your search.</p>
      </div>
    )
  }
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr><th>Company / role</th><th>Platform</th><th>Status</th><th>Applied</th><th>Next follow-up</th><th><span className="sr-only">Actions</span></th></tr>
        </thead>
        <tbody>
          {applications.map((application) => (
            <tr key={application.id}>
              <td>
                <Link className="company-link" to={`/applications/${application.id}`}>{application.company}</Link>
                <span className="table-subtitle">{application.role}</span>
              </td>
              <td>{application.platform}</td>
              <td><StatusBadge status={application.status} /></td>
              <td>{new Date(application.applied_at).toLocaleDateString()}</td>
              <td>
                {application.follow_up_at
                  ? new Date(application.follow_up_at).toLocaleDateString()
                  : <span className="muted">—</span>}
              </td>
              <td>
                <div className="row-actions">
                  {onEdit && <button aria-label={`Edit ${application.company}`} className="text-button" onClick={() => onEdit(application)} type="button">Edit</button>}
                  {onDelete && <button aria-label={`Delete ${application.company}`} className="text-button danger-text" onClick={() => onDelete(application)} type="button">Delete</button>}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
