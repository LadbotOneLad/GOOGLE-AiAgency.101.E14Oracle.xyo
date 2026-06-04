# Helm Chart for HC-AOL
# Directory structure:
# helm-hc-aol/
# ├── Chart.yaml
# ├── values.yaml
# └── templates/
#     ├── namespace.yaml
#     ├── configmap.yaml
#     ├── secret.yaml
#     ├── pvc.yaml
#     ├── deployment.yaml
#     ├── service.yaml
#     ├── ingress.yaml
#     ├── hpa.yaml
#     └── rbac.yaml

# ============================================================================
# Chart.yaml
# ============================================================================

apiVersion: v2
name: hc-aol
description: HC-AOL - Human-Controlled Autonomous Orchestration Layer
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - hc-aol
  - orchestration
  - kubernetes
home: https://github.com/yourname/codex665
sources:
  - https://github.com/yourname/codex665
maintainers:
  - name: Rebecca
    email: rebecca@example.com

---

# ============================================================================
# values.yaml
# ============================================================================

# Replica count
replicaCount: 3

# Image configuration
image:
  repository: codex665-api
  pullPolicy: Always
  tag: "latest"

# Service configuration
service:
  type: LoadBalancer
  port: 80
  targetPort: 8000

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  hosts:
    - host: hc-aol.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: hc-aol-tls
      hosts:
        - hc-aol.example.com

# Resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# HPA configuration
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

# Persistence
persistence:
  enabled: true
  size: 10Gi
  storageClassName: "standard"
  mountPath: /var/log/hc-aol

# Environment variables
env:
  HC_AOL_LOG_DIR: "/var/log/hc-aol"
  FLASK_ENV: "production"

# Secrets (set via --set or separate values file)
secrets:
  jwtSecret: "change-this-in-production"

# Security context
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

# Node affinity
nodeSelector: {}

tolerations: []

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - hc-aol
        topologyKey: kubernetes.io/hostname

---

# ============================================================================
# templates/deployment.yaml
# ============================================================================

apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "hc-aol.fullname" . }}
  labels:
    {{ include "hc-aol.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{ include "hc-aol.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{ include "hc-aol.selectorLabels" . | nindent 8 }}
    spec:
      serviceAccountName: {{ include "hc-aol.serviceAccountName" . }}
      securityContext:
        {{ toYaml .Values.securityContext | nindent 8 }}
      
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        envFrom:
        - configMapRef:
            name: {{ include "hc-aol.fullname" . }}-config
        env:
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: {{ include "hc-aol.fullname" . }}-secrets
              key: jwt-secret
        resources:
          {{ toYaml .Values.resources | nindent 12 }}
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        {{- if .Values.persistence.enabled }}
        volumeMounts:
        - name: logs
          mountPath: {{ .Values.persistence.mountPath }}
        {{- end }}
      {{- if .Values.persistence.enabled }}
      volumes:
      - name: logs
        persistentVolumeClaim:
          claimName: {{ include "hc-aol.fullname" . }}-pvc
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{ toYaml . | nindent 8 }}
      {{- end }}

---

# ============================================================================
# templates/_helpers.tpl
# ============================================================================

{{- define "hc-aol.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "hc-aol.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "hc-aol.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.AppVersion | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "hc-aol.labels" -}}
helm.sh/chart: {{ include "hc-aol.chart" . }}
{{ include "hc-aol.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "hc-aol.selectorLabels" -}}
app.kubernetes.io/name: {{ include "hc-aol.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "hc-aol.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "hc-aol.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
