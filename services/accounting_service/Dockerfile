FROM python:3.11-slim-buster

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.7.1 && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --only=main --no-root --no-interaction --no-cache

COPY . .

CMD ["python3", "/app/src/start.py"]

EXPOSE 8003