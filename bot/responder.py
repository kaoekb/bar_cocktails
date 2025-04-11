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
