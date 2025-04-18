from flask import Flask, request, jsonify, send_file
from pdf2image import convert_from_path
import gdown
import io
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def convertir_pdf():
    data = request.json
    file_id = data.get("fileId")
    file_name = data.get("fileName", "archivo.pdf")

    if not file_id:
        return jsonify({"error": "Falta el ID del archivo"}), 400

    # Descargar el archivo PDF desde Google Drive
    pdf_url = f"https://drive.google.com/uc?id={file_id}"
    output_pdf = file_name
    gdown.download(pdf_url, output_pdf, quiet=False)

    # Convertir la primera página a imagen
    images = convert_from_path(output_pdf, dpi=200)
    images[0].save("output.jpg", format='JPEG')

    return jsonify({"status": "ok", "message": "Imagen generada con éxito"})

@app.route("/output.jpg", methods=["GET"])
def servir_imagen():
    if os.path.exists("output.jpg"):
        return send_file("output.jpg", mimetype="image/jpeg")
    else:
        return jsonify({"error": "Imagen no encontrada"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

