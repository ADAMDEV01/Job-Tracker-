from app.models.application import ApplicationStatus

ALLOWED_STATUS_TRANSITIONS: dict[ApplicationStatus, frozenset[ApplicationStatus]] = {
    ApplicationStatus.APPLIED: frozenset(
        {
            ApplicationStatus.REPLIED,
            ApplicationStatus.INTERVIEW,
            ApplicationStatus.OFFER,
            ApplicationStatus.REJECTED,
            ApplicationStatus.GHOSTED,
        }
    ),
    ApplicationStatus.REPLIED: frozenset(
        {
            ApplicationStatus.INTERVIEW,
            ApplicationStatus.OFFER,
            ApplicationStatus.REJECTED,
            ApplicationStatus.GHOSTED,
        }
    ),
    ApplicationStatus.INTERVIEW: frozenset(
        {
            ApplicationStatus.OFFER,
            ApplicationStatus.REJECTED,
            ApplicationStatus.GHOSTED,
        }
    ),
    ApplicationStatus.OFFER: frozenset(),
    ApplicationStatus.REJECTED: frozenset(),
    ApplicationStatus.GHOSTED: frozenset(),
}


def is_valid_status_transition(
    current: ApplicationStatus,
    requested: ApplicationStatus,
) -> bool:
    return current == requested or requested in ALLOWED_STATUS_TRANSITIONS[current]
