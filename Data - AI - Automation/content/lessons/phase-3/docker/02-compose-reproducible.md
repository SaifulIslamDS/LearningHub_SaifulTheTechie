---
title: "Docker Compose & Reproducible Environments: Run the Whole Pipeline With One Command"
order: 2
summary: "Describe a multi-container pipeline (API + ingestion job) in compose.yaml with health checks, dependencies, environment variables and volumes, run it with one command, and make builds reproducible with pinned versions, lock files and digests."
level: Intermediate
time: "50 min"
topics: ["Compose", "Reproducible environments"]
prerequisites: ["phase-3/docker/01-images-containers"]
keywords: [docker compose, compose.yaml, services, depends_on, healthcheck, service_healthy, environment, .env, volumes, bind mount, ports, compose network, docker compose up, docker compose down, docker compose config, reproducible environment, pinning, image digest, lock file, uv.lock, stopsignal, pid 1, exit code 137]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Docker Compose overview"
    url: "https://docs.docker.com/compose/"
    source: "Docker official docs"
    note: "What Compose is and how to use it."
  - title: "Compose file reference"
    url: "https://docs.docker.com/reference/compose-file/"
    source: "Docker official docs"
    note: "services, healthcheck, depends_on, volumes, environment and more."
  - title: "Using uv in Docker"
    url: "https://docs.astral.sh/uv/guides/integration/docker/"
    source: "Astral (official)"
    note: "Reproducible Python images from uv.lock."
---

## What is it?

- **Docker Compose** describes several containers (**services**), their settings and how they connect, in one file, `compose.yaml`. `docker compose up` starts them all; `docker compose down` removes them.
- A **reproducible environment** gives the same result for anyone, on any machine, at any later date: same OS, same Python, same library versions, same configuration.

!!! job "Why it matters at work"
    Local development stacks (a database, an API, a pipeline, maybe Airflow) are almost always started with Compose, and it's the usual first step before Kubernetes or a managed container service. Reproducibility is what lets a teammate, CI and production all run the code you tested, and it's the foundation of reliable data pipelines.

## Step 1: the compose file

`docker/compose.yaml` runs the practice API and the ingestion job together:

```yaml
# Two services: the practice API and the ingestion job that reads from it.
#   docker compose up --build      start everything (Ctrl+C to stop)
#   docker compose down            remove the containers
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    environment:
      ORDERS_API_TOKEN: ${ORDERS_API_TOKEN:-practice-token-123}
    ports:
      - "8765:8765"                     # host:container, so you can open it from your browser too
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8765/robots.txt')"]
      interval: 2s
      timeout: 2s
      retries: 10

  ingest:
    build: .
    depends_on:
      api:
        condition: service_healthy      # wait until the API answers
    environment:
      ORDERS_API_URL: http://api:8765   # service name = host name on the compose network
      ORDERS_API_TOKEN: ${ORDERS_API_TOKEN:-practice-token-123}
      OUTPUT_DIR: /out
    volumes:
      - ./output:/out                   # the Parquet file appears in ./output on your machine
```

| Key | Purpose |
|---|---|
| `services` | One entry per container: `api`, `ingest` |
| `build` | Build the image from a Dockerfile (or use `image:` for a ready-made one, e.g. `postgres:18`) |
| `environment` | Settings; `${VAR:-default}` reads your shell or a `.env` file |
| `ports` | Publish to your computer (not needed for container-to-container traffic) |
| `healthcheck` | How Docker tests that the service really works |
| `depends_on` + `service_healthy` | Start `ingest` only after `api` passes its health check |
| `volumes` | Bind a host folder (or a named volume) into the container |

Compose creates a private **network** automatically; every service is reachable by its **service name** (`http://api:8765`). There's no top-level `version:` key: modern Compose ignores it and warns that it's obsolete.

## Step 2: one command

```bash
docker compose up --build --abort-on-container-exit --exit-code-from ingest
```

```text
 Container docker-api-1 Starting
 Container docker-api-1 Started
 Container docker-api-1 Waiting
api-1  | Practice API on http://0.0.0.0:8765  (token: practice-token-123)  Ctrl+C to stop
 Container docker-api-1 Healthy
 Container docker-ingest-1 Starting
 Container docker-ingest-1 Started
ingest-1  | ingested 4246 orders (API total 4246) -> /out/orders.parquet
ingest-1 exited with code 0
api-1 exited with code 130
```

- Compose built both images, started the API, **waited until it was healthy**, then ran the job.
- `--exit-code-from ingest` makes the whole command succeed or fail with the job, which is perfect for CI.
- Container names are `<project>-<service>-<n>`. The project name defaults to the folder name (`docker`).

```bash
docker compose ps -a        # status of each service
docker compose logs ingest  # one service's output
docker compose down         # stop and remove containers and the network
```

### A real bug we hit: stopping the API took 10 seconds (exit 137)

The first version stopped with `api-1 exited with code 137`: Docker sent the stop signal, waited 10 seconds, then killed it. A Python program running as the container's **main process (PID 1)** doesn't react to the default stop signal (SIGTERM) unless it handles it. The fix in `Dockerfile.api`:

```dockerfile
# Python running as PID 1 ignores the default stop signal; Ctrl+C (SIGINT) stops it cleanly
STOPSIGNAL SIGINT
CMD ["python", "mock_api.py"]
```

Now it stops immediately (exit **130** = interrupted by SIGINT). Alternatives: handle SIGTERM in your code, or add `init: true` to the service.

