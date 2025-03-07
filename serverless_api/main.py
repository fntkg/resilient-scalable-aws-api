from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Hello, world!"})


@app.route("/status")
def status():
    return jsonify({"status": "running", "uptime": "N/A"})  # Add logic as needed


if __name__ == "__main__":
    # Listen on all interfaces so the container is accessible externally
    app.run(host="0.0.0.0", port=80)
