FROM python:3.12-slim


# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1


# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1


WORKDIR /app


# System deps for psycopg
RUN apt-get update \
&& apt-get install -y --no-install-recommends gcc libpq-dev \
&& rm -rf /var/lib/apt/lists/*


# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip \
&& pip install -r requirements.txt


# Project files
COPY . .