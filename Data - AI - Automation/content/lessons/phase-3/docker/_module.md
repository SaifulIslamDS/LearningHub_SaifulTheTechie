**Docker** packages an application together with everything it needs (operating system libraries, Python, packages, code, settings) into an **image** that runs the same way on any machine as a **container**. It ends "works on my machine" problems, and it's how pipelines, databases and APIs are run in development, CI and production. **Docker Compose** starts several containers that work together with one command.

!!! tip "Setup"
    - **Windows / Mac:** install **Docker Desktop** from <https://www.docker.com/products/docker-desktop/> (on Windows it uses WSL 2, from Phase 0). **Linux:** install Docker Engine for your distribution.
    - Check it works: `docker run hello-world`.
    - The files for this module are in the `docker/` folder of [data-engineering-scripts.zip](../../../downloads/phase-3/data-engineering-scripts.zip).

!!! note "How the outputs in this module were made"
    Our build machine couldn't download images from Docker Hub, so we built a local stand-in for `python:3.14-slim` (Ubuntu 24.04 with CPython 3.14.6) and ran **the same Dockerfiles and compose file** on Docker Engine 29 and Compose 5. Commands, logs and behaviour are real; image IDs, digests and sizes on your machine will differ.

**By the end of this module you can:** write a Dockerfile, build and tag images, run containers with environment variables, ports, networks and volumes, debug them, run a multi-service pipeline with Docker Compose, and make environments reproducible.
