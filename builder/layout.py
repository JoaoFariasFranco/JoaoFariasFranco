"""Geometria dos paineis, helpers de SVG e as animacoes de revelacao."""
from .content import ART, CHIPS, DETAILS
from .theme import ADV, FONT, LS

def w(text, size, ls=LS):
    """Largura aproximada de um texto monoespacado."""
    return len(text) * (size * ADV + ls)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


CARD_W = 880
PAD = 20              # padding interno do card externo
GAP = 16              # gap entre as linhas
ART_W = 320           # coluna da esquerda (grid-template-columns: 320px 1fr)
INNER = CARD_W - 2 * PAD
TERM_W = INNER - ART_W - GAP

STRIP_H = 32          # faixa de titulo dos paineis
PANEL_RX = 12

ART_FS, ART_LH = 6.6, 8.0

LABEL_COL, ROW_GAP, DET_FS = 104, 9, 13
CHIP_FS, CHIP_PADX, CHIP_H, CHIP_GAP = 12, 16, 28, 9
LINK_H, LINK_FS, LINK_GAP = 40, 13, 14

CELL, CGAP = 11, 3
CSTEP = CELL + CGAP
HM_LEFT = 34


# do terminal sao reveladas da esquerda para a direita e os blocos de baixo
# aparecem em fade. Todas congelam no fim (fill="freeze").
def wipe(cid, x, y, pw, ph, begin, dur):
    """Cortina horizontal: revela da esquerda para a direita."""
    return (f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="0" height="{ph:.1f}">'
            f'<animate attributeName="width" from="0" to="{pw:.1f}" dur="{dur}" '
            f'begin="{begin}" fill="freeze"/></rect></clipPath>')


def curtain(cid, x, y, pw, ph, begin, dur):
    """Cortina vertical: revela de cima para baixo."""
    return (f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{pw:.1f}" height="0">'
            f'<animate attributeName="height" from="0" to="{ph:.1f}" dur="{dur}" begin="{begin}" '
            f'fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/></rect></clipPath>')


def fade(begin, dur="0.8s"):
    return (f'<animate attributeName="opacity" from="0" to="1" begin="{begin}" '
            f'dur="{dur}" fill="freeze"/>')


# ------------------------------------------------------------------ blocos ---
def panel(x, y, pw, ph, title, t, dots=False):
    """Painel com faixa de titulo, igual aos do mockup."""
    o = [f'<g><rect x="{x}" y="{y}" width="{pw}" height="{ph}" rx="{PANEL_RX}" '
         f'fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.2"/>',
         f'<path d="M{x},{y+PANEL_RX} q0,-{PANEL_RX} {PANEL_RX},-{PANEL_RX} '
         f'L{x+pw-PANEL_RX},{y} q{PANEL_RX},0 {PANEL_RX},{PANEL_RX} '
         f'L{x+pw},{y+STRIP_H} L{x},{y+STRIP_H} Z" fill="{t["strip"]}"/>',
         f'<line x1="{x}" y1="{y+STRIP_H}" x2="{x+pw}" y2="{y+STRIP_H}" stroke="{t["border"]}"/>']
    if dots:
        for i, c in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
            o.append(f'<circle cx="{x+19+i*16}" cy="{y+STRIP_H/2}" r="5" fill="{c}"/>')
    o.append(f'<text x="{x+pw/2}" y="{y+STRIP_H/2+4}" fill="{t["muted"]}" font-size="11" '
             f'text-anchor="middle" letter-spacing="0.5">{esc(title)}</text>')
    o.append("</g>")
    return o



def term_height():
    """Altura do painel do terminal, para dimensionar a linha 1."""
    h = STRIP_H + 22 + 24 + 14 + 18 + 14 + 14
    h += len(DETAILS) * (DET_FS + ROW_GAP)
    h += 18 + 14 + 14 + 10
    avail = TERM_W - 52
    lx, lines = 0, 1
    for label, _ in CHIPS:
        cw = CHIP_PADX * 2 + w(label, CHIP_FS)
        if lx > 0 and lx + cw > avail:
            lx, lines = 0, lines + 1
        lx += cw + CHIP_GAP
    return h + lines * CHIP_H + (lines - 1) * CHIP_GAP + 22


MID = 8                                   # metade do gap de 16 do mockup
A_W = ART_W + MID                         # 328
T_W = TERM_W + MID                        # 512
ROW_W = A_W + T_W                         # 840 = INNER
ROW_H = max(term_height(), STRIP_H + len(ART) * ART_LH + 28 + 24)

CONTACT_H = STRIP_H + 16 + LINK_H + 16
SLICE_W = INNER // 4                       # 210


def head(vw, vh, view=None):
    vb = view or f"0 0 {vw} {vh:.0f}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
            f'width="{vw}" height="{vh:.0f}" font-family="{FONT}" letter-spacing="{LS}">')
