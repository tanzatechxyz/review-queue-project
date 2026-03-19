import { useState } from 'react'
import { api } from '../lib/api'

export function LoginScreen({ onSuccess }: { onSuccess: () => void }) {
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault(); setLoading(true); setError(null)
    try { const response = await api.login(username, password); if (response.auth_enabled && response.access_token) localStorage.setItem('reviewQueueToken', response.access_token); onSuccess() }
    catch (err) { setError(err instanceof Error ? err.message : 'Login failed') }
    finally { setLoading(false) }
  }
  return <div className="login-shell"><form className="card login-card" onSubmit={handleSubmit}><h2>Local sign-in</h2><p className="muted">Optional single-user protection for LAN use.</p><label><span>Username</span><input value={username} onChange={(e) => setUsername(e.target.value)} /></label><label><span>Password</span><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>{error ? <div className="error-banner">{error}</div> : null}<button className="action-button primary" type="submit" disabled={loading}>{loading ? 'Signing in…' : 'Sign in'}</button></form></div>
}
