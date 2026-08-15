"""Monta o README.md a partir da geometria real dos blocos.

As larguras percentuais precisam ser proporcionais as larguras dos viewBox,
senao os dois blocos da primeira linha terminam com alturas diferentes. Gerar
o README a partir das mesmas constantes elimina essa sincronia manual.
"""
from . import README_FILE
from .content import LINKS, NAME, ROLE
from .layout import A_W, ROW_W, T_W

TOTAL = 98.0        # largura de cada linha, em % do container


def attr(txt):
    """Escapa texto que vai dentro de um atributo HTML.

    O cargo tem um "&" ("Full Stack Developer & UI Engineer"). Um & cru dentro
    de atributo e HTML invalido: o navegador tolera, mas parsers de markdown
    mais estritos descartam o bloco inteiro.
    """
    return (txt.replace("&", "&amp;").replace("<", "&lt;")
               .replace(">", "&gt;").replace('"', "&quot;"))


def _picture(nome, largura, alt):
    return (f'<picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="./assets/{nome}-dark.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="./assets/{nome}-light.svg">'
            f'<img src="./assets/{nome}-dark.svg" width="{largura}" alt="{attr(alt)}">'
            f'</picture>')


def build():
    art = f"{TOTAL * A_W / ROW_W:.1f}%"
    perfil = f"{TOTAL * T_W / ROW_W:.1f}%"
    fatia = f"{TOTAL / 4:.1f}%"

    # sem espaco entre as tags: espaco em branco vira ponto de quebra de linha
    linha1 = _picture("art", art, "VISUAL_ART.asc") + _picture("profile", perfil, f"{NAME} - {ROLE}")
    linha2 = "".join(
        f'<a href="{attr(href)}" title="{attr(rotulo)}">'
        + _picture(f"contact-{i}", fatia, rotulo)
        + "</a>"
        for i, (rotulo, href) in enumerate(
            (l.replace("\u276f ", ""), h) for l, _, h in LINKS))
    linha3 = _picture("graph", f"{TOTAL:.0f}%", "Contribuicoes no ultimo ano")

    return "\n".join(f'<p align="center">\n  {linha}\n</p>\n'
                     for linha in (linha1, linha2, linha3))


def write():
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(build())
    return README_FILE
