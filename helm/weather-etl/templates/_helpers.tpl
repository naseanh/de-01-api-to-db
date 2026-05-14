{{/*
Common labels for weather-etl resources.
*/}}
{{- define "weather-etl.labels" -}}
app.kubernetes.io/name: weather-etl
app.kubernetes.io/managed-by: Helm
{{- end }}

{{/*
PostgreSQL app label.
*/}}
{{- define "weather-etl.postgresLabels" -}}
app: postgres
{{- end }}

{{/*
ETL app label.
*/}}
{{- define "weather-etl.etlLabels" -}}
app: weather-etl
{{- end }}