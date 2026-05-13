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

k8s-apply:
	kubectl apply -f k8s/

k8s-status:
	kubectl get all -n data-pipelines

k8s-logs:
	kubectl logs -n data-pipelines -l app=weather-etl

k8s-clean:
	kubectl delete namespace data-pipelines