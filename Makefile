.PHONY: test lint compose-up compose-down compose-reset

test:
	pytest

lint:
	pylint src utils
	pylint tests --disable=duplicate-code

compose-up:
	docker compose up --build

compose-down:
	docker compose down

compose-reset:
	docker compose down -v
	docker compose up --build