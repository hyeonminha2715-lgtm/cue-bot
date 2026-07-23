"""
[2단계 스크립트]
main_generate.py가 만든 poster 이미지가 GitHub에 커밋&푸시된 '이후'에 실행된다.
raw.githubusercontent.com 공개 URL을 만들어서 Instagram API로 게시한다.
"""

import json
import os

from instagram_client import publish_post


def build_public_image_url(image_path: str) -> str:
    repo = os.environ["GITHUB_REPOSITORY"]  # 예: "username/cue-bot"
    branch = os.environ.get("GITHUB_BRANCH", "main")
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{image_path}"


def main() -> None:
    with open("pending_post.json", "r", encoding="utf-8") as f:
        pending = json.load(f)

    image_url = build_public_image_url(pending["image_path"])
    print("공개 이미지 URL:", image_url)

    post_id = publish_post(image_url, pending["caption"])
    print("인스타그램 게시 완료! post id:", post_id)


if __name__ == "__main__":
    main()
