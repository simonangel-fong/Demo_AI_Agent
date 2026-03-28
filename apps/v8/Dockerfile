FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    jq \
    procps \
    iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

RUN useradd -m -u 1000 appuser

COPY ./app /code
RUN chown -R appuser:appuser /code

USER appuser
# USER root

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]