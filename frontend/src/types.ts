export type ApplicationStatus =
  | 'applied'
  | 'replied'
  | 'interview'
  | 'offer'
  | 'rejected'
  | 'ghosted'

export type ApplicationSort = 'applied_at' | 'company' | 'last_update_at'

export interface Application {
  id: number
  company: string
  role: string
  platform: string
  url: string | null
  follow_up_at: string | null
  status: ApplicationStatus
  applied_at: string
  last_update_at: string
  notes: string | null
  created_at: string
}

export interface ApplicationInput {
  company: string
  role: string
  platform: string
  url?: string | null
  follow_up_at?: string | null
  status?: ApplicationStatus
  applied_at?: string
  notes?: string | null
}

export interface ApplicationPage {
  items: Application[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface StatusCount {
  status: ApplicationStatus
  count: number
}

export interface FollowUpItem {
  application: Application
  days_since_applied: number
}

export interface ResponseMetrics {
  total_applications: number
  responded_applications: number
  response_rate: number
  average_time_to_first_response_days: number | null
}

export interface DashboardSummary extends ResponseMetrics {
  by_status: StatusCount[]
  upcoming_followups: FollowUpItem[]
  may_be_ghosted: FollowUpItem[]
}

export interface PlatformMetrics extends ResponseMetrics {
  platform: string
}

export interface ApplicationEvent {
  id: number
  application_id: number
  previous_status: ApplicationStatus | null
  new_status: ApplicationStatus | null
  event_type: 'created' | 'status_changed' | 'updated'
  created_at: string
  note: string | null
}
