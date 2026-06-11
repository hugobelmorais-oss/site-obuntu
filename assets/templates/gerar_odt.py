"""
Gerador de templates ODT da Dignitatis usando zipfile (sem LibreOffice).
Cria arquivos OpenDocument Text (.odt) válidos e editáveis no LibreOffice/OnlyOffice.
"""

import zipfile
from pathlib import Path

OUT = Path(__file__).parent

MIMETYPE = "application/vnd.oasis.opendocument.text"

MANIFEST = """\
<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
                   manifest:version="1.2">
  <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.text"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
</manifest:manifest>"""

META = """\
<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                      xmlns:dc="http://purl.org/dc/elements/1.1/"
                      xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
                      office:version="1.2">
  <office:meta>
    <dc:creator>Dignitatis</dc:creator>
    <meta:generator>Dignitatis Template Generator</meta:generator>
  </office:meta>
</office:document-meta>"""

STYLES = """\
<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:styles>

    <style:style style:name="Standard" style:family="paragraph" style:class="text">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.212cm"/>
      <style:text-properties fo:font-size="11pt" style:font-name="Source Sans Pro" fo:color="#1c1c1c"/>
    </style:style>

    <style:style style:name="Heading1" style:family="paragraph"
                 style:parent-style-name="Standard" style:class="text">
      <style:paragraph-properties fo:text-align="left" fo:margin-top="0.4cm" fo:margin-bottom="0.2cm"/>
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"
                             style:font-name="Fraunces" fo:color="#b54e31"/>
    </style:style>

    <style:style style:name="Heading2" style:family="paragraph"
                 style:parent-style-name="Standard" style:class="text">
      <style:paragraph-properties fo:margin-top="0.3cm" fo:margin-bottom="0.15cm"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold"
                             style:font-name="Fraunces" fo:color="#0f1f3d"/>
    </style:style>

    <style:style style:name="OrgName" style:family="paragraph"
                 style:parent-style-name="Standard" style:class="text">
      <style:paragraph-properties fo:text-align="center" fo:margin-bottom="0.1cm"/>
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"
                             style:font-name="Fraunces" fo:color="#0f1f3d"/>
    </style:style>

    <style:style style:name="Tagline" style:family="paragraph"
                 style:parent-style-name="Standard" style:class="text">
      <style:paragraph-properties fo:text-align="center" fo:margin-bottom="0.3cm"/>
      <style:text-properties fo:font-size="8pt" style:font-name="Fraunces" fo:color="#9e8e7c"/>
    </style:style>

    <style:style style:name="Footer" style:family="paragraph"
                 style:parent-style-name="Standard" style:class="text">
      <style:paragraph-properties fo:text-align="center" fo:margin-top="0.3cm"/>
      <style:text-properties fo:font-size="7pt" style:font-name="Source Sans Pro" fo:color="#9e8e7c"/>
    </style:style>

    <style:style style:name="FieldLabel" style:family="paragraph"
                 style:parent-style-name="Standard" style:class="text">
      <style:paragraph-properties fo:margin-bottom="0.1cm"/>
      <style:text-properties fo:font-size="10pt" style:font-name="Source Sans Pro" fo:color="#1c1c1c"/>
    </style:style>

    <style:style style:name="Cover" style:family="paragraph"
                 style:parent-style-name="Standard" style:class="text">
      <style:paragraph-properties fo:text-align="center" fo:margin-bottom="0.4cm"/>
      <style:text-properties fo:font-size="28pt" fo:font-weight="bold"
                             style:font-name="Fraunces" fo:color="#b54e31"/>
    </style:style>

  </office:styles>

  <office:automatic-styles>
    <style:page-layout style:name="PageLayout">
      <style:page-layout-properties fo:page-width="21cm" fo:page-height="29.7cm"
                                    fo:margin-top="2.5cm" fo:margin-bottom="2.5cm"
                                    fo:margin-left="3cm" fo:margin-right="2cm"/>
    </style:page-layout>
  </office:automatic-styles>

  <office:master-styles>
    <style:master-page style:name="Standard" style:page-layout-name="PageLayout"/>
  </office:master-styles>

</office:document-styles>"""


def para(text, style="Standard", bold=False):
    b_open  = '<text:span text:style-name="Bold">' if bold else ""
    b_close = "</text:span>" if bold else ""
    return (
        f'<text:p text:style-name="{style}">'
        f"{b_open}{_esc(text)}{b_close}"
        f"</text:p>\n"
    )


def _esc(t):
    return (t.replace("&", "&amp;")
              .replace("<", "&lt;")
              .replace(">", "&gt;"))


def hr():
    return '<text:p text:style-name="Standard"><text:line-break/></text:p>\n'


def field_para(label, value):
    return (
        f'<text:p text:style-name="FieldLabel">'
        f'<text:span fo:font-weight="bold" fo:color="#0f1f3d">{_esc(label)} </text:span>'
        f'{_esc(value)}'
        f'</text:p>\n'
    )


