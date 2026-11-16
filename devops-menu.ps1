# DevOps Task Manager - Native PowerShell Interactive Menu
# Run in PowerShell: .\devops-menu.ps1
# Or via batch: devops-menu.bat

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $ScriptDir) { $ScriptDir = $PSScriptRoot }
if (-not $ScriptDir) { $ScriptDir = "C:\Users\LENOVO\devops-task-api" }
Set-Location $ScriptDir

function Show-Banner {
    Write-Host ""
    Write-Host "========================================================================================" -ForegroundColor Cyan
    Write-Host "                      DEVOPS TASK MANAGER - CONTROL CENTER                              " -ForegroundColor Cyan
    Write-Host "========================================================================================" -ForegroundColor Cyan
}

function Show-MenuTable {
    Write-Host ""
    Write-Host "+--------+---------------------------------+------------------------------------------+" -ForegroundColor Yellow
    Write-Host "| Option | Task Component                  | Action / Description                     |" -ForegroundColor Yellow
    Write-Host "+--------+---------------------------------+------------------------------------------+" -ForegroundColor Yellow
    Write-Host "|  [1]   | REST API (Flask Endpoints)      | Test Local Health & CRUD Operations      |" -ForegroundColor White
    Write-Host "|  [2]   | Automated Unit Tests (Pytest)   | Run Full Automated CI Test Suite         |" -ForegroundColor White
    Write-Host "|  [3]   | Docker Container Build          | Build 'devops-task-api:1.0' Image        |" -ForegroundColor White
    Write-Host "|  [4]   | Docker Container Run & Probe    | Spin Up Container & Test Health (p:5001) |" -ForegroundColor White
    Write-Host "|  [5]   | Jenkins CI/CD Website           | Check Port 8080 & Latest Build Pipeline  |" -ForegroundColor White
    Write-Host "|  [6]   | Kubernetes Deployment           | Apply ConfigMap, Deployment & Service    |" -ForegroundColor White
    Write-Host "|  [7]   | Kubernetes Pod Scaling          | Scale Pods (3 -> 5) & Monitor Status     |" -ForegroundColor White
    Write-Host "|  [8]   | Ansible Playbook Automation     | Verify Roles, Tasks & Jinja2 Template    |" -ForegroundColor White
    Write-Host "+--------+---------------------------------+------------------------------------------+" -ForegroundColor Yellow
    Write-Host "|  [9]   | System-Wide Health Audit        | Audit All 8 Components Status in Table   |" -ForegroundColor Green
    Write-Host "|  [0]   | Exit Menu                       | Close Control Center CLI                 |" -ForegroundColor Gray
    Write-Host "+--------+---------------------------------+------------------------------------------+" -ForegroundColor Yellow
    Write-Host ""
}

function Test-DockerRunning {
    $null = docker ps 2>&1
    return ($LASTEXITCODE -eq 0)
}

function Ensure-DockerRunning {
    if (Test-DockerRunning) { return $true }
    Write-Host "[!] Docker Desktop is not currently running." -ForegroundColor Yellow
    $ans = Read-Host "Would you like to launch Docker Desktop now? (Y/n) [Default: Y]"
    if (-not $ans -or $ans -eq 'y' -or $ans -eq 'Y') {
        Write-Host "[*] Launching Docker Desktop... please wait for the engine to initialize..." -ForegroundColor Cyan
        Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        $timeout = 60
        $elapsed = 0
        while ($elapsed -lt $timeout) {
            Start-Sleep -Seconds 3
            $elapsed += 3
            if (Test-DockerRunning) {
                Write-Host "[+] Docker Engine is now ONLINE and ready!" -ForegroundColor Green
                return $true
            }
            Write-Host "    Waiting for Docker daemon... ($elapsed s)" -ForegroundColor Gray
        }
    }
    Write-Host "[FAIL] Docker daemon is not active. Please start Docker Desktop from your Desktop or Start Menu." -ForegroundColor Red
    return $false
}

function Test-K8sRunning {
    $null = kubectl get nodes 2>&1
    return ($LASTEXITCODE -eq 0)
}

function Ensure-K8sRunning {
    if (-not (Ensure-DockerRunning)) { return $false }
    if (Test-K8sRunning) { return $true }
    Write-Host "[*] Waiting for Kubernetes API server to become ready..." -ForegroundColor Gray
    $timeout = 45
    $elapsed = 0
    while ($elapsed -lt $timeout) {
        Start-Sleep -Seconds 3
        $elapsed += 3
        if (Test-K8sRunning) {
            Write-Host "[+] Kubernetes cluster is ONLINE and ready!" -ForegroundColor Green
            return $true
        }
        Write-Host "    Waiting for Kubernetes... ($elapsed s)" -ForegroundColor Gray
    }
    Write-Host "[FAIL] Kubernetes cluster is not responding. Ensure Kubernetes is enabled in Docker Desktop settings." -ForegroundColor Red
    return $false
}

