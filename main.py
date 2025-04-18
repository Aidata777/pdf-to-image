from flask import Flask, request, jsonify
from pdf2image import convert_from_path
import gdown
import io
import requests

app = Flask(__name__)

MAKE_WEBHOOK = "https://hook.make.com/tu_webhook_receptor"

@app.route("/", methods=["POST"])
def recibir_pdf():
    data = request.json
    file_id = data.get("fileId")
    file_name = data.get("fileName", "archivo.pdf")

    pdf_url = f"https://drive.google.com/uc?id={file_id}"
    output_pdf = "archivo.pdf"
    gdown.download(pdf_url, output_pdf, quiet=False)

    images = convert_from_path(output_pdf, dpi=200)
    img_byte_arr = io.BytesIO()
    images[0].save(img_byte_arr, format='JPEG')

    files = {
        "file": ("pagina1.jpg", img_byte_arr.getvalue(), "image/jpeg")
    }
    response = requests.post(MAKE_WEBHOOK, files=files)

    return jsonify({"status": "ok", "make_response": response.status_code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
