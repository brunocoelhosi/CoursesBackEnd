import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from django.conf import settings

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

COURSE_IMAGE_DIR = Path(settings.MEDIA_ROOT) / "courses"
COURSE_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

def generate_course_image(title: str, description: str) -> str:
    prompt = (
        f"Ilustração educacional moderna e inclusiva sobre o curso "
        f"'{title}'. Tema: {description}. "
        "Estilo flat design, cores suaves, ambiente educacional, "
        "sem texto na imagem."
    )

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    filename = f"course_{title.lower().replace(' ', '_')}.png"
    file_path = COURSE_IMAGE_DIR / filename

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    #return file_path
    return f"http://localhost:8000{settings.MEDIA_URL}courses/{filename}"
    #return f"{settings.MEDIA_URL}courses/{filename}"