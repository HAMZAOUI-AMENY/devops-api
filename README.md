# DevOps API Project

A production-ready REST API built with FastAPI, featuring comprehensive DevOps practices including containerization, CI/CD, security scanning, observability, and Kubernetes deployment.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Usage](#docker-usage)
- [Kubernetes Deployment](#kubernetes-deployment)
- [API Documentation](#api-documentation)
- [Observability](#observability)
- [Security](#security)
- [CI/CD Pipeline](#cicd-pipeline)
- [Testing](#testing)
- [Project Structure](#project-structure)

## 🎯 Overview

This project demonstrates end-to-end DevOps practices by implementing a simple REST API with full observability, security scanning, containerization, and Kubernetes deployment. Built as part of a DevOps course project.

**Key Technologies:**
- **Backend:** FastAPI (Python 3.11)
- **Containerization:** Docker
- **Orchestration:** Kubernetes (Minikube/KinD)
- **CI/CD:** GitHub Actions
- **Metrics:** Prometheus Client
- **Security:** Bandit (SAST), OWASP ZAP (DAST)
- **Testing:** pytest

## ✨ Features

- ✅ RESTful API with CRUD operations
- ✅ Prometheus metrics integration
- ✅ Structured logging
- ✅ Request tracing
- ✅ Docker containerization
- ✅ Kubernetes deployment with health checks
- ✅ Automated CI/CD pipeline
- ✅ Security scanning (SAST + DAST)
- ✅ Automated testing
- ✅ Resource limits and scaling

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Kubernetes Service │  (NodePort: 30007)
│   (Load Balancer)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   FastAPI Pod(s)    │  (Port: 8000)
│  - Metrics          │
│  - Logging          │
│  - Health Checks    │
└─────────────────────┘
```

## 📦 Prerequisites

- Python 3.11+
- Docker Desktop
- Minikube or KinD
- kubectl
- Git

## 🚀 Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/amenihamzaoui/devops-api.git
cd devops-api
```

### 2. Install Dependencies

```bash
pip install -r app/requirements.txt
```

### 3. Run Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. Run Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/ -v
```

## 🐳 Docker Usage

### Build Docker Image

```bash
docker build -t amenihamzaoui/devops-api:latest .
```

### Run Container

```bash
docker run -d -p 8000:8000 --name devops-api amenihamzaoui/devops-api:latest
```

### Using Docker Compose

```bash
docker-compose up -d
```

### Stop Container

```bash
docker stop devops-api
docker rm devops-api
```

## ☸️ Kubernetes Deployment

### Minikube Deployment

#### Step 1: Start Minikube

```bash
minikube start --driver=docker
```

#### Step 2: Build Image in Minikube

```cmd
@FOR /f "tokens=*" %i IN ('minikube docker-env') DO @%i
docker build -t amenihamzaoui/devops-api:latest .
```

#### Step 3: Deploy to Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

#### Step 4: Verify Deployment

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# View logs
kubectl logs -f deployment/devops-api
```

#### Step 5: Access the API

```bash
# Get service URL
minikube service devops-api-service --url

# Or open in browser
minikube service devops-api-service
```

### Kubernetes Commands

```bash
# Scale deployment
kubectl scale deployment devops-api --replicas=3

# View pod details
kubectl describe pod <pod-name>

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/sh

# Port forward
kubectl port-forward deployment/devops-api 8000:8000

# Delete resources
kubectl delete -f k8s/
```

## 📖 API Documentation

### Base URL
- **Local:** `http://localhost:8000`
- **Minikube:** `http://<minikube-ip>:30007`

### Endpoints

#### Health Check
```bash
GET /health
```
**Response:**
```json
{
  "status": "ok"
}
```

#### Root Endpoint
```bash
GET /
```
**Response:**
```json
{
  "message": "Hello, DevOps!"
}
```

#### Get Item
```bash
GET /items/{item_id}
```
**Example:**
```bash
curl http://localhost:8000/items/42
```
**Response:**
```json
{
  "item_id": 42,
  "name": "Item 42",
  "price": 420
}
```

#### Create Item
```bash
POST /items/
Content-Type: application/json

{
  "name": "Laptop",
  "description": "Gaming laptop",
  "price": 1000,
  "tax": 0.2
}
```
**Example:**
```bash
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","price":1000,"tax":0.2}'
```

#### Update Item
```bash
PUT /items/{item_id}
```

#### Delete Item
```bash
DELETE /items/{item_id}
```

#### Tracing Example
```bash
GET /trace-example/{user_id}
```

#### Metrics (Prometheus)
```bash
GET /metrics
```

## 📊 Observability

### Metrics

The API exposes Prometheus-compatible metrics at `/metrics`:

**Custom Metrics:**
- `request_count_total` - Total number of API requests
- `request_latency_seconds` - Request latency histogram

**System Metrics:**
- Python GC metrics
- Process memory usage
- CPU usage
- Open file descriptors

**Access Metrics:**
```bash
curl http://localhost:8000/metrics
```

### Logging

Structured logging with timestamps and log levels:

```python
# View application logs
kubectl logs -f deployment/devops-api

# Example log output:
# 2025-01-15 12:34:56 INFO Root endpoint called
# 2025-01-15 12:34:57 INFO Item requested: 42
# 2025-01-15 12:34:58 ERROR Invalid item_id: -1
```

### Tracing

Basic request tracing implemented via logging:

```bash
curl http://localhost:8000/trace-example/123
```

Logs will show:
```
2025-01-15 12:34:59 INFO Tracing request for user: 123
```

## 🔒 Security

### SAST (Static Application Security Testing)

**Tool:** Bandit

```bash
# Run locally
pip install bandit
bandit -r app/ -ll
```

Automated in CI/CD pipeline on every push.

### DAST (Dynamic Application Security Testing)

**Tool:** OWASP ZAP

Runs in GitHub Actions pipeline:
- Baseline scan for common vulnerabilities
- Full scan for comprehensive testing

### Security Features

- Input validation using Pydantic models
- HTTP exception handling
- No hardcoded secrets
- Container runs as non-root user
- Resource limits in Kubernetes

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

**1. Secure CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)

Stages:
1. **Build & Test**
   - Install dependencies
   - Run pytest
   - Lint with flake8

2. **Security SAST**
   - Run Bandit scan
   - Generate security report

3. **Docker Build**
   - Build Docker image
   - Push to Docker Hub

4. **DAST Scan**
   - Deploy container
   - Run OWASP ZAP scans

5. **Deploy**
   - Create KinD cluster
   - Deploy to Kubernetes
   - Verify deployment

### Trigger CI/CD

```bash
git add .
git commit -m "Update application"
git push origin main
```

### Required GitHub Secrets

Set these in your repository settings (Settings → Secrets and variables → Actions):

- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or access token

## 🧪 Testing

### Run Tests

```bash
# Install dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Test Coverage

Current tests cover:
- Root endpoint
- Health check
- Item operations
- Math operations (sum)

## 📁 Project Structure

```
devops-api/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD pipeline configuration
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application
│   └── requirements.txt       # Python dependencies
├── k8s/
│   ├── deployment.yaml        # Kubernetes deployment
│   └── service.yaml           # Kubernetes service
├── tests/
│   └── test_api.py           # API tests
├── .gitignore
├── Dockerfile                # Container image definition
├── docker-compose.yml        # Docker Compose configuration
├── pyproject.toml           # Python project configuration
└── README.md                # This file
```


**Built for DevOps learning**