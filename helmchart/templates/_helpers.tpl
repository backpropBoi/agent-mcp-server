{{/*
Return the image subpath based on environment and domain
*/}}
{{- define "chart.imageSubpath" -}}{{- if eq .Values.domain "common" }}core{{- else if eq .Values.environment "prod" }}{{ .Values.domain }}{{- else }}qa-{{ .Values.domain }}{{- end }}{{- end }}

{{/*
Return the full image name
*/}}
{{- define "chart.fullImage" -}}{{- $subpath := include "chart.imageSubpath" . -}}{{- printf "mn-cosi-opsmate-docker-local.artifactory-mn-espoo3.int.net.nokia.com/lyra/%s/mcp-server:%s" $subpath .Values.tag }}{{- end }}

{{/*
Return ingress host
*/}}
{{- define "chart.ingressHost" -}}{{- if .Values.ingress.host }}{{ .Values.ingress.host }}{{- else if eq .Values.environment "prod" }}{{ printf "mcp-%s.lyra.dyn.nesc.nokia.net" .Values.domain }}{{- else }}{{ printf "qa-mcp-%s.lyra.dyn.nesc.nokia.net" .Values.domain }}{{- end }}{{- end }}