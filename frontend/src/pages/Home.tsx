import { useEffect, useState } from 'react'
import type { Look } from '../types'
import { getLooks, getPreferenceStatus, deletePreference } from '../services/api'
import LookGrid from '../components/LookGrid'

interface HomeProps {
  isLoggedIn: boolean
}

export default function Home({ isLoggedIn }: HomeProps) {
  const [looks, setLooks] = useState<Look[]>([])
  const [preferenceMap, setPreferenceMap] = useState<Record<string, boolean>>({})
  const [hiddenLookIds, setHiddenLookIds] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetches: Promise<unknown>[] = [getLooks().then(setLooks)]
    if (isLoggedIn) {
      fetches.push(getPreferenceStatus().then(setPreferenceMap))
    }
    Promise.all(fetches)
      .catch(() => setError('Could not load looks. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [isLoggedIn])

  function handlePreferenceChange(lookId: string, preference: boolean | null) {
    if (preference === false) {
      setPreferenceMap((prev) => ({ ...prev, [lookId]: false }))
      setHiddenLookIds((prev) => [...prev, lookId])
    } else if (preference === true) {
      setPreferenceMap((prev) => ({ ...prev, [lookId]: true }))
    } else {
      setPreferenceMap((prev) => {
        const next = { ...prev }
        delete next[lookId]
        return next
      })
    }
  }

  async function handleUndo() {
    await Promise.all(hiddenLookIds.map((id) => deletePreference(id).catch(() => {})))
    setPreferenceMap((prev) => {
      const next = { ...prev }
      hiddenLookIds.forEach((id) => delete next[id])
      return next
    })
    setHiddenLookIds([])
  }

  if (loading) return <div className="state-message">Loading</div>
  if (error) return <div className="state-message">{error}</div>
  if (looks.length === 0) return <div className="state-message">No looks yet — run the scraper to populate the database.</div>

  const visibleLooks = looks.filter((l) => !hiddenLookIds.includes(l.id))

  return (
    <>
      <LookGrid
        looks={visibleLooks}
        isLoggedIn={isLoggedIn}
        preferenceMap={preferenceMap}
        onPreferenceChange={handlePreferenceChange}
      />
      {hiddenLookIds.length > 0 && (
        <div className="undo-bar">
          <span>{hiddenLookIds.length} look{hiddenLookIds.length > 1 ? 's' : ''} hidden</span>
          <button className="undo-bar-btn" onClick={handleUndo}>Undo</button>
        </div>
      )}
    </>
  )
}
