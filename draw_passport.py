#!/usr/bin/env python3
"""draw_passport.py — builds entry.png for the-passport-page-of-a-countr-2-20261121-0318.

Build-time only (runs on this VM with Pillow). The graded entrypoint main.py
just copies the entry.png this script writes. Run: python3 draw_passport.py
Deterministic: same data in, same bytes out (no timestamps, no randomness).

Concept (from the two helper research reports, authored into this script by
the implementation builder): the Republic of Kavara, a small South Pacific
atoll nation with no airport. Holder Mereana Sela Tavake, born Lumara.
All dates/MRZ/stamps verified internally consistent by hand (ICAO 9303
7-3-1 check digits recomputed in a verification script before drawing).
The telling detail: a red endorsement, "NOT VALID FOR TRAVEL BY AIR —
SEA PASSAGE ONLY (Islands Act 1987, s.4)", which also explains why every
trip in the stamp history lasts 14-15 days (sea voyages).
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (244, 239, 227)
PAPER_DARK = (236, 229, 211)
INK = (26, 26, 26)
NAVY = (31, 58, 95)
RED = (158, 43, 37)
GREY = (96, 96, 92)
RULE = (178, 172, 160)
TINT = (233, 228, 216)
PHOTO_BG = (201, 212, 214)
SKIN = (122, 74, 43)
SKIN_DARK = (104, 60, 34)
SKIN_LIGHT = (139, 88, 54)
HAIR = (24, 18, 14)
TEAL = (15, 95, 92)
TEAL_DARK = (11, 74, 72)
PANDANUS = (214, 186, 120)
FIJI = (31, 78, 121)
TONGA = (138, 51, 36)
NZ = (46, 93, 67)

F = "/usr/share/fonts/truetype/liberation/"
SERIF_B = F + "LiberationSerif-Bold.ttf"
SERIF = F + "LiberationSerif-Regular.ttf"
SANS = F + "LiberationSans-Regular.ttf"
SANS_B = F + "LiberationSans-Bold.ttf"
SANS_I = F + "LiberationSans-Italic.ttf"
MONO = F + "LiberationMono-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, size, text, max_w):
    """Largest font size <= `size` whose text fits max_w."""
    s = size
    while s > 8:
        f = font(path, s)
        if f.getlength(text) <= max_w:
            return f
        s -= 1
    return font(path, 8)


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def ls(draw, xy, s, size, fill, spacing=2):
    """Letterspaced caps text (anchor left-top)."""
    x, y = xy
    f = font(SANS, size)
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + spacing
    return x


# ---------------------------------------------------------------- data
SURNAME = "TAVAKE"
GIVEN = "MEREANA SELA"
NATIONALITY = "KAVARAN"
DOB = "14 MAR 1988"
SEX = "F"
POB = "LUMARA, KAVARA"
PASS_NO = "KV2847163"
ISSUE = "12 JUN 2023"
EXPIRY = "12 JUN 2033"
AUTHORITY = "Passport Office, Lumara"
HEIGHT = "168 cm"
EYES = "Brown"
ATOLL = "NUKU-MANU"
CLAN = "TAVAKE (Frigate Bird)"
MRZ1 = "P<KVTAVAKE<<MEREANA<SELA<<<<<<<<<<<<<<<<<<<<"
MRZ2 = "KV28471638KV<8803148F3306127<<<<<<<<<<<<<<08"

STAMPS = [
    ("FIJI", "ARRIVED", "04 AUG 2023", "SUVA", FIJI, -6),
    ("FIJI", "DEPARTED", "19 AUG 2023", "SUVA", FIJI, 5),
    ("TONGA", "ARRIVED", "10 FEB 2024", "NUKU'ALOFA", TONGA, -4),
    ("TONGA", "DEPARTED", "24 FEB 2024", "NUKU'ALOFA", TONGA, 7),
    ("NEW ZEALAND", "ARRIVED", "02 NOV 2024", "AUCKLAND", NZ, -7),
    ("NEW ZEALAND", "DEPARTED", "17 NOV 2024", "AUCKLAND", NZ, 3),
]


# ---------------------------------------------------------------- portrait
def draw_portrait(box_w=170, box_h=215):
    """Stylised flat-colour passport portrait of Mereana Sela Tavake
    (35 at issue, 36 at the last stamp).
    Warm deep-brown skin, black hair in a low bun, white frangipani behind
    the left ear, shell stud earring, deep-teal collared blouse with a
    woven pandanus-leaf trim. Plain pale blue-grey background."""
    img = Image.new("RGB", (box_w, box_h), PHOTO_BG)
    d = ImageDraw.Draw(img)
    cx = box_w // 2
    # soft background vignette
    d.ellipse([-30, -20, box_w + 30, box_h + 10], outline=(186, 199, 201), width=3)
    # low bun FIRST (behind the head, tucked at the left side) — drawn
    # after the head below would detach it; instead it is re-drawn
    # overlapping the head edge in draw order (see hair section).
    # shoulders / blouse
    d.polygon([(cx - 78, box_h), (cx - 62, 168), (cx - 34, 152),
               (cx + 34, 152), (cx + 62, 168), (cx + 78, box_h)], fill=TEAL)
    # blouse shading
    d.polygon([(cx - 78, box_h), (cx - 62, 168), (cx - 20, 158),
               (cx - 8, box_h)], fill=TEAL_DARK)
    # collar + pandanus trim (zigzag)
    d.polygon([(cx - 34, 152), (cx, 176), (cx + 34, 152),
               (cx + 18, 146), (cx, 158), (cx - 18, 146)], fill=PANDANUS)
    d.polygon([(cx - 30, 154), (cx, 172), (cx + 30, 154),
               (cx + 14, 149), (cx, 158), (cx - 14, 149)], fill=(238, 222, 170))
    # neck — short, skin tone, soft shadow only under the jaw
    d.rounded_rectangle([cx - 12, 126, cx + 12, 156], radius=8, fill=SKIN)
    d.ellipse([cx - 13, 122, cx + 13, 134], fill=SKIN_DARK)
    # head — slightly narrower, rounder
    d.ellipse([cx - 38, 42, cx + 38, 136], fill=SKIN)
    # cheek shading — subtle, close to skin tone (no blush patches)
    d.ellipse([cx - 36, 100, cx - 10, 126], fill=(130, 81, 48))
    d.ellipse([cx + 10, 100, cx + 36, 126], fill=(130, 81, 48))
    # ears
    d.ellipse([cx - 44, 88, cx - 34, 106], fill=SKIN)
    d.ellipse([cx + 34, 88, cx + 44, 106], fill=SKIN)
    # shell stud earring (left ear, viewer's right)
    d.ellipse([cx + 36, 98, cx + 44, 106], fill=(245, 240, 225),
              outline=(200, 190, 170), width=1)
    # hair: cap with a curved hairline (no straight bowl edge)
    d.pieslice([cx - 42, 30, cx + 42, 104], start=180, end=360, fill=HAIR)
    d.polygon([(cx - 42, 62), (cx - 38, 44), (cx - 20, 38), (cx - 30, 62)],
              fill=HAIR)
    d.polygon([(cx + 42, 62), (cx + 38, 44), (cx + 20, 38), (cx + 30, 62)],
              fill=HAIR)
    d.ellipse([cx - 42, 56, cx - 30, 78], fill=HAIR)
    d.ellipse([cx + 30, 56, cx + 42, 78], fill=HAIR)
    # break the straight forehead edge: skin rounds at the temples
    d.ellipse([cx - 40, 58, cx - 26, 74], fill=SKIN)
    d.ellipse([cx + 26, 58, cx + 40, 74], fill=SKIN)
    # low bun, drawn AFTER the head so it visibly attaches to its edge
    d.ellipse([cx - 60, 100, cx - 30, 130], fill=HAIR)
    d.arc([cx - 60, 100, cx - 30, 130], start=90, end=270, fill=(60, 48, 40), width=2)
    d.ellipse([cx - 44, 108, cx - 34, 122], fill=(40, 32, 26))
    # frangipani flower tucked at the temple above the left ear
    fx, fy = cx + 40, 76
    for ang in range(0, 360, 72):
        import math as _m
        px = fx + 9 * _m.cos(_m.radians(ang))
        py = fy + 9 * _m.sin(_m.radians(ang))
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(250, 248, 242),
                  outline=(220, 210, 190), width=1)
    d.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(250, 214, 90))
    # brows
    d.arc([cx - 28, 82, cx - 8, 96], start=200, end=340, fill=HAIR, width=3)
    d.arc([cx + 8, 82, cx + 28, 96], start=200, end=340, fill=HAIR, width=3)
    # eyes — smaller, softer (dark brown)
    for ex in (cx - 18, cx + 18):
        d.ellipse([ex - 6, 97, ex + 6, 103], fill=(250, 248, 242))
        d.ellipse([ex - 3, 97, ex + 3, 103], fill=(38, 22, 12))
        d.ellipse([ex - 1, 98, ex + 1, 100], fill=(250, 250, 250))
        d.line([ex - 7, 96, ex + 7, 96], fill=HAIR, width=1)
    # nose hint
    d.line([cx, 104, cx - 2, 118, cx + 3, 120], fill=SKIN_DARK, width=2)
    # closed-lip smile
    d.arc([cx - 12, 118, cx + 12, 134], start=15, end=165, fill=(90, 48, 30), width=3)
    return img


# ---------------------------------------------------------------- coat of arms
def draw_arms(size=44):
    """Frigate bird over waves inside a shield — the arms of Kavara."""
    img = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    # shield
    d.polygon([(s, 6), (s + 34, 14), (s + 34, 62), (s, 84), (s - 34, 62),
               (s - 34, 14)], outline=NAVY, width=3)
    d.polygon([(s, 10), (s + 30, 17), (s + 30, 60), (s, 78), (s - 30, 60),
               (s - 30, 17)], fill=(232, 240, 244))
    # sun
    d.ellipse([s - 8, 20, s + 8, 36], fill=(214, 164, 60))
    # frigate bird (two swept wings)
    d.arc([s - 26, 34, s - 2, 52], start=180, end=360, fill=NAVY, width=3)
    d.arc([s + 2, 34, s + 26, 52], start=180, end=360, fill=NAVY, width=3)
    d.ellipse([s - 2, 44, s + 2, 48], fill=NAVY)
    # waves
    for wy in (58, 64, 70):
        d.arc([s - 26, wy - 5, s - 6, wy + 5], start=180, end=360, fill=NAVY, width=2)
        d.arc([s + 6, wy - 5, s + 26, wy + 5], start=180, end=360, fill=NAVY, width=2)
    return img


# ---------------------------------------------------------------- signature
def draw_signature(d, x, y, w, ink=(30, 30, 90), seed=7):
    """Handwritten signature scribble on a ruled line (deterministic)."""
    import math
    import random
    rng = random.Random(seed)
    pts = []
    n = 26
    for i in range(n + 1):
        px = x + (w * i) / n
        py = y - 3 + 4 * math.sin(i * 1.7 + seed) * math.exp(-((i - 6) ** 2) / 40.0) \
            + 3 * math.sin(i * 3.1) * math.exp(-((i - 18) ** 2) / 25.0)
        pts.append((px, py))
    d.line(pts, fill=ink, width=2, joint="curve")
    # underline flourish (kept inside the width)
    d.arc([x + w * 0.60, y - 1, x + w * 0.92, y + 8], start=300, end=90,
          fill=ink, width=2)


# ---------------------------------------------------------------- stamps
def _stamp_texture(layer, w, h, colour, seed):
    """Deterministic ink-gap speckles along the stamp border only, so the
    stamp reads as rubber-stamped, never printed. Text stays untouched."""
    import random
    rng = random.Random(seed)
    d = ImageDraw.Draw(layer)
    for _ in range(46):
        edge = rng.randrange(4)
        if edge == 0:
            px, py = 20 + rng.randrange(w), 20 + rng.randrange(3)
        elif edge == 1:
            px, py = 20 + rng.randrange(w), 20 + h - rng.randrange(3)
        elif edge == 2:
            px, py = 20 + rng.randrange(3), 20 + rng.randrange(h)
        else:
            px, py = 20 + w - rng.randrange(3), 20 + rng.randrange(h)
        r = rng.choice([1, 1, 2])
        d.ellipse([px - r, py - r, px + r, py + r], fill=(244, 239, 227, 255))


# The two stamp columns are 220 px apart but a full-size stamp layer is
# ~272 px wide, so the right column overran the page border and was
# truncated at the canvas edge. Stamps are drawn at full size, then scaled
# to 0.88 before rotation: the visible right edge then lands near 987 px
# (inside the 1003 px page border) and the columns stop overlapping.
STAMP_SCALE = 0.88


def draw_stamp(country, action, date, port, colour, rot):
    """One border stamp on its own layer, rotated for a hand-stamped look."""
    w, h = 232, 158
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0 = 20, 20
    # double border
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=10,
                        outline=colour, width=3)
    d.rounded_rectangle([x0 + 5, y0 + 5, x0 + w - 5, y0 + h - 5], radius=8,
                        outline=colour, width=1)
    cx = x0 + w // 2
    f_c = font(SANS_B, 21)
    f_a = font(SANS_B, 24)
    f_d = font(SANS_B, 20)
    f_p = font(SANS, 15)
    # country (fit)
    cf = fit(SANS_B, 21, country, w - 24)
    d.text((cx, y0 + 16), country, font=cf, fill=colour, anchor="ma")
    # anchor glyph between country and action
    ax, ay = cx, y0 + 52
    d.line([ax, ay - 8, ax, ay + 8], fill=colour, width=3)
    d.arc([ax - 7, ay - 2, ax + 7, ay + 12], start=0, end=180, fill=colour, width=3)
    d.line([ax - 10, ay - 4, ax + 10, ay - 4], fill=colour, width=3)
    d.ellipse([ax - 3, ay - 11, ax + 3, ay - 5], fill=colour)
    # action + date + port
    d.text((cx, y0 + 66), action, font=f_a, fill=colour, anchor="ma")
    d.text((cx, y0 + 98), date, font=f_d, fill=colour, anchor="ma")
    d.text((cx, y0 + 126), port, font=f_p, fill=colour, anchor="ma")
    _stamp_texture(layer, w, h, colour, seed=sum(ord(c) for c in country + action))
    layer = layer.resize((round(layer.width * STAMP_SCALE),
                          round(layer.height * STAMP_SCALE)),
                         Image.BICUBIC)
    return layer.rotate(rot, expand=True, resample=Image.BICUBIC)


def draw_round_stamp(country, action, date, port, colour, rot, diameter=175):
    """Circular date-stamp variant (different form from the rectangles).
    Font sizes scale with the diameter so text stays inside the circle."""
    layer = Image.new("RGBA", (diameter + 40, diameter + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = cy = (diameter + 40) // 2
    r = diameter // 2
    sc = diameter / 210.0
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=3)
    d.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
              outline=colour, width=1)
    cf = fit(SANS_B, max(11, round(20 * sc)), country, diameter - 44)
    d.text((cx, cy - round(62 * sc)), country, font=cf, fill=colour, anchor="ma")
    # anchor glyph
    ax, ay = cx, cy - round(28 * sc)
    d.line([ax, ay - 8, ax, ay + 8], fill=colour, width=3)
    d.arc([ax - 7, ay - 2, ax + 7, ay + 12], start=0, end=180, fill=colour, width=3)
    d.line([ax - 10, ay - 4, ax + 10, ay - 4], fill=colour, width=3)
    d.ellipse([ax - 3, ay - 11, ax + 3, ay - 5], fill=colour)
    af = fit(SANS_B, max(12, round(23 * sc)), action, diameter - 30)
    d.text((cx, cy - round(2 * sc)), action, font=af, fill=colour, anchor="ma")
    d.text((cx, cy + round(28 * sc)), date,
           font=font(SANS_B, max(11, round(18 * sc))), fill=colour, anchor="ma")
    d.text((cx, cy + round(56 * sc)), port,
           font=font(SANS, max(11, round(14 * sc))), fill=colour, anchor="ma")
    layer = layer.resize((round(layer.width * STAMP_SCALE),
                          round(layer.height * STAMP_SCALE)),
                         Image.BICUBIC)
    return layer.rotate(rot, expand=True, resample=Image.BICUBIC)


# ---------------------------------------------------------------- atoll map
def draw_atolls(d, x, y, w, h):
    """Small stylised chart of Kavara's nine atolls on the data page."""
    # sea tint
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(228, 236, 238),
                        outline=RULE, width=1)
    import math
    pts = [(0.16, 0.30), (0.32, 0.62), (0.30, 0.22), (0.50, 0.42), (0.55, 0.64),
           (0.68, 0.28), (0.72, 0.58), (0.86, 0.38), (0.88, 0.70)]
    names = {0: ("NUKU-MANU", "below"), 3: ("LUMARA", "right"),
             4: ("MANU-ITI", "above"), 7: ("TAVAKE", "left")}
    for i, (fx, fy) in enumerate(pts):
        px, py = x + fx * w, y + fy * h
        r = 7 if i == 3 else 5
        d.ellipse([px - r, py - r, px + r, py + r], fill=(196, 200, 170),
                  outline=NAVY, width=2)
        if i in names:
            label, side = names[i]
            fnt = font(SANS_B, 12)
            if side == "below":
                d.text((px - 4, py + 9), label, font=fnt, fill=NAVY)
            elif side == "right":
                d.text((px + 11, py - 7), label, font=fnt, fill=NAVY)
            elif side == "above":
                d.text((px - 4, py - 22), label, font=fnt, fill=NAVY)
            else:
                d.text((px - fnt.getlength(label) - 10, py - 7), label,
                       font=fnt, fill=NAVY)
    # compass rose, top right
    ccx, ccy, cr = x + w - 34, y + 28, 15
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=NAVY, width=1)
    d.polygon([(ccx, ccy - cr - 3), (ccx - 4, ccy + 4), (ccx + 4, ccy + 4)],
              fill=NAVY)
    d.text((ccx, ccy - cr - 16), "N", font=font(SANS_B, 11), fill=NAVY,
           anchor="ma")
    d.text((x + 8, y + h - 20), "KAVARA — NINE ATOLLS · SOUTH PACIFIC",
           font=font(SANS, 11), fill=GREY)


