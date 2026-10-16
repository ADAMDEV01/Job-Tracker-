import { useEffect, type ReactNode } from 'react'

interface Props {
  title: string
  children: ReactNode
  onClose: () => void
}

export function Modal({ title, children, onClose }: Props) {
  useEffect(() => {
    const handleKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [onClose])

  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={(event) => {
      if (event.target === event.currentTarget) onClose()
    }}>
      <section aria-labelledby="modal-title" aria-modal="true" className="modal-card" role="dialog">
        <div className="modal-heading">
          <h2 id="modal-title">{title}</h2>
          <button aria-label="Close dialog" className="icon-button" onClick={onClose} type="button">×</button>
        </div>
        {children}
      </section>
    </div>
  )
}
