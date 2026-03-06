# backend/app.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
try:
    from .db import get_db_connection
except ImportError:
    from db import get_db_connection

app = FastAPI(title="Scraped Data API")

# Enable CORS for React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Scraped Data API is running"}

@app.get("/projects")
def get_projects(
    state: Optional[str] = None,
    city: Optional[str] = None,
    status: Optional[str] = None,
    builder: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    conn = get_db_connection()
    query = "SELECT * FROM projects WHERE 1=1"
    params = []

    if state:
        query += " AND state = ?"
        params.append(state)

    if city:
        query += " AND city = ?"
        params.append(city)
    if status:
        query += " AND status = ?"
        params.append(status)
    if builder:
        query += " AND builder_name = ?"
        params.append(builder)

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = conn.execute(query, params).fetchall()
    conn.close()

    return [dict(row) for row in rows]

@app.get("/cities")
def get_cities(state: Optional[str] = None):
    conn = get_db_connection()
    query = "SELECT DISTINCT city FROM projects WHERE city != ''"
    params = []
    if state:
        query += " AND state = ?"
        params.append(state)
    query += " ORDER BY city"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [row['city'] for row in rows]

@app.get("/states")
def get_states():
    conn = get_db_connection()
    rows = conn.execute("SELECT DISTINCT state FROM projects WHERE state != '' ORDER BY state").fetchall()
    conn.close()
    return [row['state'] for row in rows]

@app.get("/metrics/projects")
def get_project_metrics(state: Optional[str] = None):
    conn = get_db_connection()
    
    where_clause = ""
    params = []
    if state:
        where_clause = " WHERE state = ?"
        params = [state]
    
    total = conn.execute(f"SELECT COUNT(*) as count FROM projects{where_clause}", params).fetchone()['count']
    
    status_counts = conn.execute(
        f"SELECT status, COUNT(*) as count FROM projects{where_clause} GROUP BY status", params
    ).fetchall()
    
    if state:
        city_query = "SELECT city, COUNT(*) as count FROM projects WHERE state = ? AND city != '' GROUP BY city ORDER BY count DESC LIMIT 10"
    else:
        city_query = "SELECT city, COUNT(*) as count FROM projects WHERE city != '' GROUP BY city ORDER BY count DESC LIMIT 10"
    
    city_counts = conn.execute(city_query, params).fetchall()
    
    conn.close()

    return {
        "total": total,
        "by_status": {row['status']: row['count'] for row in status_counts},
        "top_cities": {row['city']: row['count'] for row in city_counts}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
