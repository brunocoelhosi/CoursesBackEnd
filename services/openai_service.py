import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_course_image(title: str, description: str) -> str:
    prompt = (
        f"Ilustração educacional moderna e inclusiva sobre o curso "
        f"'{title}'. Tema: {description}. "
        "Estilo flat design, cores suaves, ambiente educacional, "
        "sem texto na imagem."
    )

    response = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024"
    )

    return response.data[0].url