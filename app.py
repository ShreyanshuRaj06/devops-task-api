import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory task list (no external DB needed)
tasks = [
    {"id": 1, "title": "Complete DevOps Component 1", "done": True},
    {"id": 2, "title": "Deploy on Kubernetes", "done": False},
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "DevOps Task Manager API",
        "status": "running",
        "endpoints": ["GET /health", "GET /tasks", "POST /tasks"]
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"count": len(tasks), "tasks": tasks}), 200


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Task title is required"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": bool(data.get("done", False))
    }
    tasks.append(new_task)
    return jsonify(new_task), 201


if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", 5000))
    app.run(host="0.0.0.0", port=port)