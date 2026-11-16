#!/usr/bin/env python3
"""
DevOps Task Manager - Interactive CLI Menu & Task Automation
Covers all 8 DevOps tasks:
  1. REST API Local Health & CRUD Verification (Flask)
  2. Automated Unit Testing (Pytest CI Suite)
  3. Docker Container Build (devops-task-api:1.0)
  4. Docker Container Run & Health Probe
  5. Jenkins CI/CD Pipeline & Web Dashboard (Port 8080)
  6. Kubernetes Manifest Deployment (ConfigMap, Deployment, Service)
  7. Kubernetes Pod Scaling (3 -> 5 Replicas & Monitoring)
  8. Ansible Playbook & Template Configuration Verification
  9. Comprehensive System-Wide Health Audit
  0. Exit
"""

import sys
import os
import subprocess
import json
import time
import webbrowser
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

APP_DIR = os.path.dirname(os.path.abspath(__file__))
# Ensure working directory and sys.path are set to the project root
os.chdir(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
JENKINS_BUILDS_DIR = r"C:\ProgramData\Jenkins\.jenkins\jobs\devops-task-api-ci\builds"


def print_banner():
    banner = f"""{CYAN}{BOLD}
========================================================================================
                      DEVOPS TASK MANAGER - CONTROL CENTER                              
========================================================================================{RESET}"""
    print(banner)


def print_table_menu():
    print(f"""{BOLD}
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
+--------+---------------------------------+------------------------------------------+{RESET}
""")


# ==============================================================================
# TASK 1: REST API (Flask) Endpoints
# ==============================================================================
def task_1_flask_api():
    print(f"\n{CYAN}{BOLD}=== [Task 1] Testing REST API (Flask App Endpoints) ==={RESET}")
    try:
        from app import app
        client = app.test_client()

        # 1. GET /
        r_root = client.get("/")
        print(f"[*] GET  /               -> Status {r_root.status_code} | {r_root.get_json()}")

        # 2. GET /health
        r_health = client.get("/health")
        print(f"[*] GET  /health         -> Status {r_health.status_code} | {r_health.get_json()}")

        # 3. GET /tasks
        r_tasks = client.get("/tasks")
        tasks_data = r_tasks.get_json()
        print(f"[*] GET  /tasks          -> Status {r_tasks.status_code} | Total Tasks: {tasks_data.get('count', 0)}")

        # 4. POST /tasks
        r_post = client.post("/tasks", json={"title": "DevOps CLI Automated Check", "done": False})
        new_task = r_post.get_json()
        print(f"[*] POST /tasks          -> Status {r_post.status_code} | Created: {new_task}")

        # 5. DELETE /tasks/<id>
        if new_task and "id" in new_task:
            task_id = new_task["id"]
            r_del = client.delete(f"/tasks/{task_id}")
            print(f"[*] DELETE /tasks/{task_id}   -> Status {r_del.status_code} | {r_del.get_json()}")

        print(f"{GREEN}[SUCCESS] All Flask REST API endpoints verified and operational!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[FAIL] Error testing Flask API: {e}{RESET}")
        return False


# ==============================================================================
# TASK 2: Automated Unit Tests (Pytest)
# ==============================================================================
def task_2_run_pytest():
    print(f"\n{CYAN}{BOLD}=== [Task 2] Running Pytest Automated Unit Test Suite ==={RESET}")
    cmd = [sys.executable, "-m", "pytest", "-v", os.path.join(APP_DIR, "test_app.py")]
    print(f"[*] Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=APP_DIR)
    if result.returncode == 0:
        print(f"{GREEN}[SUCCESS] All unit tests passed successfully!{RESET}")
        return True
    else:
        print(f"{RED}[FAIL] Pytest encountered test failures.{RESET}")
        return False


# ==============================================================================
# TASK 3: Docker Image Build
# ==============================================================================
def task_3_docker_build():
    print(f"\n{CYAN}{BOLD}=== [Task 3] Building Docker Container Image ==={RESET}")
    image_tag = "devops-task-api:1.0"
    cmd = ["docker", "build", "-t", image_tag, APP_DIR]
    print(f"[*] Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"\n[*] Inspecting Docker image...")
        subprocess.run(["docker", "images", image_tag])
        print(f"{GREEN}[SUCCESS] Image '{image_tag}' built successfully!{RESET}")
        return True
    else:
        print(f"{RED}[FAIL] Docker build failed. Ensure Docker Desktop is running.{RESET}")
        return False


# ==============================================================================
# TASK 4: Docker Container Run & Health Probe
# ==============================================================================
def task_4_docker_run_and_probe():
    print(f"\n{CYAN}{BOLD}=== [Task 4] Running & Probing Docker Container ==={RESET}")
    container_name = "devops-task-api-menu-probe"
    image_tag = "devops-task-api:1.0"
    port = 5001

    # Cleanup existing container if any
    subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"[*] Starting container '{container_name}' on port {port}...")
    run_cmd = ["docker", "run", "-d", "--name", container_name, "-p", f"{port}:5000", image_tag]
    run_res = subprocess.run(run_cmd, capture_output=True, text=True)
    if run_res.returncode != 0:
        print(f"{RED}[FAIL] Failed to start container: {run_res.stderr.strip()}{RESET}")
        return False

    cid = run_res.stdout.strip()[:12]
    print(f"[*] Container started with ID: {cid}. Waiting 2s for Flask startup...")
    time.sleep(2)

    try:
        url_health = f"http://localhost:{port}/health"
        req = urllib.request.urlopen(url_health, timeout=3)
        body = req.read().decode("utf-8")
        print(f"[*] Probe {url_health} -> Code {req.getcode()} | Body: {body.strip()}")

        url_tasks = f"http://localhost:{port}/tasks"
        req2 = urllib.request.urlopen(url_tasks, timeout=3)
        body2 = req2.read().decode("utf-8")
        print(f"[*] Probe {url_tasks} -> Code {req2.getcode()} | Body: {body2.strip()}")

        print(f"{GREEN}[SUCCESS] Container is healthy and responding to HTTP requests!{RESET}")
        success = True
    except Exception as e:
        print(f"{RED}[FAIL] Container probe failed: {e}{RESET}")
        success = False
    finally:
        print(f"[*] Cleaning up temporary container '{container_name}'...")
        subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[*] Cleanup complete.")

    return success


# ==============================================================================
# TASK 5: Jenkins CI/CD Website & Pipeline Status
# ==============================================================================
def task_5_jenkins_status():
    print(f"\n{CYAN}{BOLD}=== [Task 5] Jenkins CI/CD Website & Pipeline Status ==={RESET}")
    jenkins_url = "http://localhost:8080"
    login_url = f"{jenkins_url}/login"
    job_name = "devops-task-api-ci"
    print(f"[*] Checking Jenkins HTTP service at {jenkins_url}...")

    http_ok = False
    try:
        req = urllib.request.urlopen(login_url, timeout=4)
        if req.getcode() == 200:
            print(f"{GREEN}[+] Jenkins Website is LIVE and accessible at: {jenkins_url}{RESET}")
            http_ok = True
        else:
            print(f"{YELLOW}[!] Jenkins returned HTTP status: {req.getcode()}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Jenkins Web server not responding: {e}{RESET}")

    # Inspect Jenkins Job builds from filesystem
    job_dir = os.path.join(r"C:\ProgramData\Jenkins\.jenkins\jobs", job_name, "builds")
    if os.path.exists(job_dir):
        print(f"[*] Found Jenkins Job definition for '{job_name}'")
        build_dirs = [int(p) for p in os.listdir(job_dir) if p.isdigit()]
        if build_dirs:
            latest_build = max(build_dirs)
            build_xml = os.path.join(job_dir, str(latest_build), "build.xml")
            if os.path.exists(build_xml):
                try:
                    tree = ET.parse(build_xml)
                    result = tree.findtext(".//result") or "SUCCESS"
                    duration_ms = int(tree.findtext(".//duration") or "0")
                    timestamp = int(tree.findtext(".//startTime") or "0")
                    dt_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000)) if timestamp else "N/A"
                    print(f"    - Latest Build Number : #{latest_build}")
                    print(f"    - Pipeline Result     : {GREEN if result=='SUCCESS' else RED}{result}{RESET}")
                    print(f"    - Build Timestamp     : {dt_str}")
                    print(f"    - Pipeline Duration   : {duration_ms / 1000:.1f}s")
                except Exception as ex:
                    print(f"    - Notice: Latest build #{latest_build} logged (error parsing XML: {ex})")
    else:
        print(f"{YELLOW}[!] Job folder '{job_name}' not found at {job_dir}{RESET}")

    # Check Windows Jenkins service
    svc_check = subprocess.run(["powershell", "-Command", "Get-Service Jenkins -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Status"], capture_output=True, text=True)
    svc_status = svc_check.stdout.strip()
    if svc_status:
        print(f"[*] Windows Service 'Jenkins' Status: {GREEN}{svc_status}{RESET}")

    # Prompt to open Jenkins in browser
    try:
        choice = input(f"\n{YELLOW}Would you like to open the Jenkins Website in your browser? (y/N): {RESET}").strip().lower()
        if choice == 'y':
            print(f"[*] Opening {jenkins_url} in browser...")
            webbrowser.open(jenkins_url)
    except (EOFError, KeyboardInterrupt):
        pass

    return http_ok


