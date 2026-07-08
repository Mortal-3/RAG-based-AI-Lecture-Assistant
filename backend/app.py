import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.utils import create_chunks, get_status, process_videos, query_text

app = Flask(__name__)
CORS(app)

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"success": True, "data": get_status()})

@app.route("/api/process-videos", methods=["POST"])
def api_process_videos():
    try:
        result = process_videos()
        return jsonify({"success": True, "data": result})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

@app.route("/api/create-chunks", methods=["POST"])
def api_create_chunks():
    try:
        result = create_chunks()
        return jsonify({"success": True, "data": result})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

@app.route("/api/query", methods=["POST"])
def api_query():
    payload = request.get_json(silent=True) or {}
    question = payload.get("question", "").strip()
    if not question:
        return jsonify({"success": False, "error": "Question is required."}), 400

    try:
        result = query_text(question)
        return jsonify({"success": True, "data": result})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", "5051"))
    app.run(host="0.0.0.0", port=port, debug=True)
