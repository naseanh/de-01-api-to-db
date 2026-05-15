# Phase 5 Roadmap

## Objective

Phase 5 focuses on Kubernetes packaging, scheduled execution, and operational deployment maturity.

The goal is to move from raw Kubernetes manifests to reusable Helm-based deployment packaging.

## Primary Goals

- Package Kubernetes resources using Helm
- Replace static YAML duplication with templates
- Add `values.yaml` configuration
- Support ETL execution as both Job and CronJob
- Add environment-specific deployment values
- Improve deployment automation with Makefile commands
- Document Helm install, upgrade, rollback, and uninstall workflows

## Planned Enhancements

- Helm chart scaffold
- PostgreSQL Helm templates
- ETL Job Helm template
- ETL CronJob Helm template
- `values.yaml`
- optional `values-dev.yaml`
- Helm deployment runbook
- README Phase 5 architecture update
- Phase 5 retrospective

## Engineering Concepts Practiced

- Helm charts
- Kubernetes templating
- `values.yaml` configuration
- release lifecycle management
- scheduled ETL execution
- deployment reuse
- environment-specific configuration
- install/upgrade/rollback/uninstall workflows

## Success Criteria

Phase 5 is complete when:

- Kubernetes resources deploy through Helm
- ETL can run as a Kubernetes Job
- ETL can run as a Kubernetes CronJob
- Configuration is driven through Helm values
- Helm release can be installed, upgraded, rolled back, and uninstalled
- Documentation clearly explains the deployment lifecycle
