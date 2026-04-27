import { useEffect, useState } from 'react'
import type { Look } from '../types'
import { getLikedLooks, deletePreference } from '../services/api'
import LookGrid from '../components/LookGrid'
import ConfirmModal from '../components/ConfirmModal'

export default function Profile() {
  const [looks, setLooks] = useState<Look[]>([])
  const [loading, setLoading] = useState(true)
  const [confirmingLookId, setConfirmingLookId] = useState<string | null>(null)

  useEffect(() => {
    getLikedLooks()
      .then(setLooks)
      .finally(() => setLoading(false))
  }, [])

  async function handleConfirmRemove() {
    if (!confirmingLookId) return
    try {
      await deletePreference(confirmingLookId)
      setLooks((prev) => prev.filter((l) => l.id !== confirmingLookId))
    } finally {
      setConfirmingLookId(null)
    }
  }

  const preferenceMap = Object.fromEntries(looks.map((l) => [l.id, true as boolean]))

  if (loading) return <div className="state-message">Loading</div>

  return (
    <>
      {confirmingLookId && (
        <ConfirmModal
          message="Are you sure you want to remove this look?"
          onConfirm={handleConfirmRemove}
          onCancel={() => setConfirmingLookId(null)}
        />
      )}
      {looks.length === 0
        ? <div className="state-message">You haven't liked any looks yet.</div>
        : (
          <LookGrid
            looks={looks}
            isLoggedIn={true}
            preferenceMap={preferenceMap}
            hideDislike={true}
            onClickWhenActive={setConfirmingLookId}
          />
        )
      }
    </>
  )
}
