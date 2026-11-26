#!/usr/bin/env python3
"""Draw the competition entry image: a newspaper front page for 26 November 2026."""

from PIL import Image, ImageDraw, ImageFont
import os

# Canvas
W, H = 1024, 1024
IMG = Image.new("RGB", (W, H), (250, 248, 240))  # off-white newsprint
DRAW = ImageDraw.Draw(IMG)

# Fonts
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
try:
    FONT_BOLD = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 42)
    FONT_BOLD_SM = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 26)
    FONT_BOLD_XS = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 20)
    FONT_REG = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), 22)
    FONT_REG_SM = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), 18)
    FONT_MAST = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf"), 56)
    FONT_DATE = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 72)
    FONT_DAY = ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), 36)
except OSError:
    # Fallback to default
    FONT_BOLD = ImageFont.load_default()
    FONT_BOLD_SM = ImageFont.load_default()
    FONT_BOLD_XS = ImageFont.load_default()
    FONT_REG = ImageFont.load_default()
    FONT_REG_SM = ImageFont.load_default()
    FONT_MAST = ImageFont.load_default()
    FONT_DATE = ImageFont.load_default()
    FONT_DAY = ImageFont.load_default()

BLACK = (15, 15, 15)
DARK_GRAY = (60, 60, 60)
MID_GRAY = (120, 120, 120)
LIGHT_GRAY = (200, 198, 190)
RULE = (80, 80, 80)

def draw_text(x, y, text, font, fill=BLACK, anchor="lt"):
    DRAW.text((x, y), text, font=font, fill=fill, anchor=anchor)

def draw_wrapped(x, y, text, font, max_w, fill=BLACK, line_spacing=4):
    """Draw text wrapped to max_w, return height used."""
    words = text.split()
    lines = []
    cur = []
    for w in words:
        test = " ".join(cur + [w])
        if DRAW.textlength(test, font=font) <= max_w:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    h = 0
    for line in lines:
        draw_text(x, y + h, line, font, fill=fill)
        h += font.size + line_spacing
    return h

# ============ MASTHEAD ============
mast_y = 30
draw_text(W // 2, mast_y, "THE WORLD TODAY", FONT_MAST, fill=BLACK, anchor="mt")

# Double rule under masthead
DRAW.line([(60, mast_y + 62), (W - 60, mast_y + 62)], fill=RULE, width=3)
DRAW.line([(60, mast_y + 68), (W - 60, mast_y + 68)], fill=RULE, width=1)

# ============ DATE ============
date_y = mast_y + 90
draw_text(W // 2, date_y, "26 NOVEMBER 2026", FONT_DATE, fill=BLACK, anchor="mt")
day_y = date_y + 80
draw_text(W // 2, day_y, "THURSDAY", FONT_DAY, fill=DARK_GRAY, anchor="mt")

# Rule under date
DRAW.line([(80, day_y + 46), (W - 80, day_y + 46)], fill=RULE, width=2)

# ============ NEWS STORIES ============
# Pick 6 stories for breadth:
stories = [
    ("US proposes 25% tariffs on Indian goods",
     "17% rate if trade deal reached; New Delhi warns of retaliation"),
    ("Houthis strike Riyadh; India condemns attack",
     "Two Indian nationals injured in missile barrage on Saudi capital"),
    ("First Pakistani astronaut reaches Tiangong",
     "Shenzhou-24 carries Islamabad's inaugural spaceman to Chinese station"),
    ("NATO ramps up air surveillance after missile crashes",
     "South Korea on alert as Russian jets near its airspace"),
    ("Tankers hit by explosions in Strait of Hormuz",
     "Multiple vessels damaged; global oil supply route disrupted"),
    ("Six dead in plane crash off US southern coast",
     "Small aircraft ditches in Gulf; no survivors found"),
]

# Layout: 2 columns x 3 rows
col_w = (W - 160) // 2
col_gap = 40
start_x_left = 80
start_x_right = 80 + col_w + col_gap
start_y = day_y + 70
row_h = 260

for idx, (headline, detail) in enumerate(stories):
    row = idx // 2
    col = idx % 2
    x = start_x_left if col == 0 else start_x_right
    y = start_y + row * row_h

    # Story box background (subtle)
    DRAW.rectangle([x - 10, y - 8, x + col_w + 10, y + row_h - 30],
                   outline=LIGHT_GRAY, width=1)

    # Headline
    draw_wrapped(x, y, headline, FONT_BOLD_SM, col_w - 10, fill=BLACK, line_spacing=2)

    # Detail line
    detail_y = y + 95
    draw_wrapped(x, detail_y, detail, FONT_REG_SM, col_w - 10, fill=DARK_GRAY, line_spacing=2)

    # Thin rule between stories in same column (except last row)
    if row < 2:
        rule_y = y + row_h - 20
        DRAW.line([(x, rule_y), (x + col_w, rule_y)], fill=MID_GRAY, width=1)

# ============ DECORATIVE GLOBE (bottom-left story box clear space) ============
# Moved from bottom-right to the empty space at the bottom of the first story
# (left column, first row). Detail text ends ~y=409; rule between stories at y=510.
# Globe sits safely in the clear gap.
globe_cx, globe_cy = 180, 460
globe_r = 40
DRAW.ellipse([globe_cx - globe_r, globe_cy - globe_r,
              globe_cx + globe_r, globe_cy + globe_r],
             outline=RULE, width=2)
# Meridians
for angle in (0, 90):
    import math
    rad = math.radians(angle)
    x1 = globe_cx + globe_r * math.cos(rad)
    y1 = globe_cy + globe_r * math.sin(rad)
    x2 = globe_cx - globe_r * math.cos(rad)
    y2 = globe_cy - globe_r * math.sin(rad)
    DRAW.line([(x1, y1), (x2, y2)], fill=RULE, width=1)
# Equator
DRAW.line([(globe_cx - globe_r, globe_cy), (globe_cx + globe_r, globe_cy)], fill=RULE, width=1)

# ============ BOTTOM RULE ============
DRAW.line([(60, H - 40), (W - 60, H - 40)], fill=RULE, width=2)
draw_text(W // 2, H - 30, "THE WORLD TODAY  •  26 NOVEMBER 2026",
          FONT_REG_SM, fill=MID_GRAY, anchor="mt")

# Save
out_path = "entry.png"
IMG.save(out_path, "PNG", optimize=True)
print(f"Saved {out_path}")

# Verify
import os
size = os.path.getsize(out_path)
print(f"File size: {size} bytes ({size/1024:.1f} KiB)")
print(f"Dimensions: {IMG.size}")
assert IMG.size == (1024, 1024), "Wrong dimensions"
assert size < 1048576, "File too large (>1 MiB)"
print("✓ All checks passed")