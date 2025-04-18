from flask import Flask, request, jsonify
from pdf2image import convert_from_path
import gdown
import io
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def recibir_pdf():
    data = request.json
    file_id = data.get("fileId")
    file_name = data.get("fileName", "archivo.pdf")

    if not file_id:
        return jsonify({"error": "Falta fileId"}), 400

    # Descargar PDF desde Google Drive
    pdf_url = f"https://drive.google.com/uc?id={file_id}"
    output_pdf = "archivo.pdf"
    gdown.download(pdf_url, output_pdf, quiet=False)

    try:
        # Convertir la primera página a imagen
        images = convert_from_path(output_pdf, dpi=200)
        img_path = "pagina1.jpg"
        images[0].save(img_path, format="JPEG")
        return jsonify({"status": "ok", "message": f"Imagen generada como {img_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Correr la app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

