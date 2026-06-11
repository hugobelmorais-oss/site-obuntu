"""
Gera arquivos PNG para as 5 variantes da logomarca Dignitatis.
Símbolo: arco duplo horizonte (terracota + navy) — evoca alba do semiárido,
         luta por direitos humanos no contexto das mudanças climáticas.
Wordmark: DIGNITATIS (Liberation Serif Bold / Fraunces)
Tagline:  direitos humanos . PB
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).parent

TERRACOTA  = (181, 78, 49, 255)    # #B54E31
AZUL_NOITE = (15, 31, 61, 255)     # #0F1F3D
AREIA      = (249, 245, 239, 255)  # #F9F5EF
BRANCO     = (255, 255, 255, 255)
TRANSP     = (0, 0, 0, 0)

FONT_BOLD  = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_SEMI  = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_SANS  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def draw_arc_symbol(draw, cx, cy, scale, arc_color, dome_color, bg_color):
    """
    Arco duplo horizonte: arco grosso (arc_color) com cúpula interna (dome_color).
    cy = baseline y (ponto inferior do símbolo).
    scale = pixels por unidade (unidade de referência: raio externo = 100).
    """
    s = scale
    outer_r = int(100 * s)
    # Arco terracota externo: meia-elipse superior
    draw.pieslice(
        [cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r],
        start=180, end=0, fill=arc_color
    )
    # Corte interno (cria espessura do arco ~30% do raio)
    cut_r = int(68 * s)
    draw.pieslice(
        [cx - cut_r, cy - cut_r, cx + cut_r, cy + cut_r],
        start=180, end=0, fill=bg_color
    )
    # Cúpula navy interna
    dome_rx = int(58 * s)
    dome_ry = int(38 * s)
    draw.pieslice(
        [cx - dome_rx, cy - dome_ry, cx + dome_rx, cy + dome_ry],
        start=180, end=0, fill=dome_color
    )
    # Linha de base horizontal (navy/arc_color)
    lw = max(3, int(5 * s))
    draw.rectangle(
        [cx - outer_r, cy - lw, cx + outer_r, cy + lw],
        fill=dome_color
    )


def make_completo(bg=TRANSP, arc_color=TERRACOTA, dome_color=AZUL_NOITE,
                  text_color=AZUL_NOITE, tag_color=(158, 142, 124, 255)):
    W, H = 1400, 420
    img = Image.new("RGBA", (W, H), bg)
    draw = ImageDraw.Draw(img)

    # Símbolo à esquerda
    sym_scale = 1.7
    sym_cx = 185
    sym_cy = 290
    draw_arc_symbol(draw, sym_cx, sym_cy, sym_scale, arc_color, dome_color,
                    bg if bg != TRANSP else (0, 0, 0, 0))

    # Wordmark DIGNITATIS
    try:
        font_main = ImageFont.truetype(FONT_BOLD, 105)
        font_tag  = ImageFont.truetype(FONT_SANS, 38)
    except Exception:
        font_main = ImageFont.load_default()
        font_tag  = font_main

    draw.text((355, 115), "DIGNITATIS", font=font_main, fill=text_color)

    # Tagline
    bbox = draw.textbbox((0, 0), "DIGNITATIS", font=font_main)
    wm_w = bbox[2] - bbox[0]
    tag_text = "direitos humanos . PB"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_x = 355 + (wm_w - tag_w) // 2
    draw.text((tag_x, 240), tag_text, font=font_tag, fill=tag_color)
    return img


def make_compacto(bg=TRANSP, arc_color=TERRACOTA, dome_color=AZUL_NOITE,
                  text_color=AZUL_NOITE, tag_color=(158, 142, 124, 255)):
    W, H = 700, 680
    img = Image.new("RGBA", (W, H), bg)
    draw = ImageDraw.Draw(img)

    # Símbolo centralizado no topo
    sym_scale = 2.2
    sym_cx = W // 2
    sym_cy = 260
    draw_arc_symbol(draw, sym_cx, sym_cy, sym_scale, arc_color, dome_color,
                    bg if bg != TRANSP else (0, 0, 0, 0))

    try:
        font_main = ImageFont.truetype(FONT_BOLD, 82)
        font_tag  = ImageFont.truetype(FONT_SANS, 30)
    except Exception:
        font_main = ImageFont.load_default()
        font_tag  = font_main

    # DIGNITATIS centralizado
    bbox = draw.textbbox((0, 0), "DIGNITATIS", font=font_main)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 310), "DIGNITATIS", font=font_main, fill=text_color)

    # Tagline centralizada
    tag_text = "direitos humanos . PB"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=font_tag)
    tag_w = tag_bbox[2] - tag_bbox[0]
    draw.text(((W - tag_w) // 2, 415), tag_text, font=font_tag, fill=tag_color)
    return img


def make_icone(bg=TRANSP, arc_color=TERRACOTA, dome_color=AZUL_NOITE):
    W, H = 500, 320
    img = Image.new("RGBA", (W, H), bg)
    draw = ImageDraw.Draw(img)
    draw_arc_symbol(draw, W // 2, H - 40, 2.2, arc_color, dome_color,
                    bg if bg != TRANSP else (0, 0, 0, 0))
    return img


def save_variants():
    # 1. Completo — terracota arc, navy dome, navy wordmark, transparent bg
    make_completo().save(OUT / "dignitatis-logo-completo.png")
    print("  ✓ dignitatis-logo-completo.png")

    # 2. Compacto — empilhado, transparent bg
    make_compacto().save(OUT / "dignitatis-logo-compacto.png")
    print("  ✓ dignitatis-logo-compacto.png")

    # 3. Ícone — só símbolo
    make_icone().save(OUT / "dignitatis-logo-icone.png")
    print("  ✓ dignitatis-logo-icone.png")

    # 4. Escuro — tudo navy (monocromático)
    CINZA_NOITE = (158, 142, 124, 255)
    make_completo(arc_color=AZUL_NOITE, dome_color=(8, 16, 30, 255),
                  text_color=AZUL_NOITE, tag_color=CINZA_NOITE).save(
        OUT / "dignitatis-logo-escuro.png"
    )
    print("  ✓ dignitatis-logo-escuro.png")

    # 5. Branco — tudo branco (para fundos escuros)
    BRANCO_TAG = (220, 215, 205, 255)
    make_completo(arc_color=BRANCO, dome_color=(200, 195, 185, 255),
                  text_color=BRANCO, tag_color=BRANCO_TAG).save(
        OUT / "dignitatis-logo-branco.png"
    )
    print("  ✓ dignitatis-logo-branco.png")


if __name__ == "__main__":
    print("Gerando variantes da logomarca Dignitatis (arco horizonte)...")
    save_variants()
    print(f"Concluído: {OUT}")
