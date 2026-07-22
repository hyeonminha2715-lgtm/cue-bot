name: CUE 자동 포스팅

on:
  schedule:
    # 한국시간(KST) 기준 오전 9시 / 오후 3시 / 오후 9시 = UTC 0시 / 6시 / 12시
    - cron: "0 0,6,12 * * *"
  workflow_dispatch: {}   # 수동으로 "Run workflow" 버튼 눌러 테스트 가능

permissions:
  contents: write

jobs:
  auto-post:
    runs-on: ubuntu-latest
    steps:
      - name: 저장소 체크아웃
        uses: actions/checkout@v4

      - name: 파이썬 설치
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: 한글 폰트 설치
        run: sudo apt-get update && sudo apt-get install -y fonts-nanum

      - name: 패키지 설치
        run: pip install -r requirements.txt

      - name: 1단계 - 주제/이미지/포스터 생성
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python main_generate.py

      - name: 결과물 커밋 & 푸시 (Instagram이 볼 수 있는 공개 URL을 만들기 위함)
        run: |
          git config user.name "cue-bot"
          git config user.email "cue-bot@users.noreply.github.com"
          git add posts/ topics_history.json pending_post.json
          git commit -m "auto: 새 포스트 생성 $(date -u +'%Y-%m-%d %H:%M UTC')"
          git push

      - name: 이미지가 GitHub에 반영될 때까지 잠깐 대기
        run: sleep 20

      - name: 2단계 - 인스타그램 게시
        env:
          IG_USER_ID: ${{ secrets.IG_USER_ID }}
          IG_ACCESS_TOKEN: ${{ secrets.IG_ACCESS_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          GITHUB_BRANCH: main
        run: python main_publish.py