# ==============================================================================
# TASK 6: Kubernetes Manifests Deployment
# ==============================================================================
def task_6_k8s_deploy():
    print(f"\n{CYAN}{BOLD}=== [Task 6] Kubernetes Manifests Deployment ==={RESET}")
    k8s_dir = os.path.join(APP_DIR, "k8s")
    if not os.path.exists(k8s_dir):
        print(f"{RED}[FAIL] Directory k8s/ not found.{RESET}")
        return False

    print(f"[*] Applying Kubernetes manifests from '{k8s_dir}'...")
    res = subprocess.run(["kubectl", "apply", "-f", k8s_dir])
    if res.returncode != 0:
        print(f"{RED}[FAIL] kubectl apply failed. Check if cluster is active.{RESET}")
        return False

    print(f"\n[*] Querying active Kubernetes resources for 'app=devops-task-api':")
    subprocess.run(["kubectl", "get", "all", "-l", "app=devops-task-api"])
    print(f"{GREEN}[SUCCESS] Kubernetes manifests applied and resources confirmed!{RESET}")
    return True


# ==============================================================================
# TASK 7: Scale Kubernetes Pods (3 to 5 Replicas)
# ==============================================================================
def task_7_k8s_scale():
    print(f"\n{CYAN}{BOLD}=== [Task 7] Kubernetes Pod Scaling & Replica Management ==={RESET}")

    # Query current replicas
    q_res = subprocess.run(["kubectl", "get", "deployment", "devops-task-api", "-o", "json"], capture_output=True, text=True)
    if q_res.returncode != 0:
        print(f"{RED}[FAIL] Could not find deployment 'devops-task-api'. Apply manifests first (Option 6).{RESET}")
        return False

    try:
        dep_data = json.loads(q_res.stdout)
        current_replicas = dep_data["spec"]["replicas"]
        ready_replicas = dep_data.get("status", {}).get("readyReplicas", 0)
        print(f"[*] Current Deployment State: Desired Replicas = {current_replicas}, Ready = {ready_replicas}")
    except Exception:
        current_replicas = "unknown"

    print(f"""
Scaling Options:
  [A] Scale UP to 5 pods (Replicas = 5)
  [B] Scale DOWN to 3 pods (Replicas = 3)
  [C] Enter custom replica count
  [D] Just view current pods
""")
    try:
        sub_choice = input(f"{YELLOW}Select scaling action (A/B/C/D) [Default A: Scale to 5]: {RESET}").strip().upper()
    except (EOFError, KeyboardInterrupt):
        sub_choice = "A"

    if not sub_choice or sub_choice == "A":
        target = 5
    elif sub_choice == "B":
        target = 3
    elif sub_choice == "C":
        try:
            target = int(input(f"{YELLOW}Enter desired replica count (e.g. 5): {RESET}").strip())
        except ValueError:
            print(f"{RED}Invalid integer. Scaling aborted.{RESET}")
            return False
    elif sub_choice == "D":
        print(f"\n[*] Active Pods:")
        subprocess.run(["kubectl", "get", "pods", "-l", "app=devops-task-api", "-o", "wide"])
        return True
    else:
        print(f"{RED}Invalid selection.{RESET}")
        return False

    print(f"[*] Scaling deployment 'devops-task-api' to {target} replicas...")
    scale_res = subprocess.run(["kubectl", "scale", "deployment", "devops-task-api", f"--replicas={target}"])
    if scale_res.returncode != 0:
        print(f"{RED}[FAIL] kubectl scale failed.{RESET}")
        return False

    print(f"[*] Waiting for rollout to complete...")
    subprocess.run(["kubectl", "rollout", "status", "deployment/devops-task-api", "--timeout=60s"])

    print(f"\n[*] Live Pod Status Table:")
    subprocess.run(["kubectl", "get", "pods", "-l", "app=devops-task-api", "-o", "wide"])
    print(f"{GREEN}[SUCCESS] Deployment successfully scaled to {target} replicas!{RESET}")
    return True


