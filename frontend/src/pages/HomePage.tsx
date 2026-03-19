import { useNavigate } from 'react-router-dom'
import { ActionButton } from '../components/ActionButton'
import { StatCard } from '../components/StatCard'
import { usePolling } from '../hooks/usePolling'
import { api } from '../lib/api'

export function HomePage() {
  const navigate = useNavigate()
  const { data, loading, error, refresh } = usePolling(api.getDashboard, 8000, [])
  return <div className="stack-gap"><section className="hero card"><div><h2>Continue where you left off</h2><p className="muted">The queue favors oldest unfinished items and stores progress in the app database.</p></div><div className="hero-actions"><ActionButton label="Continue" tone="primary" onClick={() => navigate('/review')} disabled={!data?.continue_video_id} /><ActionButton label="Timeline" onClick={() => navigate('/timeline')} /><ActionButton label="Refresh" onClick={() => void refresh()} /></div></section>{loading && !data ? <div className="card">Loading dashboard…</div> : null}{error ? <div className="error-banner">{error}</div> : null}{data ? <><section className="stats-grid"><StatCard label="Total videos" value={data.total_videos} /><StatCard label="Unfinished" value={data.unfinished_count} /><StatCard label="Watched" value={data.watched_count} /><StatCard label="Skipped" value={data.skipped_count} /><StatCard label="Bookmarked" value={data.bookmarked_count} /><StatCard label="Current position" value={data.current_queue_position ?? '—'} hint={data.queue_total ? `of ${data.queue_total}` : undefined} /></section><section className="card info-grid two-column"><div><div className="meta-label">Current item</div><div className="meta-value">{data.current_video_filename ?? 'None selected'}</div></div><div><div className="meta-label">Continue target</div><div className="meta-value">{data.continue_video_filename ?? 'Queue complete'}</div></div></section></> : null}</div>
}