# ---------------------------------------------------------------- composition
def field(d, x, y, w, label, value, value_size=17):
    """One labelled field with a ruled underline. Returns y of next field."""
    d.text((x, y), label, font=font(SANS, 11), fill=GREY)
    vf = fit(SANS_B, value_size, value, w)
    d.text((x, y + 14), value, font=vf, fill=INK)
    d.line([x, y + 34, x + w, y + 34], fill=RULE, width=1)
    return y + 42


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer double border + spine
    d.rectangle([14, 14, W - 15, H - 15], outline=NAVY, width=2)
    d.rectangle([20, 20, W - 21, H - 21], outline=NAVY, width=1)
    d.line([512, 20, 512, H - 21], fill=(200, 193, 176), width=2)
    d.line([514, 20, 514, H - 21], fill=(214, 208, 192), width=1)

    # ================= LEFT PAGE — data page =================
    LX0, LX1 = 28, 492
    # header: arms + country title
    arms = draw_arms(44)
    img.paste(arms, (256 - 44, 30), arms)
    d.text((260, 122), "REPUBLIC OF KAVARA", font=font(SERIF_B, 29),
           fill=NAVY, anchor="ma")
    ls(d, (260 - 62, 154), "PASSPORT", 13, NAVY, spacing=4)
    d.line([52, 176, 468, 176], fill=NAVY, width=2)

    # photo box
    px0, py0, pw, ph = 52, 192, 170, 215
    d.rectangle([px0 - 3, py0 - 3, px0 + pw + 3, py0 + ph + 3], fill=NAVY)
    portrait = draw_portrait(pw, ph)
    img.paste(portrait, (px0, py0))
    d.rectangle([px0, py0, px0 + pw, py0 + ph], outline=NAVY, width=2)
    # signature strip under photo (bearer signs on the line)
    d.line([px0, 428, px0 + pw, 428], fill=INK, width=1)
    draw_signature(d, px0 + 30, 422, pw - 60, seed=7)
    d.text((px0 + pw // 2, 434), "Signature of bearer", font=font(SANS_I, 11),
           fill=GREY, anchor="ma")

    # fields right of photo
    fx, fw = 244, 224
    y = 192
    y = field(d, fx, y, fw, "SURNAME", SURNAME)
    y = field(d, fx, y, fw, "GIVEN NAMES", GIVEN)
    y = field(d, fx, y, fw, "NATIONALITY", NATIONALITY)
    y = field(d, fx, y, fw, "DATE OF BIRTH", DOB)
    y = field(d, fx, y, fw, "SEX", SEX + "   ·   HEIGHT " + HEIGHT)
    y = field(d, fx, y, fw, "PLACE OF BIRTH", POB, value_size=15)
    # eyes line (ruled like the other fields)
    d.text((fx, y + 2), "EYES  " + EYES, font=font(SANS, 12), fill=INK)
    d.line([fx, y + 20, fx + fw, y + 20], fill=RULE, width=1)

    # bottom block: document number + dates + authority
    d.line([52, 480, 468, 480], fill=NAVY, width=1)
    d.text((52, 492), "PASSPORT No.", font=font(SANS, 11), fill=GREY)
    d.text((52, 506), PASS_NO, font=font(SANS_B, 26), fill=INK)
    d.text((300, 492), "DATE OF ISSUE", font=font(SANS, 11), fill=GREY)
    d.text((300, 508), ISSUE, font=font(SANS_B, 17), fill=INK)
    d.text((300, 536), "DATE OF EXPIRY", font=font(SANS, 11), fill=GREY)
    d.text((300, 552), EXPIRY, font=font(SANS_B, 17), fill=INK)
    d.text((52, 552), "AUTHORITY", font=font(SANS, 11), fill=GREY)
    d.text((52, 566), AUTHORITY, font=font(SANS_B, 15), fill=INK)
    d.text((52, 590), "HOME ATOLL  " + ATOLL + "   ·   CLAN  " + CLAN,
           font=font(SANS, 12), fill=INK)

    # red endorsement — the telling detail
    d.rounded_rectangle([52, 622, 468, 700], radius=4, outline=RED, width=3)
    d.text((260, 634), "NOT VALID FOR TRAVEL BY AIR",
           font=font(SANS_B, 16), fill=RED, anchor="ma")
    d.text((260, 658), "SEA PASSAGE ONLY  ·  Islands Act 1987, s.4",
           font=font(SANS_B, 13), fill=RED, anchor="ma")

    # atoll chart fills the lower middle (no dead space)
    draw_atolls(d, 52, 716, 416, 130)

    # MRZ band (two lines, vertically centred; no redundant caption)
    d.rectangle([52, 862, 468, 946], fill=TINT, outline=RULE, width=1)
    d.text((260, 880), MRZ1, font=font(MONO, 15), fill=INK, anchor="ma")
    d.text((260, 906), MRZ2, font=font(MONO, 15), fill=INK, anchor="ma")

    # ================= RIGHT PAGE — visas / stamps =================
    RX0 = 532
    d.text((764, 40), "VISAS", font=font(SERIF_B, 26), fill=NAVY, anchor="ma")
    d.text((980, 48), "PAGES 8–9", font=font(SANS, 12), fill=GREY, anchor="ra")
    d.line([548, 76, 980, 76], fill=NAVY, width=2)

    # 6 stamps, 2 columns x 3 rows, chronological top-to-bottom.
    # Fiji + Tonga are rectangular; New Zealand is circular (different
    # form, as real border stamps differ).
    positions = [(548, 92), (768, 92), (548, 268), (768, 268),
                 (548, 444), (768, 444)]
    for (country, action, date, port, colour, rot), (sx, sy) in zip(STAMPS, positions):
        if country == "NEW ZEALAND":
            stamp = draw_round_stamp(country, action, date, port, colour, rot)
            img.paste(stamp, (sx + 12, sy - 10), stamp)
        else:
            stamp = draw_stamp(country, action, date, port, colour, rot)
            img.paste(stamp, (sx - 8, sy - 8), stamp)

    # ferry tax stamp (second telling detail: the fee stamp)
    tax = Image.new("RGBA", (420, 90), (0, 0, 0, 0))
    td = ImageDraw.Draw(tax)
    td.rounded_rectangle([4, 4, 416, 86], radius=6, outline=NAVY, width=3)
    td.rounded_rectangle([9, 9, 411, 81], radius=4, outline=NAVY, width=1)
    td.text((210, 16), "FERRY TAX PAID — 12 VAKA", font=font(SANS_B, 19),
            fill=NAVY, anchor="ma")
    td.text((210, 48), "LUMARA FERRY TERMINAL",
            font=font(SANS, 13), fill=NAVY, anchor="ma")
    tax = tax.rotate(-3, expand=True, resample=Image.BICUBIC)
    img.paste(tax, (556, 652), tax)

    # remarks block
    d.line([548, 762, 980, 762], fill=NAVY, width=1)
    d.text((548, 774), "REMARKS", font=font(SANS_B, 13), fill=NAVY)
    remarks = [
        "Holder is a citizen of the Republic of Kavara.",
        "This passport remains the property of the Government",
        "of Kavara and must be surrendered on demand.",
        "Sea passage only: the Republic has no airport.",
    ]
    ry = 796
    for line in remarks:
        d.text((548, ry), line, font=font(SANS, 13), fill=INK)
        ry += 20
    # issuing officer signature
    d.line([548, 890, 740, 890], fill=INK, width=1)
    draw_signature(d, 556, 886, 120, seed=21)
    d.text((548, 896), "Issuing officer, Lumara", font=font(SANS_I, 11), fill=GREY)
    d.text((800, 890), "12 JUN 2023", font=font(SANS_B, 14), fill=INK, anchor="ra")
    # footer
    d.text((764, 958), "KV — 2847163", font=font(SANS, 11), fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes)")
