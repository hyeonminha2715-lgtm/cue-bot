"""
클로드(Anthropic) API + 웹 검색 도구를 이용해
- 오늘 다룰 '실제' 트렌드/이슈 주제 (지어내지 않고 검색 기반)
- 포스터에 들어갈 짧은 제목
- 인스타 캡션(사실 기반 설명글, 여러 문단)
- 배경 이미지 생성을 위한 영어 프롬프트
를 한 번에 만들어주는 모듈.

최근에 다룬 주제 목록(topics_history.json)을 참고해서
같은 주제가 반복되지 않도록 함.
"""

import json
import os
from anthropic import Anthropic

HISTORY_FILE = "topics_history.json"
MAX_HISTORY = 30


def load_history() -> list[str]:
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history: list[str]) -> None:
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-MAX_HISTORY:], f, ensure_ascii=False, indent=2)


def _extract_json(text: str) -> dict:
    """응답 텍스트(검색 인용 등이 섞여있을 수 있음)에서 JSON 객체만 뽑아낸다."""
    text = text.replace("```json", "").replace("```", "")
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"JSON을 찾을 수 없음: {text[:300]}")
    return json.loads(text[start : end + 1])


def generate_post() -> dict:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    history = load_history()

    history_note = (
        f"최근에 이미 다룬 주제들이야. 이거랑 겹치지 않는 새로운 주제를 골라줘: {history}"
        if history
        else "아직 다룬 주제가 없어. 자유롭게 첫 주제를 골라줘."
    )

    prompt = f"""너는 'CUE'라는 인스타그램 매거진 계정의 에디터야.
컨셉: 라이프스타일 × 테크를 다루는 트렌디한 매거진.

**먼저 웹 검색을 해서 오늘 기준 실제로 화제가 되고 있는 라이프스타일 또는 테크 이슈를 하나 찾아줘.**
지어내지 말고, 검색으로 확인된 실제 뉴스/트렌드만 사용해. (예: 특정 드라마 화제성, 새로 나온 서비스/기기, 급부상한 트렌드 등 - 실제로 지금 사람들이 얘기하고 있는 것)

{history_note}

주제를 정했으면, 아래 형식의 JSON으로만 답해줘 (JSON 앞뒤에 다른 설명 붙이지 마):
{{
  "topic": "이번에 다룰 주제 (한 줄, 한국어)",
  "title": "포스터 정중앙에 들어갈 임팩트 있는 제목 (한국어, 2줄 이내로 짧게, 예: '공개 5일 만에 000를 집어삼켰다' 같은 후킹한 문구)",
  "caption": "인스타 캡션. 검색으로 확인한 실제 사실/수치/배경 설명을 3~4개의 짧은 문단으로 구성. 각 문단은 줄바꿈(\\n\\n)으로 구분. 트렌디하지만 정보성 있는 말투. 마지막에 해시태그 4~6개",
  "image_prompt": "포스터 배경으로 쓸 이미지에 대한 영어 프롬프트 (글자 없이, 주제와 관련된 인물/사물/분위기를 담은 세로형 구도, 영화 스틸컷 또는 매거진 화보 같은 느낌으로 구체적으로 묘사)"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )

    full_text = "".join(
        block.text for block in response.content if block.type == "text"
    )
    data = _extract_json(full_text)

    history.append(data["topic"])
    save_history(history)

    return data


if __name__ == "__main__":
    result = generate_post()
    print(json.dumps(result, ensure_ascii=False, indent=2))
