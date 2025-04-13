import openai
from PIL import Image
import requests
from io import BytesIO
# from rembg import remove


def get_openai_client(api_key: str):
    return openai.OpenAI(api_key=api_key)

def generate_response(client, prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()

def generate_image_url(client, prompt: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response.data[0].url

# def generate_image_sticker(client, prompt: str) -> BytesIO:
#     image_url = generate_image_url(client, prompt)
#     image_data = requests.get(image_url).content
#     img = Image.open(BytesIO(image_data)).convert("RGBA")

#     output = BytesIO()
#     # img.save(output, format="WEBP")
#     img.save(output, format="WEBP", lossless=True)
#     output.name = "sticker.webp"
#     output.seek(0)
#     return output

def generate_image_sticker(client, prompt: str) -> BytesIO:
    image_url = generate_image_url(client, prompt)
    image_data = requests.get(image_url).content
    img = Image.open(BytesIO(image_data)).convert("RGBA")

    output = BytesIO()
    img.save(output, format="PNG")
    output.name = "sticker.png"
    output.seek(0)
    return output

# def generate_image_sticker(client, prompt: str) -> BytesIO:
#     image_url = generate_image_url(client, prompt)
#     image_data = requests.get(image_url).content
#     img = Image.open(BytesIO(image_data)).convert("RGBA")

#     # Приводим размер к максимуму 512x512
#     max_size = (512, 512)
#     img.thumbnail(max_size, Image.LANCZOS)

#     output = BytesIO()
#     img.save(output, format="WEBP", lossless=True)
#     output.name = "sticker.webp"
#     output.seek(0)
#     return output

# def generate_image_sticker(client, prompt: str) -> BytesIO:
#     image_url = generate_image_url(client, prompt)
#     image_data = requests.get(image_url).content
#     img = Image.open(BytesIO(image_data)).convert("RGBA")

#     # Удаляем фон
#     img_no_bg = Image.open(BytesIO(remove(image_data))).convert("RGBA")

#     # Приводим размер к 512x512
#     max_size = (512, 512)
#     img_no_bg.thumbnail(max_size, Image.LANCZOS)

#     output = BytesIO()
#     img_no_bg.save(output, format="WEBP", lossless=True)
#     output.name = "sticker.webp"
#     output.seek(0)
#     return output