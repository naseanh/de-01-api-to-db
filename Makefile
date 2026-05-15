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

.PHONY: helm-lint helm-template helm-install helm-upgrade helm-uninstall helm-status helm-history helm-rollback

helm-lint:
	helm lint helm/weather-etl

helm-template:
	helm template weather-etl helm/weather-etl

helm-install:
	helm upgrade --install weather-etl helm/weather-etl \
		--namespace data-pipelines \
		--create-namespace \
		--wait

helm-upgrade:
	helm upgrade weather-etl helm/weather-etl \
		--namespace data-pipelines \
		--wait

helm-uninstall:
	helm uninstall weather-etl -n data-pipelines

helm-status:
	helm status weather-etl -n data-pipelines

helm-history:
	helm history weather-etl -n data-pipelines

helm-rollback:
	helm rollback weather-etl 1 -n data-pipelines