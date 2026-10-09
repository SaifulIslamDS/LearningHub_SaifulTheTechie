---
title: "Docker Images & Containers: Package a Pipeline Once, Run It Anywhere"
order: 1
summary: "Write a Dockerfile for a Python ingestion job, build an image with cached layers, run containers with environment variables, networks and volumes, and debug them with logs and exit codes."
level: Intermediate
time: "55 min"
topics: ["Images", "Containers"]
prerequisites: ["phase-3/data-ingestion/01-rest-apis-auth-pagination", "phase-0/linux/01-filesystem-terminal"]
keywords: [docker, dockerfile, image, container, docker build, docker run, layer, build cache, from, workdir, copy, run, cmd, env, user, non-root, tag, docker ps, docker logs, docker exec, environment variable, volume, bind mount, network, port mapping, exit code, .dockerignore]
reviewed: 2026-10-09
files: [phase-3/data-engineering-scripts.zip]
resources:
  - title: "Docker: Get started"
    url: "https://docs.docker.com/get-started/"
    source: "Docker official docs"
    note: "Concepts, a first image and a first container, step by step."
  - title: "Building best practices"
    url: "https://docs.docker.com/build/building/best-practices/"
    source: "Docker official docs"
    note: "Layer caching, small images, non-root users, .dockerignore."
  - title: "Using uv in Docker"
    url: "https://docs.astral.sh/uv/guides/integration/docker/"
    source: "Astral (official)"
    note: "The recommended pattern for uv-based Python images."
---

## What is it?

| Term | Meaning | Analogy |
|---|---|---|
| **Dockerfile** | A text recipe for building an image | The recipe |
| **Image** | A read-only package: OS files + Python + libraries + code | The cooked meal, frozen |
| **Container** | A running (or stopped) instance of an image | A plate served from it |
| **Registry** | Where images are shared (Docker Hub, GitHub Container Registry, cloud registries) | The shop |

A container is not a virtual machine: it shares your computer's kernel, so it starts in about a second and uses little memory, but it's isolated from other containers and from your files unless you connect them.

!!! job "Why it matters at work"
    Pipelines, APIs and databases at most companies run in containers: on a laptop, in CI, on Kubernetes or on cloud services. Orchestrators like Airflow and Dagster (Phase 3B) often run each task in a container. "Can you containerise this?" is a routine request, and Docker appears in a large share of data engineering job adverts.

## Step 1: a Dockerfile for the ingestion job

`docker/ingest_job.py` is a non-interactive version of the API ingestion script: it reads its settings from **environment variables**, pulls every page, and writes `orders.parquet`.

```dockerfile
# Image for the ingestion job: Python + pinned libraries + our script
FROM python:3.14-slim

WORKDIR /app
# print logs immediately, so `docker logs` shows them
ENV PYTHONUNBUFFERED=1

# 1) dependencies first: this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) then the code, which changes more often
COPY ingest_job.py .

# don't run as root inside the container
RUN useradd --create-home appuser
USER appuser

CMD ["python", "ingest_job.py"]
```

| Instruction | Does |
|---|---|
| `FROM` | Start from a base image (an official Python image here) |
| `WORKDIR` | Set the working folder inside the image |
| `ENV` | Set an environment variable |
| `COPY` | Copy files from your folder into the image |
| `RUN` | Run a command **at build time** (install packages, create a user) |
| `USER` | Switch to a non-root user for running |
| `CMD` | The default command **when a container starts** |

`requirements.txt` pins exact versions (`pandas==3.0.6`, `pyarrow==25.0.1`, `requests==2.34.2`), so every build gets the same libraries.

## Step 2: build, and see the layer cache

```bash
docker build -t orders-ingest:1.0 .
```

Each instruction creates a **layer**. Change only `ingest_job.py` and rebuild:

```text
#6 [2/6] WORKDIR /app
#6 CACHED
#7 [3/6] COPY requirements.txt .
#7 CACHED
#8 [4/6] RUN pip install --no-cache-dir -r requirements.txt
#8 CACHED
#9 [5/6] COPY ingest_job.py .
#10 [6/6] RUN useradd --create-home appuser
```

Steps 2–4 come from the **cache**; only the steps after the changed file run again. That's why dependencies are copied and installed **before** the code: a code edit doesn't reinstall pandas. Put what changes least at the top.

`-t orders-ingest:1.0` gives the image a **name:tag**. Use meaningful version tags; `latest` is just a default name, not a guarantee of anything.

## Step 3: run containers that talk to each other

The ingestion job needs the practice API. Build an image for it too (`Dockerfile.api`), put both on a **network**, and pass settings with `-e`:

```bash
docker network create practice-net
docker run -d --name api --network practice-net orders-api:1.0
docker ps
```

```text
NAMES     IMAGE            STATUS         PORTS
api       orders-api:1.0   Up 2 seconds   8765/tcp
```

