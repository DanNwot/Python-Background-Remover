from rembg import remove
from PIL import Image

input_path = "entrada.jpg"
output_path = "saida.png"

with Image.open(input_path) as img:
    output = remove(img)
    output.save(output_path)

print("Fundo removido com sucesso!")
