# DevOps Task Manager API & Orchestration Suite

A comprehensive DevOps project showcasing an automated CI/CD lifecycle, containerization, orchestration, and configuration management for a RESTful Task Management service.

---

## Project Overview

This repository demonstrates an end-to-end DevOps engineering workflow:
- **REST API**: Python Flask service with health monitoring and CRUD task endpoints.
- **Automated Testing**: Pytest suite verifying endpoint contracts and business logic.
- **Containerization**: Dockerfile building a lightweight, production-ready Python 3.12 image.
- **CI/CD Automation**: Declarative Jenkins pipeline automating testing, artifact packaging, and build archiving.
- **Kubernetes Orchestration**: Declarative manifests for Deployment, ConfigMap, and NodePort Service.
- **Dynamic Pod Scaling**: Automated scaling from 3 to 5 pod replicas with zero downtime rollout.
- **Configuration Management**: Ansible playbooks, common roles, and Jinja2 environment templates.
- **Interactive Control Center CLI**: A switch-case menu-driven CLI in PowerShell and Python covering all 8 tasks.

---

## Interactive Menu-Driven CLI (`devops-menu`)

An interactive command-line interface provides single-keypress execution and health auditing for all 8 DevOps tasks:

```text
========================================================================================
                      DEVOPS TASK MANAGER - CONTROL CENTER                              
========================================================================================

+--------+---------------------------------+------------------------------------------+
| Option | Task Component                  | Action / Description                     |
+--------+---------------------------------+------------------------------------------+
|  [1]   | REST API (Flask Endpoints)      | Test Local Health & CRUD Operations      |
|  [2]   | Automated Unit Tests (Pytest)   | Run Full Automated CI Test Suite         |
|  [3]   | Docker Container Build          | Build 'devops-task-api:1.0' Image        |
|  [4]   | Docker Container Run & Probe    | Spin Up Container & Test Health (p:5001) |
|  [5]   | Jenkins CI/CD Website           | Check Port 8080 & Latest Build Pipeline  |
|  [6]   | Kubernetes Deployment           | Apply ConfigMap, Deployment & Service    |
|  [7]   | Kubernetes Pod Scaling          | Scale Pods (3 -> 5) & Monitor Status     |
|  [8]   | Ansible Playbook Automation     | Verify Roles, Tasks & Jinja2 Template    |
+--------+---------------------------------+------------------------------------------+
|  [9]   | System-Wide Health Audit        | Audit All 8 Components Status in Table   |
|  [0]   | Exit Menu                       | Close Control Center CLI                 |
+--------+---------------------------------+------------------------------------------+
```

### Running the CLI

#### Windows PowerShell:
```powershell
cd devops-task-api
powershell -ExecutionPolicy Bypass -File .\devops-menu.ps1
```

#### Windows Command Prompt / Instant Launcher:
```cmd
devops-menu.bat
```

#### Python CLI (Cross-Platform):
```bash
python devops_menu.py
```

*Non-interactive health audit:*
```bash
python devops_menu.py --audit
```

---

## Component Breakdown & Verification

### 1. REST API (Flask)
- **File**: `app.py`
- **Endpoints**:
  - `GET /` &mdash; Service status and available endpoints
  - `GET /health` &mdash; Health check returning `{"status": "healthy"}`
  - `GET /tasks` &mdash; Retrieve task list
  - `POST /tasks` &mdash; Create a new task (`{"title": "...", "done": bool}`)
  - `DELETE /tasks/<id>` &mdash; Delete a task by ID

### 2. Automated Testing (Pytest)
- **File**: `test_app.py`
- **Command**: `pytest -v`
- Verifies all 4 test cases (`test_health_endpoint`, `test_get_tasks`, `test_create_task`, `test_delete_task`).

### 3 & 4. Docker Containerization
- **File**: `Dockerfile`
- **Build**: `docker build -t devops-task-api:1.0 .`
- **Run**: `docker run -d -p 5000:5000 devops-task-api:1.0`

### 5. Jenkins CI/CD Pipeline
- **File**: `Jenkinsfile`
- **Access**: `http://localhost:8080` (Job: `devops-task-api-ci`)
- Pipeline stages:
  1. **Checkout**: Git SCM checkout
  2. **Install Dependencies**: `pip install -r requirements.txt`
  3. **Run Automated Tests**: Automated `pytest` execution
  4. **Package Build Artifact**: Generates `dist/devops-task-api-build-<BUILD_NUMBER>.zip`
  5. **Post / Archive**: Archives build zip artifacts

### 6. Kubernetes Deployment & Service
- **Manifests**: `k8s/`
  - `configmap.yaml`: Runtime environment parameters (`APP_PORT`, `APP_ENV`, `LOG_LEVEL`)
  - `deployment.yaml`: Replicated pod deployment (container port 5000)
  - `service.yaml`: NodePort Service exposing port 5000 on node port 30080
- **Apply**: `kubectl apply -f k8s/`

### 7. Kubernetes Pod Scaling
- **Scale Up (3 &rarr; 5 Replicas)**:
  ```bash
  kubectl scale deployment devops-task-api --replicas=5
  kubectl rollout status deployment/devops-task-api
  ```
- **Scale Down (5 &rarr; 3 Replicas)**:
  ```bash
  kubectl scale deployment devops-task-api --replicas=3
  ```

### 8. Ansible Configuration Management
- **Directory**: `ansible/`
  - `inventory.ini`: Target hosts specification
  - `deploy_app.yml`: Main provisioning playbook
  - `roles/common/tasks/main.yml`: Directory layout and metadata provisioning
  - `app.env.j2`: Jinja2 template for dynamic environment configuration

---

## Repository Structure

```text
devops-task-api/
|-- app.py                     # Flask REST API implementation
|-- test_app.py                # Pytest unit tests
|-- requirements.txt           # Python package dependencies
|-- Dockerfile                 # Container image specification
|-- Jenkinsfile                # CI/CD declarative pipeline
|-- devops_menu.py             # Python interactive menu-driven CLI
|-- devops-menu.ps1            # PowerShell interactive menu-driven CLI
|-- devops-menu.bat            # Windows batch shortcut launcher
|-- README.md                  # Project documentation & execution guide
|-- k8s/                       # Kubernetes manifests
|   |-- configmap.yaml
|   |-- deployment.yaml
|   |-- service.yaml
`-- ansible/                   # Ansible automation & configuration
    |-- inventory.ini
    |-- deploy_app.yml
    |-- app.env.j2
    `-- roles/
        `-- common/
            `-- tasks/
                `-- main.yml
```

---

## Author

- **Shreyanshu Raj** ([@ShreyanshuRaj06](https://github.com/ShreyanshuRaj06))
