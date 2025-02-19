from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    """Serve the main display page."""
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def receive_scan():
    """Receive barcode/QR code from scanner."""
    data = request.json
    scanned_id = data.get("scanned_code", "Unknown")
    scanner_user = data.get("scanner_user", "Unknown Scanner")  # New field for scanner name
    
    print(f"📡 Received scan: {scanned_id} from {scanner_user}")

    # Send update to all connected clients
    socketio.emit("update_scan", {"scanned_id": scanned_id, "scanner_user": scanner_user})

    return jsonify({"status": "success", "message": "Scan received!"})

if __name__ == "__main__":
    print("🚀 Server running on http://localhost:5050")
    socketio.run(app, host="0.0.0.0", port=5050, debug=True)