```bash
docker run --rm --network practice-net \
  -e ORDERS_API_URL=http://api:8765 -e ORDERS_API_TOKEN=practice-token-123 \
  -v "$PWD/output:/out" orders-ingest:1.0
```

```text
ingested 4246 orders (API total 4246) -> /out/orders.parquet
```

| Option | Meaning |
|---|---|
| `-d` | Run in the background (detached) |
| `--name api` | Container name; on a user-defined network it's also the **host name** (`http://api:8765`) |
| `--network` | Containers on the same network can reach each other by name |
| `-e KEY=value` | Environment variable (settings and secrets, not baked into the image) |
| `-v host_path:container_path` | **Bind mount**: the container writes `/out/orders.parquet`, which appears in `./output` on your machine |
| `--rm` | Delete the container when it exits |
| `-p 8765:8765` | Publish a port to your computer (needed only to reach it from your browser) |

## Step 4: debug like a data engineer

**A wrong token:**

```text
requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url: http://api:8765/api/v1/orders?page_size=1000
```

The job fails loudly and exits with a non-zero code, so a scheduler would mark it failed.

**Look inside an image:**

```bash
docker run --rm orders-ingest:1.0 python -c "import sys, pandas, pyarrow, requests; print(sys.version.split()[0], pandas.__version__, pyarrow.__version__, requests.__version__)"
docker run --rm orders-ingest:1.0 whoami
```

```text
3.14.6 3.0.6 25.0.1 2.34.2
appuser
```

| Command | Use |
|---|---|
| `docker ps -a` | All containers, including stopped ones, with their exit codes |
| `docker logs api` | What a container printed (add `-f` to follow) |
| `docker exec -it api bash` | A shell inside a running container (if the image has bash) |
| `docker run --rm -it image bash` | Start a throwaway container to poke around |
| `docker image inspect image` | Configuration: command, user, environment |
| `docker rm -f api` / `docker network rm practice-net` | Clean up |

The Parquet file in `./output` is owned by user ID 1000 (the `appuser` inside the container) on your machine. Bind mounts share files *and* permissions, a common surprise on Linux.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `COPY . .` before installing dependencies | Every code change reinstalls everything | Copy requirements first, code last |
| Secrets in the Dockerfile (`ENV TOKEN=…`) | Anyone with the image can read them | Pass at run time (`-e`, secrets), never bake in |
| Running as root | A compromised container has more power | `USER` with a non-root user |
| Using `localhost` between containers | "Connection refused": localhost is the container itself | Same network; use the container/service name |
| Unpinned versions (`pandas`, `FROM python:latest`) | Different builds on different days | Pin library versions and the base image tag |
| No `.dockerignore` | Huge build context, secrets copied into images | Ignore `.venv`, outputs, `.env`, `.git` |

## Try it yourself

**Task:** Which user does the ingestion image run as, and what command does it run by default? Find out **without** reading the Dockerfile.

<details markdown="1">
<summary>Show the solution</summary>

```bash
docker image inspect orders-ingest:1.0 --format '{{.Config.Cmd}} {{.Config.User}} {{.Config.WorkingDir}}'
```

```text
[python ingest_job.py] appuser /app
```

`docker image inspect` shows the configuration baked into any image, which is useful when you're given an image someone else built.
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. What's the difference between an image and a container?

1. None
2. An image is the read-only package; a container is a running instance of it
3. A container is a stored image

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Why copy `requirements.txt` and install packages before copying the code?

1. It's required by Docker
2. Code edits then reuse the cached dependency layer, making rebuilds fast
3. It makes the image smaller

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

<div class="quiz-q" markdown="1">
3\. How should the ingestion container reach the API container?

1. `http://localhost:8765`
2. `http://api:8765`, with both on the same Docker network
3. Through a shared file

<details markdown="1"><summary>Show answer</summary>
**B.**
</details>
</div>

## Summary

- **Dockerfile** → `docker build` → **image** (layers, cached) → `docker run` → **container**.
- Order the Dockerfile from least to most frequently changed; pin versions; run as a non-root user.
- Configure with **environment variables**; connect containers with **networks**; share files with **volumes**.
- Debug with `docker ps -a`, `logs`, `exec`, `inspect`, and fail loudly with exit codes.

!!! job "Job-ready check"
    **Interview question:** *"Walk me through containerising a Python data job."*

    **Strong answer:** "I start from a slim, pinned Python base image, copy the lock or requirements file and install dependencies first so that layer is cached, then copy the code, create a non-root user and set the command. Configuration and secrets come in as environment variables at run time, never baked in. Outputs go to a volume or object storage, the job exits non-zero on failure for the scheduler, and I add a .dockerignore. Then I test it locally with the same image CI and production use."

    **Mini project:** Containerise the scraping script from the ingestion module: a Dockerfile, a `.dockerignore`, settings via environment variables, and output to a mounted folder. Write the exact `docker build` and `docker run` commands in a README.
