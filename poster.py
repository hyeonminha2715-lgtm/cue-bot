"""
배경 이미지 위에 CUE 로고 느낌의 워터마크 + 제목 텍스트를 입혀
최종 인스타 포스터(세로형 1080x1350, 4:5 비율)를 만드는 모듈.

한글이 깨지지 않도록 나눔고딕 폰트를 사용한다.
(GitHub Actions 워크플로우에서 `apt-get install fonts-nanum`으로 미리 설치해둠)
"""

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf"
FALLBACK_FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"

CANVAS_SIZE = (1080, 1350)  # 인스타그램 세로형(4:5) 비율
ACCENT_COLOR = (212, 255, 63)  # CUE 브랜드 라임그린


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in (FONT_PATH, FALLBACK_FONT_PATH):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_poster(background_path: str, title: str, output_path: str = "poster.png") -> str:
    bg = Image.open(background_path).convert("RGB").resize(CANVAS_SIZE)

    overlay = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    gradient_height = 620
    for i in range(gradient_height):
        alpha = int(210 * (i / gradient_height))
        y = CANVAS_SIZE[1] - gradient_height + i
        draw_overlay.line([(0, y), (CANVAS_SIZE[0], y)], fill=(0, 0, 0, alpha))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)

    draw = ImageDraw.Draw(bg)

    small_font = _load_font(36)
    draw.text((60, 1230), "CUE", font=small_font, fill=(255, 255, 255, 255))
    draw.rectangle([60, 1210, 130, 1216], fill=ACCENT_COLOR)

    max_width = CANVAS_SIZE[0] - 120
    font_size = 82
    font = _load_font(font_size)
    lines = _wrap_text(draw, title, font, max_width)
    while len(lines) > 3 and font_size > 40:
        font_size -= 4
        font = _load_font(font_size)
        lines = _wrap_text(draw, title, font, max_width)

    line_height = font_size + 16
    total_text_height = line_height * len(lines)
    y = CANVAS_SIZE[1] - 260 - total_text_height

    for line in lines:
        draw.text((60, y), line, font=font, fill=(255, 255, 255, 255))
        y += line_height

    bg.convert("RGB").save(output_path, quality=95)
    return output_path


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


if __name__ == "__main__":
    make_poster("background.png", "요즘 다들 쓰는 AI 메모앱", "poster.png")
