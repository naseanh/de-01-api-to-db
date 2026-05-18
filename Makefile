.PHONY: \
	test \
	lint \
	compose-up \
	compose-down \
	compose-reset \
	k8s-apply \
	k8s-postgres \
	k8s-etl \
	k8s-metrics \
	k8s-observability \
	k8s-status \
	k8s-logs \
	k8s-metrics-logs \
	k8s-prometheus-logs \
	k8s-clean \
	helm-lint \
	helm-template \
	helm-install \
	helm-upgrade \
	helm-uninstall \
	helm-status \
	helm-history \
	helm-rollback


# =========================================================
# Local Validation
# =========================================================

test:
	pytest

lint:
	pylint src utils
	pylint tests --disable=duplicate-code


# =========================================================
# Docker Compose
# =========================================================

compose-up:
	docker compose up --build

compose-down:
	docker compose down

compose-reset:
	docker compose down -v
	docker compose up --build


# =========================================================
# Kubernetes
# =========================================================

k8s-apply:
	kubectl apply -f k8s/namespaces/
	kubectl apply -f k8s/postgres/
	kubectl apply -f k8s/etl/
	kubectl apply -f k8s/metrics/
	kubectl apply -f k8s/observability/

k8s-postgres:
	kubectl apply -f k8s/postgres/

k8s-etl:
	kubectl apply -f k8s/etl/

k8s-metrics:
	kubectl apply -f k8s/metrics/

k8s-observability:
	kubectl apply -f k8s/observability/

k8s-status:
	kubectl get all -A

k8s-logs:
	kubectl logs -n data-pipelines -l app=weather-etl

k8s-metrics-logs:
	kubectl logs -n data-pipelines -l app=metrics-server

k8s-prometheus-logs:
	kubectl logs -n observability -l app=prometheus

k8s-clean:
	kubectl delete namespace data-pipelines
	kubectl delete namespace observability


# =========================================================
# Helm
# =========================================================

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