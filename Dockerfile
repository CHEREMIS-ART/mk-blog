FROM python:3.11-slim

WORKDIR /app

ENV POETRY_VERSION=2.2.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
