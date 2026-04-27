import { useState } from 'react'
import type { Look } from '../types'
import { savePreference, deletePreference } from '../services/api'

interface LookCardProps {
  look: Look
  isLoggedIn: boolean
  initialPreference?: boolean | null
  hideDislike?: boolean
  onClickWhenActive?: (lookId: string) => void
  onPreferenceChange?: (lookId: string, preference: boolean | null) => void
}

export default function LookCard({
  look,
  isLoggedIn,
  initialPreference = null,
  hideDislike = false,
  onClickWhenActive,
  onPreferenceChange,
}: LookCardProps) {
  const [preference, setPreference] = useState<boolean | null>(initialPreference)

  async function applyChange(next: boolean | null) {
    try {
      if (next === null) {
        await deletePreference(look.id)
      } else {
        await savePreference(look.id, next)
      }
      setPreference(next)
      onPreferenceChange?.(look.id, next)
    } catch {
      // keep current state on error
    }
  }

  function handlePreference(value: boolean) {
    if (!isLoggedIn) return
    const isUndo = preference === value
    if (isUndo && onClickWhenActive) {
      onClickWhenActive(look.id)
    } else {
      applyChange(isUndo ? null : value)
    }
  }

  const designerName = look.designer?.name ?? 'Unknown'
  const meta = [look.season, look.collection_type].filter(Boolean).join(' · ')

  return (
    <div className="look-card">
      <div className="look-card-image-wrap">
        <img src={look.image_url} alt={`${designerName} ${look.season ?? ''}`} loading="lazy" />

        {isLoggedIn && (
          <div className="look-card-overlay">
            <button
              className={`btn-like${preference === true ? ' active' : ''}`}
              onClick={() => handlePreference(true)}
              title="Like"
            >♥</button>
            {!hideDislike && (
              <button
                className={`btn-dislike${preference === false ? ' active' : ''}`}
                onClick={() => handlePreference(false)}
                title="Pass"
              >✕</button>
            )}
          </div>
        )}
      </div>

      <div className="look-card-info">
        <div className="look-card-designer">{designerName}</div>
        {meta && <div className="look-card-meta">{meta}</div>}
      </div>
    </div>
  )
}
