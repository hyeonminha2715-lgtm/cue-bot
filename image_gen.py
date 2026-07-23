"""
OpenAI 이미지 생성 API로 포스터 배경 이미지를 만드는 모듈.
인스타그램 세로형(4:5) 포스터에 맞춰 세로 비율로 생성한다.
글자가 깨지는 걸 막기 위해, 여기서는 '글자 없는 배경'만 생성하고
제목 텍스트는 poster.py에서 별도로 입힌다.
"""

import base64
import os
from openai import OpenAI


def generate_background(image_prompt: str, output_path: str = "background.png") -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    full_prompt = (
        f"{image_prompt}. "
        "No text, no letters, no words, no typography anywhere in the image. "
        "Vertical portrait composition with room at the bottom for adding a title later. "
        "High quality, trendy magazine cover / movie still style, cinematic lighting."
    )

    result = client.images.generate(
        model="gpt-image-1",
        prompt=full_prompt,
        size="1024x1536",
        quality="high",
    )

    image_bytes = base64.b64decode(result.data[0].b64_json)
    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return output_path


if __name__ == "__main__":
    path = generate_background("a cinematic portrait of a mysterious figure in traditional Korean hanbok, moody lighting")
    print(f"저장됨: {path}")
