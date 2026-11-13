import os

import httpx
import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Recipe RAG", version="0.1.0")

QDRANT_URL = os.environ.get("QDRANT_URL", "http://qdrant:6333")
FUSEKI_URL = os.environ.get("FUSEKI_URL", "http://fuseki:3030")
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://recipe:recipe@postgres:5432/recipe",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "recipe-rag", "status": "ok"}


def _check_http(url: str) -> dict[str, object]:
    try:
        response = httpx.get(url, timeout=3.0)
        response.raise_for_status()
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True}

def _check_postgres() -> dict[str, object]:
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            conn.execute("SELECT 1").fetchone()
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True}

@app.get("/health")
def health() -> JSONResponse:

    checks = {
        "postgres": _check_postgres(),
        "qdrant": _check_http(f"{QDRANT_URL}/readyz"),
        "fuseki": _check_http(f"{FUSEKI_URL}/$/ping"),
    }
    
    ok = all(check["ok"] for check in checks.values())
    return JSONResponse(
        status_code=200 if ok else 503,
        content={"status": "ok" if ok else "degraded", "checks": checks},
    )