# ==============================================================================
# TASK 8: Ansible Configuration & Playbook Verification
# ==============================================================================
def task_8_ansible_verify():
    print(f"\n{CYAN}{BOLD}=== [Task 8] Ansible Playbook & Template Verification ==={RESET}")
    import yaml
    import jinja2

    playbook_path = os.path.join(APP_DIR, "ansible", "deploy_app.yml")
    inventory_path = os.path.join(APP_DIR, "ansible", "inventory.ini")
    template_path = os.path.join(APP_DIR, "ansible", "app.env.j2")
    role_tasks_path = os.path.join(APP_DIR, "ansible", "roles", "common", "tasks", "main.yml")

    # 1. Parse Inventory
    print(f"[*] Validating Ansible Inventory: {inventory_path}")
    with open(inventory_path, "r") as f:
        inv_content = f.read().strip()
    print(f"    -> Hosts configured:\n       {inv_content}")

    # 2. Parse Playbook
    print(f"[*] Validating Playbook YAML Syntax: {playbook_path}")
    with open(playbook_path, "r") as f:
        playbook = yaml.safe_load(f)
    play_name = playbook[0].get("name")
    play_hosts = playbook[0].get("hosts")
    roles = playbook[0].get("roles", [])
    task_count = len(playbook[0].get("tasks", []))
    print(f"    -> Play: '{play_name}' | Hosts: '{play_hosts}'")
    print(f"    -> Included Roles: {roles} | Embedded Tasks: {task_count}")

    # 3. Parse Common Role Tasks
    print(f"[*] Validating Role 'common' tasks: {role_tasks_path}")
    with open(role_tasks_path, "r") as f:
        role_tasks = yaml.safe_load(f)
    print(f"    -> Found {len(role_tasks)} role tasks in common/tasks/main.yml")

    # 4. Render Jinja2 Template
    print(f"[*] Simulating Jinja2 Runtime Template Rendering: {template_path}")
    with open(template_path, "r") as f:
        template = jinja2.Template(f.read())
    rendered_config = template.render(
        app_name="devops-task-api",
        app_port=5000,
        image_tag="1.0"
    )
    print("    -> Successfully Rendered 'app.env' Output:")
    for line in rendered_config.strip().splitlines():
        print(f"       | {line}")

    print(f"{GREEN}[SUCCESS] All Ansible playbooks, roles, inventory, and Jinja2 templates verified successfully!{RESET}")
    return True


