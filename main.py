from flask import Flask, request, jsonify
from pdf2image import convert_from_path
import gdown
import io
import requests
import os

app = Flask(__name__)

# URL del webhook receptor en Make (pon aquí tu webhook real si lo necesitas más adelante)
MAKE_WEBHOOK = "https://hook.make.com/tu_webhook_receptor"

@app.route("/", methods=["POST"])
def recibir_pdf():
    data = request.json

    file_id = data.get("fileId")
    file_name = data.get("fileName", "archivo.pdf")

    if not file_id:
        return jsonify({"error": "fileId is required"}), 400

    # Descargar el PDF desde Google Drive
    pdf_url = f"https://drive.google.com/uc?id={file_id}"
    output_pdf = file_name
    gdown.download(pdf_url, output_pdf, quiet=False)

    # Convertir la primera página del PDF a imagen
    images = convert_from_path(output_pdf, dpi=200)
    img_byte_arr = io.BytesIO()
    images[0].save(img_byte_arr, format='JPEG')

    # Enviar la imagen a Make (si se usa)
    if MAKE_WEBHOOK and "make.com" in MAKE_WEBHOOK:
        files = {
            "file": ("pagina1.jpg", img_byte_arr.getvalue(), "image/jpeg")
        }
        response = requests.post(MAKE_WEBHOOK, files=files)
        return jsonify({"status": "ok", "make_response": response.status_code})

    # O responder la imagen directamente (opcional)
    return jsonify({"status": "ok", "message": "Imagen generada, no enviada a Make"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # Usa el puerto que Render asigna
    app.run(host="0.0.0.0", port=port)
