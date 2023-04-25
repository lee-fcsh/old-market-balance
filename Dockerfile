FROM python:3.8.14

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && \
    pip install -U wheel && \
    pip install -U setuptools

RUN pip install otree==3.3.10

WORKDIR /app

COPY requirements* .
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8000

CMD ["otree", "prodserver", "0.0.0.0:8000"]
