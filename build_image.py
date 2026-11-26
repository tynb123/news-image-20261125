"""Draw the 25 November 2026 world-news image (1024x768 PNG).

Deterministic: fixed layout, fixed fonts, no randomness, no timestamps.
Run: python3 build_image.py  -> writes entry.png next to this file.

Layout: a navy header with the date in huge type, then five rows.
Each row is one story: a coloured block holding one big number on the
left, and a short bold headline (one or two lines, no small print) on
the right. Nothing else on the image: no subtitles, no source lines,
no lists. The first design goal is legibility at ~300 px wide, so the
date and the five numbers are as large as the layout allows.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 768
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (15, 23, 42)
GOLD = (245, 158, 11)
INK = (17, 24, 39)
WHITE = (255, 255, 255)
DIVIDER = (229, 231, 235)

HEADER_H = 108
ROW_H = 132
NUM_W = 270
TEXT_X = NUM_W + 24
TEXT_W = W - TEXT_X - 28

# (big number, headline, block colour)
# Numbers are taken verbatim from the verified research file:
# 14 economies hit by new US tariffs; Dow closed +164.25 after erasing
# a 1,100-point intraday plunge; 2 tankers hit mines in the Strait of
# Hormuz; Shenzhou-24 launched 08:18 Beijing time; A$740M over 10 years.
ROWS = [
    ("14", "US hits 14 economies with new tariffs", (185, 28, 28)),
    ("+164", "Dow erases 1,100-point plunge to close higher", (22, 101, 52)),
    ("2", "Oil tankers hit mines in the Strait of Hormuz", (194, 65, 12)),
    ("08:18", "First foreign astronaut boards China's Tiangong station", (29, 78, 216)),
    ("A$740M", "Solomon Islands signs Australia pact — no foreign bases", (15, 118, 110)),
]


def font(size):
    return ImageFont.truetype(BOLD, size)


def fit_font(draw, text, start, max_w, min_size=20):
    """Largest bold font size (<= start) at which text fits in max_w."""
    size = start
    while size > min_size and draw.textlength(text, font=font(size)) > max_w:
        size -= 1
    return font(size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_image():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # Header: the date, huge, centred on navy.
    draw.rectangle([0, 0, W, HEADER_H], fill=NAVY)
    date_font = fit_font(draw, "25 NOVEMBER 2026", 68, W - 40)
    draw.text((W / 2, HEADER_H / 2), "25 NOVEMBER 2026",
              font=date_font, fill=WHITE, anchor="mm")
    draw.rectangle([0, HEADER_H - 5, W, HEADER_H], fill=GOLD)

    # Five story rows.
    y = HEADER_H
    for number, headline, colour in ROWS:
        # Coloured number block.
        draw.rectangle([0, y, NUM_W, y + ROW_H], fill=colour)
        num_font = fit_font(draw, number, 64, NUM_W - 24)
        draw.text((NUM_W / 2, y + ROW_H / 2), number,
                  font=num_font, fill=WHITE, anchor="mm")
        # Headline, shrunk only until it fits on two lines.
        size = 38
        while size >= 26:
            fnt = font(size)
            lines = wrap(draw, headline, fnt, TEXT_W)
            if len(lines) <= 2:
                break
            size -= 1
        line_h = int(size * 1.18)
        total_h = line_h * len(lines)
        ty = y + (ROW_H - total_h) / 2
        for line in lines:
            draw.text((TEXT_X, ty), line, font=fnt, fill=INK)
            ty += line_h
        # Thin divider between rows.
        draw.line([(0, y + ROW_H - 1), (W, y + ROW_H - 1)], fill=DIVIDER, width=1)
        y += ROW_H

    return img


def main():
    img = draw_image()
    img.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
