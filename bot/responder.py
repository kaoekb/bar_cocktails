# responder.py

import openai

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

def generate_image(client, prompt: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response.data[0].url
