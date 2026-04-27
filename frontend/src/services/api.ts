import type { Look, User } from '../types'

const BASE_URL = 'http://localhost:8000'

function getToken(): string | null {
  return localStorage.getItem('token')
}

export async function getLooks(): Promise<Look[]> {
  const res = await fetch(`${BASE_URL}/looks`)
  if (!res.ok) throw new Error('Failed to fetch looks')
  return res.json()
}

export async function login(email: string, password: string): Promise<{ token: string; username: string }> {
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)
  const res = await fetch(`${BASE_URL}/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form,
  })
  if (!res.ok) throw new Error('Incorrect email or password')
  const data = await res.json()
  return { token: data.access_token, username: data.username }
}

export async function register(username: string, email: string, password: string): Promise<User> {
  const res = await fetch(`${BASE_URL}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  })
  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.detail || 'Registration failed')
  }
  return res.json()
}

export async function savePreference(lookId: string, preference: boolean): Promise<void> {
  const token = getToken()
  const res = await fetch(`${BASE_URL}/user/preferences`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ look_id: lookId, preference }),
  })
  if (!res.ok) throw new Error('Failed to save preference')
}

export async function deletePreference(lookId: string): Promise<void> {
  const token = getToken()
  const res = await fetch(`${BASE_URL}/user/preferences/${lookId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Failed to delete preference')
}

export async function getPreferenceStatus(): Promise<Record<string, boolean>> {
  const token = getToken()
  const res = await fetch(`${BASE_URL}/user/preferences/status`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Failed to fetch preference status')
  return res.json()
}

export async function getLikedLooks(): Promise<Look[]> {
  const token = getToken()
  const res = await fetch(`${BASE_URL}/user/preferences`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Failed to fetch liked looks')
  return res.json()
}
