# Fashion Bug

A runway fashion discovery app. Users browse looks scraped from runway shows, like/dislike them, and build a personal style profile.

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: Vite + React + TypeScript
- **Auth**: JWT (python-jose), bcrypt password hashing

## Running Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Runs on http://localhost:8000. Interactive API docs at http://localhost:8000/docs.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs on http://localhost:5173.

## Environment Variables

Create `backend/.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/fashionbug_db
SECRET_KEY=your-secret-key-here
```

## Database

PostgreSQL. Tables are auto-created on backend startup via SQLAlchemy. To populate looks, run the scraper manually:
```bash
cd backend
python -m app.services.scraper.firstview_scraper
```

## MVP Features

- Browse runway looks in a uniform grid
- Like / dislike looks (requires login)
- User registration and login (JWT)

## Project Structure

```
backend/app/
  api/routes.py        — all API endpoints
  models/
    base.py            — SQLAlchemy Base
    models.py          — ORM models (User, Designer, Look, UserPreference, Recommendation)
    database.py        — engine, SessionLocal, get_db, scraper DB utilities
  schemas/schemas.py   — Pydantic request/response schemas
  services/
    auth.py            — JWT creation and validation, password hashing
    scraper/firstview_scraper.py — runway image scraper (Selenium, run manually)

frontend/src/
  pages/               — Home, Login, Register
  components/          — Navbar, LookGrid, LookCard
  services/api.ts      — API client (fetch wrapper)
  types/index.ts       — shared TypeScript types
```

## Key Conventions

- Auth: JWT bearer token stored in localStorage, passed as `Authorization: Bearer <token>`
- Login uses form data (`application/x-www-form-urlencoded`) at `POST /token`
- All preference endpoints require authentication
