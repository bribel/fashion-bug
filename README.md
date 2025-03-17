# fashion-bug
### Current Progress:
- Database schema has been designed and tables are created.
- Scraping images from runway websites (FirstView) is set up.
- Runway scraping and storing process in progress.

### Next Steps:
- Basic backend with FastAPI
- Build frontend to display suggestions and allow user interaction.
- Implement user preference system for style and designer suggestions.
- Refine database schema for flexibility.

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