def header_block(subtitulo=""):
    out = para("DIGNITATIS", style="OrgName")
    out += para("Direitos Humanos · Paraíba · Brasil", style="Tagline")
    if subtitulo:
        out += para(subtitulo, style="Tagline")
    out += hr()
    return out


def footer_block():
    out = hr()
    out += para(
        "[Nome Legal da Organização]  ·  CNPJ: [00.000.000/0000-00]  ·  "
        "[Endereço]  ·  [Cidade/UF]  ·  [e-mail]  ·  [site]",
        style="Footer"
    )
    return out


def wrap_content(body: str) -> str:
    return f"""\
<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:automatic-styles/>
  <office:body>
    <office:text>
{body}
    </office:text>
  </office:body>
</office:document-content>"""


def write_odt(filename: str, content_xml: str):
    path = OUT / filename
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", MIMETYPE, compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/manifest.xml", MANIFEST)
        z.writestr("meta.xml", META)
        z.writestr("styles.xml", STYLES)
        z.writestr("content.xml", content_xml)
    print(f"  ✓ {filename}")
    return path


# ── 1. Ofício ────────────────────────────────────────────────────────────────
def gerar_oficio_odt():
    body = header_block("Organização de Direitos Humanos")
    body += hr()
    body += field_para("Ofício Nº:", "[000/ANO]")
    body += field_para("Data:", "[Cidade], [DD] de [mês] de [AAAA]")
    body += field_para("Para:", "[Nome do Destinatário]")
    body += field_para("Cargo:", "[Cargo/Instituição]")
    body += field_para("Assunto:", "[Assunto do ofício]")
    body += hr()
    body += para("Prezado(a) Senhor(a),")
    body += hr()
    for _ in range(3):
        body += para(
            "[Insira aqui o texto do ofício. Este é um parágrafo de exemplo "
            "que deve ser substituído pelo conteúdo real do documento.]"
        )
        body += hr()
    body += para("Atenciosamente,")
    body += hr()
    body += hr()
    body += para("_____________________________________________")
    body += para("[Nome Completo]")
    body += para("[Cargo na Organização]")
    body += para("DIGNITATIS")
    body += footer_block()
    write_odt("dignitatis_oficio.odt", wrap_content(body))


# ── 2. Relatório ─────────────────────────────────────────────────────────────
def gerar_relatorio_odt():
    # Capa
    body = hr()
    body += hr()
    body += para("RELATÓRIO", style="Cover")
    body += para("[Título do Relatório]", style="Heading1")
    body += para("Direitos Humanos · Paraíba · Brasil", style="Tagline")
    body += hr()
    body += para("Período: [mês/AAAA – mês/AAAA]", style="Tagline")
    body += para("Elaborado por: [Nome/Equipe]", style="Tagline")
    body += para("Data: [DD/MM/AAAA]", style="Tagline")
    body += hr()
    body += para("DIGNITATIS — Organização de Direitos Humanos", style="OrgName")
    body += '<text:p text:style-name="Standard"><text:soft-page-break/></text:p>\n'

    # Sumário
    body += header_block("Organização de Direitos Humanos")
    body += para("SUMÁRIO", style="Heading2")
    for i, sec in enumerate([
        "Apresentação", "Contexto e Objetivos", "Metodologia",
        "Resultados e Análise", "Conclusões e Recomendações",
        "Referências", "Anexos"
    ], 1):
        body += para(f"{i}. {sec}")
    body += '<text:p text:style-name="Standard"><text:soft-page-break/></text:p>\n'

    # Seções
    for titulo in ["1. Apresentação", "2. Contexto e Objetivos", "3. Metodologia"]:
        body += header_block("Organização de Direitos Humanos")
        body += para(titulo, style="Heading2")
        for _ in range(2):
            body += para(
                "[Insira aqui o conteúdo desta seção. Substitua este texto pelo "
                "conteúdo real do relatório.]"
            )
            body += hr()
        body += footer_block()
        body += '<text:p text:style-name="Standard"><text:soft-page-break/></text:p>\n'

    write_odt("dignitatis_relatorio.odt", wrap_content(body))


# ── 3. Comunicado ────────────────────────────────────────────────────────────
def gerar_comunicado_odt():
    body = header_block("Comunicado Institucional")
    body += hr()
    body += para("[Cidade], [DD] de [mês] de [AAAA]")
    body += hr()
    body += para("A quem possa interessar,")
    body += hr()
    for _ in range(4):
        body += para(
            "[Insira aqui o texto do comunicado. Este parágrafo deve ser "
            "substituído pelo conteúdo real.]"
        )
        body += hr()
    body += para("Respeitosamente,")
    body += hr()
    body += hr()
    body += para("[Nome Completo]")
    body += para("[Cargo]")
    body += para("DIGNITATIS")
    body += footer_block()
    write_odt("dignitatis_comunicado.odt", wrap_content(body))


if __name__ == "__main__":
    print("Gerando arquivos ODT...")
    gerar_oficio_odt()
    gerar_relatorio_odt()
    gerar_comunicado_odt()
    print("Concluído:", OUT)