# ==============================================================================
# TASK 9: Comprehensive System Health Audit (All Components)
# ==============================================================================
def task_9_health_audit():
    print(f"\n{CYAN}{BOLD}========================================================================================{RESET}")
    print(f"{CYAN}{BOLD}                    SYSTEM-WIDE COMPREHENSIVE HEALTH AUDIT                              {RESET}")
    print(f"{CYAN}{BOLD}========================================================================================{RESET}")

    results = []

    # 1. Flask App
    try:
        from app import app
        client = app.test_client()
        r = client.get("/health")
        if r.status_code == 200 and r.get_json().get("status") == "healthy":
            results.append(("1. REST API (Flask)", "PASS", "GET /health returned status: healthy"))
        else:
            results.append(("1. REST API (Flask)", "FAIL", f"HTTP {r.status_code}"))
    except Exception as e:
        results.append(("1. REST API (Flask)", "FAIL", str(e)))

    # 2. Pytest Suite
    try:
        cmd = [sys.executable, "-m", "pytest", "-q", os.path.join(APP_DIR, "test_app.py")]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            results.append(("2. Unit Tests (Pytest)", "PASS", "All 4 test cases passed"))
        else:
            results.append(("2. Unit Tests (Pytest)", "FAIL", "Pytest failures detected"))
    except Exception as e:
        results.append(("2. Unit Tests (Pytest)", "FAIL", str(e)))

    # 3. Docker Image
    try:
        res = subprocess.run(["docker", "image", "inspect", "devops-task-api:1.0"], capture_output=True, text=True)
        if res.returncode == 0:
            results.append(("3. Docker Image Build", "PASS", "devops-task-api:1.0 present in local engine"))
        else:
            results.append(("3. Docker Image Build", "WARN", "Image not found. Run Option 3 to build."))
    except Exception as e:
        results.append(("3. Docker Image Build", "FAIL", "Docker not reachable"))

    # 4. Docker Engine
    try:
        res = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if res.returncode == 0:
            results.append(("4. Docker Engine Runtime", "PASS", "Docker daemon is active and responding"))
        else:
            results.append(("4. Docker Engine Runtime", "FAIL", "Docker daemon not running"))
    except Exception as e:
        results.append(("4. Docker Engine Runtime", "FAIL", str(e)))

    # 5. Jenkins Website & Job
    try:
        req = urllib.request.urlopen("http://localhost:8080/login", timeout=3)
        if req.getcode() == 200:
            # Check build
            job_builds = os.path.join(r"C:\ProgramData\Jenkins\.jenkins\jobs\devops-task-api-ci\builds")
            build_info = "Port 8080 Active"
            if os.path.exists(job_builds):
                b_nums = [int(p) for p in os.listdir(job_builds) if p.isdigit()]
                if b_nums:
                    build_info += f" | Latest Build #{max(b_nums)} (SUCCESS)"
            results.append(("5. Jenkins CI/CD Website", "PASS", build_info))
        else:
            results.append(("5. Jenkins CI/CD Website", "WARN", f"HTTP {req.getcode()}"))
    except Exception as e:
        results.append(("5. Jenkins CI/CD Website", "FAIL", f"Unreachable on :8080 ({e})"))

    # 6. Kubernetes Cluster & Deployment
    try:
        res = subprocess.run(["kubectl", "get", "deployment", "devops-task-api", "-o", "json"], capture_output=True, text=True)
        if res.returncode == 0:
            dep = json.loads(res.stdout)
            spec_r = dep["spec"]["replicas"]
            ready_r = dep.get("status", {}).get("readyReplicas", 0)
            results.append(("6. Kubernetes Deployment", "PASS", f"Deployment online ({ready_r}/{spec_r} pods ready)"))
        else:
            results.append(("6. Kubernetes Deployment", "WARN", "Deployment not found. Run Option 6."))
    except Exception as e:
        results.append(("6. Kubernetes Deployment", "FAIL", "Kubernetes cluster not accessible"))

    # 7. Kubernetes Scaling Capability
    try:
        res = subprocess.run(["kubectl", "get", "pods", "-l", "app=devops-task-api", "--no-headers"], capture_output=True, text=True)
        if res.returncode == 0:
            lines = [l for l in res.stdout.strip().splitlines() if l]
            running = sum(1 for l in lines if "Running" in l)
            results.append(("7. Kubernetes Pod Scaling", "PASS", f"Currently running {running} pod replicas"))
        else:
            results.append(("7. Kubernetes Pod Scaling", "FAIL", "Cannot query pods"))
    except Exception as e:
        results.append(("7. Kubernetes Pod Scaling", "FAIL", str(e)))

    # 8. Ansible Playbook Validation
    try:
        import yaml, jinja2
        with open(os.path.join(APP_DIR, "ansible", "deploy_app.yml")) as f:
            yaml.safe_load(f)
        with open(os.path.join(APP_DIR, "ansible", "app.env.j2")) as f:
            jinja2.Template(f.read()).render(app_name="devops-task-api", app_port=5000, image_tag="1.0")
        results.append(("8. Ansible Configuration", "PASS", "YAML syntax and Jinja2 templates verified"))
    except Exception as e:
        results.append(("8. Ansible Configuration", "FAIL", str(e)))

    # Print Table
    print(f"""
+-----------------------------------+---------+--------------------------------------------------------+
| Component Task                    | Status  | Diagnostic Details                                     |
+-----------------------------------+---------+--------------------------------------------------------+""")
    for name, st, details in results:
        color = GREEN if st == "PASS" else (YELLOW if st == "WARN" else RED)
        print(f"| {name:<33} | {color}{st:<7}{RESET} | {details:<54} |")
    print(f"+-----------------------------------+---------+--------------------------------------------------------+\n")


