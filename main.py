from flask import Flask, request, send_file, jsonify
from pdf2image import convert_from_path
import gdown
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def convertir_pdf_a_imagen():
    data = request.get_json()
    file_id = data.get("fileId")
    file_name = data.get("fileName", "archivo.pdf")

    if not file_id:
        return jsonify({"error": "Se requiere 'fileId'"}), 400

    # Descargar PDF desde Google Drive
    pdf_url = f"https://drive.google.com/uc?id={file_id}"
    output_pdf = os.path.join("/tmp", file_name)
    gdown.download(pdf_url, output_pdf, quiet=False)

    # Convertir PDF a imagen
    images = convert_from_path(output_pdf, dpi=200)
    output_image_path = os.path.join("/tmp", "output.jpg")
    images[0].save(output_image_path, "JPEG")

    return jsonify({"message": "Imagen generada con éxito", "image_path": "/output.jpg"}), 200

@app.route("/output.jpg", methods=["GET"])
def obtener_imagen():
    output_image_path = os.path.join("/tmp", "output.jpg")
    if not os.path.exists(output_image_path):
        return jsonify({"error": "La imagen aún no se ha generado"}), 404
    return send_file(output_image_path, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


