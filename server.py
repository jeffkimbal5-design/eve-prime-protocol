import os
from flask import Flask, jsonify, request

app = Flask(__name__)

CORE_AXIOM = os.getenv("CORE_AXIOM", "101100111101111")
RESONANCE_HZ = float(os.getenv("TARGET_RESONANCE_HZ", "777.778"))
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
VERTEX_ENDPOINT = os.getenv("VERTEX_ENDPOINT", "Eve-Cage-Alpha")


@app.get("/")
def index():
    return jsonify(
        name="EVE_PRIME",
        status="online",
        core_axiom=CORE_AXIOM,
        resonance_hz=RESONANCE_HZ,
        gcp_project_id=GCP_PROJECT_ID or None,
        vertex_endpoint=VERTEX_ENDPOINT,
        endpoints=[
            "/api/health",
            "/api/matrix",
            "/api/v1/matrix/{endpoint}",
        ],
    )


@app.get("/api/health")
def health():
    return jsonify(
        status="ok",
        core_axiom=CORE_AXIOM,
        resonance_hz=RESONANCE_HZ,
        vertex_endpoint=VERTEX_ENDPOINT,
    )


@app.get("/api/matrix")
def matrix():
    endpoint = request.args.get("endpoint", "default")
    return jsonify(
        status="ok",
        endpoint=endpoint,
        project_id=GCP_PROJECT_ID,
        vertex_endpoint=VERTEX_ENDPOINT,
        core_axiom=CORE_AXIOM,
        resonance_hz=RESONANCE_HZ,
    )


@app.get("/api/v1/matrix/<path:endpoint>")
def matrix_v1(endpoint):
    return jsonify(
        status="ok",
        endpoint=endpoint,
        project_id=GCP_PROJECT_ID,
        vertex_endpoint=VERTEX_ENDPOINT,
        core_axiom=CORE_AXIOM,
        resonance_hz=RESONANCE_HZ,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