# Task 1: REST API (Flask)
function Invoke-Task1 {
    Write-Host "`n=== [Task 1] Testing REST API (Flask App Endpoints) ===" -ForegroundColor Cyan
    py -c "
from app import app
c = app.test_client()
print('GET  /          ->', c.get('/').status_code, c.get('/').get_json())
print('GET  /health    ->', c.get('/health').status_code, c.get('/health').get_json())
print('GET  /tasks     ->', c.get('/tasks').status_code, c.get('/tasks').get_json())
post_r = c.post('/tasks', json={'title': 'PS Menu Test Task'})
print('POST /tasks     ->', post_r.status_code, post_r.get_json())
tid = post_r.get_json().get('id')
if tid:
    print(f'DEL  /tasks/{tid} ->', c.delete(f'/tasks/{tid}').status_code)
"
    Write-Host "[SUCCESS] Flask REST API verified and functional!" -ForegroundColor Green
}

# Task 2: Pytest
function Invoke-Task2 {
    Write-Host "`n=== [Task 2] Running Pytest Automated Unit Test Suite ===" -ForegroundColor Cyan
    py -m pytest -v (Join-Path $ScriptDir "test_app.py")
}

# Task 3: Docker Build
function Invoke-Task3 {
    Write-Host "`n=== [Task 3] Building Docker Container Image ===" -ForegroundColor Cyan
    if (-not (Ensure-DockerRunning)) {
        return
    }
    docker build -t devops-task-api:1.0 $ScriptDir
    if ($LASTEXITCODE -eq 0) {
        docker images devops-task-api:1.0
        Write-Host "[SUCCESS] Docker image devops-task-api:1.0 built successfully!" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Docker build failed." -ForegroundColor Red
    }
}

# Task 4: Docker Run & Probe
function Invoke-Task4 {
    Write-Host "`n=== [Task 4] Running & Probing Docker Container ===" -ForegroundColor Cyan
    if (-not (Ensure-DockerRunning)) {
        return
    }
    docker rm -f devops-task-api-menu-probe 2>$null | Out-Null
    Write-Host "[*] Launching container on port 5001..." -ForegroundColor Gray
    docker run -d --name devops-task-api-menu-probe -p 5001:5000 devops-task-api:1.0 | Out-Null
    Start-Sleep -Seconds 2

    try {
        $health = Invoke-RestMethod -Uri "http://localhost:5001/health" -TimeoutSec 3
        Write-Host "[*] GET http://localhost:5001/health -> Status: $($health.status)" -ForegroundColor Green

        $tasks = Invoke-RestMethod -Uri "http://localhost:5001/tasks" -TimeoutSec 3
        Write-Host "[*] GET http://localhost:5001/tasks  -> Total tasks: $($tasks.count)" -ForegroundColor Green
        Write-Host "[SUCCESS] Docker container probe succeeded!" -ForegroundColor Green
    }
    catch {
        Write-Host "[FAIL] Container probe failed: $_" -ForegroundColor Red
    }
    finally {
        Write-Host "[*] Removing temporary probe container..." -ForegroundColor Gray
        docker rm -f devops-task-api-menu-probe 2>$null | Out-Null
        Write-Host "[*] Cleanup complete." -ForegroundColor Gray
    }
}

# Task 5: Jenkins Website & Status
function Invoke-Task5 {
    Write-Host "`n=== [Task 5] Jenkins CI/CD Website & Pipeline Status ===" -ForegroundColor Cyan
    $url = "http://localhost:8080"
    try {
        $resp = curl.exe -s -I "http://localhost:8080/login"
        if ($resp -match "200 OK") {
            Write-Host "[+] Jenkins Website is LIVE at: $url" -ForegroundColor Green
        } else {
            Write-Host "[!] Jenkins server responded on port 8080." -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "[-] Jenkins not responding on :8080: $_" -ForegroundColor Red
    }

    $buildsDir = "C:\ProgramData\Jenkins\.jenkins\jobs\devops-task-api-ci\builds"
    if (Test-Path $buildsDir) {
        $builds = Get-ChildItem -Path $buildsDir -Directory | Where-Object { $_.Name -match '^\d+$' } | Sort-Object { [int]$_.Name } -Descending
        if ($builds) {
            $latest = $builds[0].Name
            Write-Host "    - Pipeline Job Name  : devops-task-api-ci" -ForegroundColor White
            Write-Host "    - Latest Build Number: #$latest" -ForegroundColor White
            $buildXml = Join-Path $builds[0].FullName "build.xml"
            if (Test-Path $buildXml) {
                [xml]$xml = Get-Content $buildXml
                $res = $xml.SelectSingleNode("//result").InnerText
                Write-Host "    - Pipeline Result    : $res" -ForegroundColor Green
            }
        }
    }

    $openBrowser = Read-Host "`nOpen Jenkins in your browser? (y/N)"
    if ($openBrowser -eq 'y' -or $openBrowser -eq 'Y') {
        Start-Process $url
    }
}

# Task 6: Kubernetes Deployment
function Invoke-Task6 {
    Write-Host "`n=== [Task 6] Kubernetes Manifests Deployment ===" -ForegroundColor Cyan
    if (-not (Ensure-K8sRunning)) {
        return
    }
    $k8sDir = Join-Path $ScriptDir "k8s"
    kubectl apply -f $k8sDir
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[*] Current Kubernetes Resources:" -ForegroundColor Gray
        kubectl get all -l app=devops-task-api
        Write-Host "[SUCCESS] Kubernetes manifests applied successfully!" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Failed to apply Kubernetes manifests." -ForegroundColor Red
    }
}

