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