### Another one: "port is already allocated"

```text
failed to bind host port 0.0.0.0:8765/tcp: address already in use
```

The practice API was still running outside Docker on port 8765. Stop the other program, or publish a different host port (`"18765:8765"`).

## Step 3: configuration and secrets

```bash
docker compose config        # shows the final, fully resolved configuration
```

```text
    environment:
      ORDERS_API_TOKEN: practice-token-123
      ORDERS_API_URL: http://api:8765
      OUTPUT_DIR: /out
```

Set `ORDERS_API_TOKEN=s3cret` in your shell (or in a `.env` file next to `compose.yaml`) and the resolved value changes everywhere it's used:

```text
      ORDERS_API_TOKEN: s3cret
```

- Keep real secrets in `.env` (and add `.env` to `.gitignore`), or use Compose **secrets** / your platform's secret store.
- `docker compose config` is the quickest way to debug "why does my container see the wrong value?".

## Step 4: reproducible environments

| Layer | Pin it with | In this project |
|---|---|---|
| Base OS + Python | A specific image tag, or a **digest** (`python:3.14-slim@sha256:…`) for full immutability | `FROM python:3.14-slim` |
| Python libraries | Exact versions, ideally a **lock file** with hashes | `requirements.txt` with `==` pins |
| System packages | Explicit `apt-get install pkg=version` (when you need them) | None needed |
| Configuration | Environment variables + versioned `compose.yaml` | `.env`, compose |
| Data | Versioned inputs and fingerprints (Phase 2 research thinking) | SHA-256 of input files |

Check what really ended up in the image:

```bash
docker run --rm orders-ingest:1.0 pip freeze
```

```text
certifi==2026.7.22
charset-normalizer==3.5.2
idna==3.20
numpy==2.5.3
pandas==3.0.6
pyarrow==25.0.1
python-dateutil==2.9.0.post0
requests==2.34.2
six==1.17.0
urllib3==2.8.0
```

Only 3 libraries were pinned, but 10 were installed: their **dependencies** (numpy, urllib3, …) were resolved at build time and could differ next month. A **lock file** pins the whole tree. With uv (Phase 0), the officially recommended pattern is:

```dockerfile
FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY . .
CMD ["uv", "run", "--no-sync", "python", "ingest_job.py"]
```

*(Shown for reference; this variant wasn't run for the lesson. `--locked` fails the build if `uv.lock` is out of date, so the image always matches the lock file.)*

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `depends_on` without a health check | The job starts before the API/database is ready | `condition: service_healthy` + a real healthcheck |
| `localhost` in service URLs | Connection refused | Service names on the compose network |
| Secrets committed in `compose.yaml` | Leaked credentials | `${VAR}` + `.env` (git-ignored) or secrets |
| Pinning only top-level packages | Dependency drift between builds | Lock files (`uv.lock`), digests for base images |
| Ignoring exit codes | CI passes while the job failed | `--exit-code-from`; non-zero on failure |

## Try it yourself

**Task:** Add a **PostgreSQL** service to `compose.yaml` that the pipeline could load into: official image, a password from `.env`, a named volume so data survives `docker compose down`, and a health check.

<details markdown="1">
<summary>Show a model answer</summary>

```yaml
  db:
    image: postgres:18
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?set POSTGRES_PASSWORD in .env}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 2s
      retries: 15

volumes:
  pgdata:
```

`${VAR:?message}` makes Compose stop with a clear error if the password isn't set. The named volume `pgdata` keeps the database files between runs (`docker compose down -v` deletes it). The official image's documentation explains its data directory and environment variables. *(This answer wasn't executed for the lesson, because our build machine couldn't pull images from Docker Hub.)*
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. How does the `ingest` service find the `api` service?

1. By its IP address, written in the code
2. By its service name (`api`) on the network Compose creates
3. Through a shared folder

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. What does `condition: service_healthy` add to `depends_on`?

1. Nothing
2. The dependent service waits until the health check passes, not just until the container starts
3. It restarts failed containers

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. You pinned pandas, pyarrow and requests, but the image contains numpy too. Is the environment fully reproducible?

1. Yes
2. No: dependencies like numpy can drift; use a lock file (and a pinned base image)
3. Only on Linux

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- **Compose** = several services in one `compose.yaml`: build/image, environment, ports, volumes, health checks, dependencies.
- `docker compose up --build` / `down`; `config` shows the resolved settings; `--exit-code-from` for CI.
- Containers reach each other by **service name**; use health checks so services start in the right order; handle stop signals (`STOPSIGNAL`, `init: true`).
- **Reproducible**: pinned base image (tag or digest), lock files for the full dependency tree, configuration in env/`.env`, versioned data.

!!! job "Job-ready check"
    **Interview question:** *"How do you make sure a pipeline runs the same on your laptop, in CI and in production?"*

    **Strong answer:** "I containerise it: a pinned base image, dependencies installed from a lock file, configuration and secrets injected through environment variables, and the same image promoted from CI to production. Locally, Docker Compose starts the pipeline with its dependencies (database, API) using health checks, and CI runs the same compose setup, failing on the job's exit code. Data inputs are versioned too, so a run can be reproduced exactly."

    **Mini project:** Extend the compose stack with the PostgreSQL service from *Try it yourself* and a `load` service that reads `output/orders.parquet` into the database after `ingest` completes successfully (`condition: service_completed_successfully`).
