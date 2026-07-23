"""
클로드(Anthropic) API를 이용해
- 오늘 다룰 주제
- 포스터에 들어갈 짧은 제목
- 인스타 캡션(설명글)
- 배경 이미지 생성을 위한 영어 프롬프트
를 한 번에 만들어주는 모듈.

최근에 다룬 주제 목록(topics_history.json)을 참고해서
같은 주제가 반복되지 않도록 함.
"""

import json
import os
from anthropic import Anthropic

HISTORY_FILE = "topics_history.json"
MAX_HISTORY = 30  # 최근 몇 개까지 "겹치지 않게" 참고할지


def load_history() -> list[str]:
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history: list[str]) -> None:
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-MAX_HISTORY:], f, ensure_ascii=False, indent=2)


def generate_post() -> dict:
    """
    반환값 예시:
    {
        "topic": "AI 노트 앱 트렌드",
        "title": "요즘 다들 쓰는 AI 메모앱",
        "caption": "인스타 캡션 텍스트...",
        "image_prompt": "a minimalist flat illustration of ..."
    }
    """
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    history = load_history()

    history_note = (
        f"최근에 이미 다룬 주제들이야. 이거랑 겹치지 않는 새로운 주제를 골라줘: {history}"
        if history
        else "아직 다룬 주제가 없어. 자유롭게 첫 주제를 골라줘."
    )

    prompt = f"""너는 'CUE'라는 인스타그램 매거진 계정의 에디터야.
컨셉: 라이프스타일 × 테크를 다루는 트렌디한 매거진, 하루 여러 번 짧고 임팩트 있는 카드뉴스 형태로 업로드해.

{history_note}

아래 형식의 JSON으로만 답해줘 (다른 설명 붙이지 말고 JSON만):
{{
  "topic": "이번에 다룰 주제 (한 줄, 한국어)",
  "title": "포스터 정중앙에 들어갈 아주 짧은 제목 (한국어, 8자 내외, 임팩트 있게)",
  "caption": "인스타 캡션 (한국어, 2~4문장, 트렌디한 말투, 해시태그 3~5개 포함)",
  "image_prompt": "포스터 배경으로 쓸 이미지에 대한 영어 프롬프트 (글자/텍스트 없는 미니멀한 일러스트 또는 사진 스타일 배경, 구체적으로 묘사)"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    data = json.loads(text)

    history.append(data["topic"])
    save_history(history)

    return data


if __name__ == "__main__":
    result = generate_post()
    print(json.dumps(result, ensure_ascii=False, indent=2))
