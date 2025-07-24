from flask import Flask, render_template, request, send_file, url_for
import qrcode
import os
from datetime import datetime

app = Flask(__name__)

# Directory to save generated QR codes
QR_FOLDER = "static"
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Display the QR generator form and handle QR code generation.
    """
    qr_path = None

    if request.method == "POST":
        data = request.form.get("data")

        if data:
            # Create a unique filename based on timestamp
            filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            qr_path = os.path.join(QR_FOLDER, filename)

            # Generate and save QR code
            img = qrcode.make(data)
            img.save(qr_path)

            # Render template with generated QR code
            return render_template("index.html", qr_path=qr_path)

    return render_template("index.html")

@app.route("/download/<filename>")
def download_qr(filename):
    """
    Download the generated QR code file.
    """
    file_path = os.path.join(QR_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
