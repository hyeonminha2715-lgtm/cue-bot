"""
Instagram API(graph.instagram.com)로 이미지+캡션을 게시하는 모듈.

전제 조건: poster 이미지가 인터넷에서 접근 가능한 '공개 URL'이어야 함
(Instagram 서버가 그 URL로 직접 이미지를 가져가기 때문).
이 프로젝트에서는 GitHub 저장소(퍼블릭)에 이미지를 커밋한 뒤,
raw.githubusercontent.com 주소를 그 공개 URL로 사용한다.
"""

import os
import time
import requests

GRAPH_API_BASE = "https://graph.instagram.com/v21.0"


def publish_post(image_url: str, caption: str) -> str:
    ig_user_id = os.environ["IG_USER_ID"]
    access_token = os.environ["IG_ACCESS_TOKEN"]

    # 1) 미디어 컨테이너 생성
    create_res = requests.post(
        f"{GRAPH_API_BASE}/{ig_user_id}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token,
        },
        timeout=30,
    )
    create_res.raise_for_status()
    creation_id = create_res.json()["id"]

    # 2) 컨테이너가 처리될 때까지 잠깐 대기 (드물게 바로 처리 안 될 수 있음)
    time.sleep(5)

    # 3) 게시
    publish_res = requests.post(
        f"{GRAPH_API_BASE}/{ig_user_id}/media_publish",
        data={
            "creation_id": creation_id,
            "access_token": access_token,
        },
        timeout=30,
    )
    publish_res.raise_for_status()

    return publish_res.json()["id"]


if __name__ == "__main__":
    post_id = publish_post(
        "https://example.com/sample.png",
        "테스트 캡션입니다 #CUE",
    )
    print(f"게시 완료, post id: {post_id}")
