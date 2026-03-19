import type { DashboardStatsResponse, PaginatedVideosResponse, PublicConfigResponse, QueueAdjacentResponse, QueueItemResponse, ScanStatusResponse, SettingsResponse, VideoDetail } from '../types'

const API_BASE = ''
function authHeaders(): HeadersInit { const token = localStorage.getItem('reviewQueueToken'); return token ? { Authorization: `Bearer ${token}` } : {} }
async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { ...init, headers: { 'Content-Type': 'application/json', ...authHeaders(), ...(init?.headers ?? {}) } })
  if (response.status === 401) throw new Error('Unauthorized')
  if (!response.ok) throw new Error((await response.text()) || `Request failed: ${response.status}`)
  return response.json() as Promise<T>
}
export const api = {
  getPublicConfig: () => request<PublicConfigResponse>('/api/auth/public-config'),
  login: (username: string, password: string) => request<{ access_token: string; auth_enabled: boolean }>('/api/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) }),
  getDashboard: () => request<DashboardStatsResponse>('/api/dashboard/stats'),
  getSettings: () => request<SettingsResponse>('/api/settings'),
  updateSettings: (payload: Partial<SettingsResponse>) => request<SettingsResponse>('/api/settings', { method: 'PUT', body: JSON.stringify(payload) }),
  getScanStatus: () => request<ScanStatusResponse>('/api/scan/status'),
  startScan: () => request<{ started: boolean; reason?: string }>('/api/scan/start', { method: 'POST' }),
  listVideos: (params: URLSearchParams) => request<PaginatedVideosResponse>(`/api/videos?${params.toString()}`),
  getVideo: (videoId: string, view = 'unfinished') => request<VideoDetail>(`/api/videos/${videoId}?view=${view}`),
  updateVideoStatus: (videoId: string, payload: Record<string, unknown>) => request<VideoDetail>(`/api/videos/${videoId}/status`, { method: 'POST', body: JSON.stringify(payload) }),
  savePlayback: (videoId: string, payload: Record<string, unknown>) => request<{ video_id: string; position_seconds: number }>(`/api/videos/${videoId}/playback`, { method: 'POST', body: JSON.stringify(payload) }),
  resumePlayback: (videoId: string) => request<{ video_id: string; position_seconds: number }>(`/api/videos/${videoId}/resume`),
  getContinue: () => request<QueueItemResponse>('/api/queue/continue'),
  getCurrent: () => request<QueueItemResponse>('/api/queue/current'),
  getAdjacent: (videoId: string, view = 'unfinished') => request<QueueAdjacentResponse>(`/api/queue/adjacent/${videoId}?view=${view}`),
  jump: (params: URLSearchParams) => request<{ video_id: string | null }>(`/api/queue/jump?${params.toString()}`),
}
