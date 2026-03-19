import { useEffect, useState } from 'react'

export function usePolling<T>(loader: () => Promise<T>, intervalMs: number, dependencies: unknown[] = []) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    let active = true
    const run = async () => {
      try { const next = await loader(); if (!active) return; setData(next); setError(null) }
      catch (err) { if (!active) return; setError(err instanceof Error ? err.message : 'Unknown error') }
      finally { if (active) setLoading(false) }
    }
    run(); const timer = window.setInterval(run, intervalMs)
    return () => { active = false; window.clearInterval(timer) }
  }, dependencies)
  return { data, loading, error, refresh: async () => { setLoading(true); try { const next = await loader(); setData(next); setError(null) } catch (err) { setError(err instanceof Error ? err.message : 'Unknown error') } finally { setLoading(false) } } }
}