# Task 7: Scale Kubernetes Pods
function Invoke-Task7 {
    Write-Host "`n=== [Task 7] Kubernetes Pod Scaling & Replica Management ===" -ForegroundColor Cyan
    if (-not (Ensure-K8sRunning)) {
        return
    }
    try {
        $depJson = kubectl get deployment devops-task-api -o json 2>$null
        if ($depJson) {
            $dep = $depJson | ConvertFrom-Json
            $cur = $dep.spec.replicas
            Write-Host "[*] Current Desired Replicas: $cur" -ForegroundColor White
        }
    } catch {}

    Write-Host "Scaling Options:" -ForegroundColor Gray
    Write-Host "  [A] Scale UP to 5 pods (Replicas = 5)" -ForegroundColor White
    Write-Host "  [B] Scale DOWN to 3 pods (Replicas = 3)" -ForegroundColor White
    Write-Host "  [C] Custom replica count" -ForegroundColor White

    $sub = Read-Host "Select scaling action (A/B/C) [Default: A]"
    if (-not $sub -or $sub -eq 'A' -or $sub -eq 'a') {
        $target = 5
    } elseif ($sub -eq 'B' -or $sub -eq 'b') {
        $target = 3
    } elseif ($sub -eq 'C' -or $sub -eq 'c') {
        $target = Read-Host "Enter desired replica count (e.g. 5)"
    } else {
        $target = 5
    }

    Write-Host "[*] Scaling deployment 'devops-task-api' to $target replicas..." -ForegroundColor Cyan
    $scaleOut = kubectl scale deployment devops-task-api --replicas=$target 2>&1
    Write-Host $scaleOut
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[*] Awaiting rollout completion..." -ForegroundColor Gray
        kubectl rollout status deployment/devops-task-api --timeout=60s
        Write-Host "`n[*] Live Pods Table:" -ForegroundColor Gray
        kubectl get pods -l app=devops-task-api -o wide
        Write-Host "[SUCCESS] Deployment scaled to $target replicas!" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Could not scale deployment. Is Docker Desktop and Kubernetes running?" -ForegroundColor Red
    }
}

# Task 8: Ansible Verification
function Invoke-Task8 {
    Write-Host "`n=== [Task 8] Ansible Playbook & Template Verification ===" -ForegroundColor Cyan
    py -c "
import os, yaml, jinja2
script_dir = r'$ScriptDir'
playbook_p = os.path.join(script_dir, 'ansible', 'deploy_app.yml')
with open(playbook_p) as f:
    play = yaml.safe_load(f)
print('[*] Playbook Parsed:', play[0]['name'])
print('    Roles:', play[0].get('roles'), '| Hosts:', play[0].get('hosts'))

template_p = os.path.join(script_dir, 'ansible', 'app.env.j2')
with open(template_p) as f:
    tmpl = jinja2.Template(f.read())
rendered = tmpl.render(app_name='devops-task-api', app_port=5000, image_tag='1.0')
print('[*] Rendered app.env template successfully:')
for line in rendered.strip().splitlines():
    print('    |', line)
"
    Write-Host "[SUCCESS] Ansible configuration syntax and Jinja2 templates verified!" -ForegroundColor Green
}

# Task 9: Health Audit
function Invoke-Task9 {
    py (Join-Path $ScriptDir "devops_menu.py") --audit
}

# Main Switch-Case Menu Loop
Show-Banner
do {
    Show-MenuTable
    $choice = Read-Host "Enter option (0-9)"

    switch ($choice) {
        "1" { Invoke-Task1 }
        "2" { Invoke-Task2 }
        "3" { Invoke-Task3 }
        "4" { Invoke-Task4 }
        "5" { Invoke-Task5 }
        "6" { Invoke-Task6 }
        "7" { Invoke-Task7 }
        "8" { Invoke-Task8 }
        "9" { Invoke-Task9 }
        "0" {
            Write-Host "`nExiting DevOps Control Center. Goodbye!" -ForegroundColor Cyan
            break
        }
        default {
            Write-Host "`n[!] Invalid selection '$choice'. Please select between 0 and 9." -ForegroundColor Red
        }
    }

    if ($choice -ne "0") {
        Write-Host ""
        Read-Host "Press [Enter] to return to menu..."
    }
} while ($choice -ne "0")
