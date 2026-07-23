"""
[1단계 스크립트]
주제/캡션을 생성하고, 배경 이미지를 만들고, 포스터를 합성해서
posts/ 폴더에 저장한다.

이 스크립트가 끝나면 GitHub Actions가 결과물(poster 이미지, 기록 파일)을
저장소에 커밋 & 푸시한다. 그래야 Instagram이 그 이미지에 접근할 수 있는
'공개 URL'이 생기기 때문이다. (실제 인스타 게시는 main_publish.py 에서 함)
"""

import json
import os
from datetime import datetime, timezone, timedelta

from topic_writer import generate_post
from image_gen import generate_background
from poster import make_poster

KST = timezone(timedelta(hours=9))


def main() -> None:
    os.makedirs("posts", exist_ok=True)

    post_data = generate_post()
    print("생성된 주제:", post_data["topic"])
    print("제목:", post_data["title"])

    background_path = generate_background(post_data["image_prompt"])

    timestamp = datetime.now(KST).strftime("%Y%m%d_%H%M%S")
    filename = f"posts/{timestamp}.png"
    make_poster(background_path, post_data["title"], filename)
    print("포스터 저장 완료:", filename)

    pending = {
        "image_path": filename,
        "caption": post_data["caption"],
        "topic": post_data["topic"],
        "title": post_data["title"],
    }
    with open("pending_post.json", "w", encoding="utf-8") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)

    print("다음 단계(게시) 준비 완료")


if __name__ == "__main__":
    main()
