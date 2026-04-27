import { Link, useNavigate } from 'react-router-dom'

interface NavbarProps {
  username: string | null
  onLogout: () => void
}

export default function Navbar({ username, onLogout }: NavbarProps) {
  const navigate = useNavigate()

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-logo">Fashion Bug</Link>
      <div className="navbar-actions">
        {username ? (
          <>
            <Link to="/profile" className="navbar-btn secondary">My Looks</Link>
            <span>{username}</span>
            <button className="navbar-btn secondary" onClick={onLogout}>Sign out</button>
          </>
        ) : (
          <>
            <button className="navbar-btn secondary" onClick={() => navigate('/register')}>Register</button>
            <button className="navbar-btn" onClick={() => navigate('/login')}>Sign in</button>
          </>
        )}
      </div>
    </nav>
  )
}
