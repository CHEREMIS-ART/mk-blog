POETRY_RUN = poetry run

.PHONY: help
help:
	@echo "Доступные команды:"
	@echo "  make install        - установить зависимости (включая dev)"
	@echo "  make run            - запустить приложение локально (uvicorn)"
	@echo "  make lint           - запустить ruff и black --check"
	@echo "  make fmt            - отформатировать код (ruff --fix + black)"
	@echo "  make typecheck      - запустить mypy"
	@echo "  make test           - запустить pytest"
	@echo "  make pre-commit     - прогнать pre-commit на всех файлах"
	@echo "  make pre-commit-install - установить git-хуки pre-commit"
	@echo "  make up             - запустить сервисы через docker-compose"
	@echo "  make down           - остановить сервисы и удалить контейнеры"
	@echo "  make logs           - показать логи api-сервиса"
	@echo "  make build          - пересобрать образы api и worker"

.PHONY: install
install:
	poetry install --extras dev

.PHONY: run
run:
	$(POETRY_RUN) uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: lint
lint:
	$(POETRY_RUN) ruff check src tests
	$(POETRY_RUN) black --check src tests

.PHONY: fmt
fmt:
	$(POETRY_RUN) ruff check --fix src tests
	$(POETRY_RUN) black src tests

.PHONY: typecheck
typecheck:
	$(POETRY_RUN) mypy src

.PHONY: test
test:
	ENV=test $(POETRY_RUN) pytest

.PHONY: pre-commit-install
pre-commit-install:
	$(POETRY_RUN) pre-commit install

.PHONY: pre-commit
pre-commit:
	$(POETRY_RUN) pre-commit run --all-files

.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down

.PHONY: logs
logs:
	docker-compose logs -f api

.PHONY: build
build:
	docker-compose build --no-cache api worker
