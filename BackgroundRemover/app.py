from flask import Flask, render_template, request, send_file
from rembg import remove, new_session
from PIL import Image, ImageFilter
import io

app = Flask(__name__)

# Modelo de alta qualidade
session = new_session("isnet-general-use")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]

        if not file:
            return "Nenhum arquivo enviado"

        img = Image.open(file.stream).convert("RGBA")

        # Remoção com alpha matting (recorte refinado)
        output = remove(
            img,
            session=session,
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=8
        )

        # Suavização leve de bordas
        output = output.filter(ImageFilter.SMOOTH)

        img_io = io.BytesIO()
        output.save(img_io, format="PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
