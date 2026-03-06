# Project Plan: Scraped Data Dashboard

## Context
- **Goal**: Generalized frontend for logging and retrieving scraped real estate data.
- **Scale**: Multi-city, multi-builder data (~20k projects).
- **Core Requirement**: Scaleable architecture with a dashboard.

## Phase 1: Data Infrastructure (ETL)
- **Task 1.1**: Create `scripts/load_to_db.py`.
- **Task 1.2**: Implement budget parsing logic (Regex + Unit conversion).
- **Task 1.3**: Automated schema generation in `data/app.db`.

## Phase 2: Backend API (FastAPI)
- **Task 2.1**: Setup FastAPI in `backend/app.py`.
- **Task 2.2**: Implement SQLite data access layer in `sqlite3`.
- **Task 2.3**: Define JSON response models for frontend consumption.

## Phase 3: Frontend Dashboard (React + Vite)
- **Task 3.1**: Initialize Vite project in `frontend/`.
- **Task 3.2**: Install Material UI (MUI) & Recharts.
- **Task 3.3**: Component implementation: Filters, Tables, and Charts.
- **Task 3.4**: Logic for median calculation (client-side as requested).

## Phase 4: Integration & UX
- **Task 4.1**: Connect Frontend to Backend API.
- **Task 4.2**: Implement Loading states and error handling.
- **Task 4.3**: Final aesthetic polish (Premium Design).

## Agent Assignments
- **`backend-specialist`**: Phase 1 & 2.
- **`frontend-specialist`**: Phase 3 & 4.

## Verification Checklist
- [ ] ETL loads > 20,000 rows.
- [ ] `/projects` API returns valid JSON.
- [ ] Dashboard filters update UI without full page refresh.
- [ ] Budget median chart renders accurately.