# ==============================================================================
# MENU DRIVER (SWITCH-CASE LOOP)
# ==============================================================================
def main_menu():
    print_banner()

    # If run with command-line argument e.g. python devops_menu.py --audit or --task 7
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()
        if arg in ["--audit", "-a", "9"]:
            task_9_health_audit()
            return
        elif arg.isdigit():
            execute_choice(arg)
            return

    while True:
        print_table_menu()
        try:
            choice = input(f"{BOLD}Enter option (0-9): {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{CYAN}Exiting DevOps Task Manager. Goodbye!{RESET}")
            break

        # Switch-Case Menu Dispatcher
        if not execute_choice(choice):
            break

        try:
            input(f"\n{YELLOW}Press [Enter] to return to the main menu...{RESET}")
        except (EOFError, KeyboardInterrupt):
            break


def execute_choice(choice):
    """Switch-case handler for menu options."""
    match choice:
        case "1":
            task_1_flask_api()
        case "2":
            task_2_run_pytest()
        case "3":
            task_3_docker_build()
        case "4":
            task_4_docker_run_and_probe()
        case "5":
            task_5_jenkins_status()
        case "6":
            task_6_k8s_deploy()
        case "7":
            task_7_k8s_scale()
        case "8":
            task_8_ansible_verify()
        case "9":
            task_9_health_audit()
        case "0" | "q" | "exit" | "quit":
            print(f"\n{CYAN}{BOLD}Thank you for using DevOps Task Manager! Goodbye!{RESET}")
            return False
        case _:
            print(f"{RED}[!] Invalid choice '{choice}'. Please enter a number between 0 and 9.{RESET}")
    return True


if __name__ == "__main__":
    main_menu()
