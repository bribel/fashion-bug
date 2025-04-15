# fashion-bug
### Current Progress:
- Database schema has been designed and tables are created.
- Scraping images from runway websites (FirstView) is set up.
- Runway scraping and storing process in progress.
- Basic backend with FastAPI

### Next Steps:
- Adding user authentication
- Building recommendation system
- Build frontend to display suggestions and allow user interaction.
- Implement user preference system for style and designer suggestions.
- Refine database schema for flexibility.

### Notes:
-user ID for saving user preference does not seem to be necessary now that auth is implemented

### Project Structure:
```
fashion-bug
├─ backend
│  ├─ app
│  │  ├─ api
│  │  ├─ main.py
│  │  ├─ models
│  │  │  ├─ database.py
│  │  │  ├─ models.py
│  │  │  └─ user.py
│  │  ├─ schemas
│  │  ├─ services
│  │  │  └─ scraper
│  │  │     ├─ firstview_scraper.py
│  │  │     └─ __init__.py
│  │  └─ __init__.py
│  └─ requirements.txt
├─ frontend
│  └─ src
│     ├─ components
│     ├─ pages
│     └─ services
├─ LICENSE
└─ README.md

```
```
fashion-bug
├─ backend
│  ├─ app
│  │  ├─ api
│  │  │  └─ routes.py
│  │  ├─ main.py
│  │  ├─ models
│  │  │  ├─ base.py
│  │  │  ├─ database.py
│  │  │  ├─ models.py
│  │  │  └─ user.py
│  │  ├─ schemas
│  │  │  └─ schemas.py
│  │  ├─ services
│  │  │  ├─ scraper
│  │  │  │  ├─ firstview_scraper.py
│  │  │  │  └─ __init__.py
│  │  │  └─ __init__.py
│  │  └─ __init__.py
│  └─ requirements.txt
├─ frontend
│  └─ src
│     ├─ components
│     ├─ pages
│     └─ services
├─ LICENSE
└─ README.md

```