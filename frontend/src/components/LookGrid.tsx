import type { Look } from '../types'
import LookCard from './LookCard'

interface LookGridProps {
  looks: Look[]
  isLoggedIn: boolean
  preferenceMap?: Record<string, boolean>
  hideDislike?: boolean
  onClickWhenActive?: (lookId: string) => void
  onPreferenceChange?: (lookId: string, preference: boolean | null) => void
}

export default function LookGrid({
  looks,
  isLoggedIn,
  preferenceMap = {},
  hideDislike = false,
  onClickWhenActive,
  onPreferenceChange,
}: LookGridProps) {
  return (
    <div className="grid-container">
      <div className="grid-header">
        <h1>{looks.length} looks</h1>
      </div>
      <div className="look-grid">
        {looks.map((look) => (
          <LookCard
            key={look.id}
            look={look}
            isLoggedIn={isLoggedIn}
            initialPreference={preferenceMap[look.id] ?? null}
            hideDislike={hideDislike}
            onClickWhenActive={onClickWhenActive}
            onPreferenceChange={onPreferenceChange}
          />
        ))}
      </div>
    </div>
  )
}
