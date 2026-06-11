"""
Gera arquivos SVG e PNG para as 5 variantes da logomarca Dignitatis.
Figura humana estilizada (braços erguidos) + wordmark DIGNITATIS.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path(__file__).parent

# Brand colors
TERRACOTA  = (181, 78, 49, 255)    # #B54E31
AZUL_NOITE = (15, 31, 61, 255)     # #0F1F3D
AREIA      = (249, 245, 239, 255)  # #F9F5EF
BRANCO     = (255, 255, 255, 255)
TRANSP     = (0, 0, 0, 0)

FONT_PATH  = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def figure_polygons(cx, cy, scale=1.0):
    """
    Returns (head_circle, body_polygon, left_arm_polygon, right_arm_polygon)
    for a geometric human figure with arms raised.
    cx, cy = center-x, bottom-center-y of bounding box
    scale  = pixels per unit (unit ~= figure height 100)
    """
    s = scale

    # Head: circle at top center
    head_cx = cx
    head_cy = cy - 88 * s
    head_r  = 14 * s

    # Shoulders at y = cy - 68*s
    # Body: from shoulders down
    body = [
        (cx - 17*s, cy - 68*s),  # upper-left shoulder
        (cx + 17*s, cy - 68*s),  # upper-right shoulder
        (cx + 14*s, cy),          # lower-right
        (cx - 14*s, cy),          # lower-left
    ]

    # Left arm: extends upward-left from left shoulder
    # Arm goes from shoulder corner, sweeps up to arm tip, returns
    larm = [
        (cx - 17*s, cy - 68*s),  # shoulder connect (same as body UL)
        (cx - 14*s, cy - 80*s),  # inner arm base
        (cx - 38*s, cy - 90*s),  # arm tip inner
        (cx - 44*s, cy - 76*s),  # arm tip outer
        (cx - 26*s, cy - 62*s),  # outer shoulder
    ]

    # Right arm: mirror of left
    rarm = [
        (cx + 17*s, cy - 68*s),
        (cx + 14*s, cy - 80*s),
        (cx + 38*s, cy - 90*s),
        (cx + 44*s, cy - 76*s),
        (cx + 26*s, cy - 62*s),
    ]

    return head_cx, head_cy, head_r, body, larm, rarm


def draw_figure(draw, cx, cy, scale, color):
    hcx, hcy, hr, body, larm, rarm = figure_polygons(cx, cy, scale)
    draw.ellipse([hcx - hr, hcy - hr, hcx + hr, hcy + hr], fill=color)
    draw.polygon(body, fill=color)
    draw.polygon(larm, fill=color)
    draw.polygon(rarm, fill=color)


def make_completo(bg=(0,0,0,0), fig_color=TERRACOTA, text_color=AZUL_NOITE):
    W, H = 1200, 420
    img = Image.new("RGBA", (W, H), bg)
    draw = ImageDraw.Draw(img)

    # Figure on the left
    draw_figure(draw, cx=170, cy=370, scale=3.5, color=fig_color)

    # Wordmark to the right
    try:
        font = ImageFont.truetype(FONT_PATH, 110)
    except Exception:
        font = ImageFont.load_default()

    draw.text((340, 120), "DIGNITATIS", font=font, fill=text_color)
    return img


def make_compacto(bg=(0,0,0,0), fig_color=TERRACOTA, text_color=AZUL_NOITE):
    W, H = 700, 700
    img = Image.new("RGBA", (W, H), bg)
    draw = ImageDraw.Draw(img)

    # Figure centered on top half
    draw_figure(draw, cx=350, cy=420, scale=3.8, color=fig_color)

    # Wordmark below, centered
    try:
        font = ImageFont.truetype(FONT_PATH, 72)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "DIGNITATIS", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 455), "DIGNITATIS", font=font, fill=text_color)
    return img


def make_icone(bg=(0,0,0,0), fig_color=TERRACOTA):
    W, H = 500, 500
    img = Image.new("RGBA", (W, H), bg)
    draw = ImageDraw.Draw(img)
    draw_figure(draw, cx=250, cy=440, scale=4.0, color=fig_color)
    return img


def save_variants():
    # 1. Completo — terracota figure, navy wordmark, transparent bg
    make_completo().save(OUT / "dignitatis-logo-completo.png")
    print("  ✓ dignitatis-logo-completo.png")

    # 2. Compacto — stacked, transparent bg
    make_compacto().save(OUT / "dignitatis-logo-compacto.png")
    print("  ✓ dignitatis-logo-compacto.png")

    # 3. Ícone — symbol only, transparent bg
    make_icone().save(OUT / "dignitatis-logo-icone.png")
    print("  ✓ dignitatis-logo-icone.png")

    # 4. Escuro — monochrome navy figure + navy wordmark
    make_completo(fig_color=AZUL_NOITE, text_color=AZUL_NOITE).save(
        OUT / "dignitatis-logo-escuro.png"
    )
    print("  ✓ dignitatis-logo-escuro.png")

    # 5. Branco — white figure + white wordmark (for dark backgrounds)
    make_completo(fig_color=BRANCO, text_color=BRANCO).save(
        OUT / "dignitatis-logo-branco.png"
    )
    print("  ✓ dignitatis-logo-branco.png")


if __name__ == "__main__":
    print("Gerando variantes da logomarca Dignitatis...")
    save_variants()
    print(f"Concluído: {OUT}")
