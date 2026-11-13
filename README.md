# Recipe RAG

Local stack for a recipe retrieval app: Postgres, Qdrant, Apache Jena Fuseki, and a small FastAPI service. All four run in Docker Compose.

## Prerequisites

- Docker Desktop (or Docker Engine with the Compose plugin)

## Start

```bash
docker compose up --build
```

Copy `.env.example` to `.env` if you want to change ports or the local database password. The defaults work without a `.env` file.

Stop and keep the data volumes:

```bash
docker compose down
```

Remove the volumes as well:

```bash
docker compose down -v
```

## Services

| Service | Image | URL |
| --- | --- | --- |
| API | local FastAPI app | http://localhost:8000 |
| Postgres | `postgres:17-alpine` | `localhost:5432` |
| Qdrant | `qdrant/qdrant:v1.20.0` | http://localhost:6333 |
| Jena Fuseki | `secoresearch/fuseki:6.2.0` | http://localhost:3030 |

Default credentials are for local development only:

- Postgres: user `recipe`, password `recipe`, database `recipe`
- Fuseki UI: user `admin`, password `admin`
- Fuseki dataset `ds`: query at http://localhost:3030/ds/sparql, update at http://localhost:3030/ds/update
- Qdrant dashboard: http://localhost:6333/dashboard

## API

`GET /` confirms the API process is up.

`GET /health` checks Postgres, Qdrant, and Fuseki. It returns `200` when all three respond, and `503` when any check fails.

```bash
curl http://localhost:8000/health
```
