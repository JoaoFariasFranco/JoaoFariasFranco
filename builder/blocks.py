"""Os quatro blocos do README, cada um um SVG auto-contido."""
import datetime

from .content import ART, CHIPS, DETAILS, GRAPH_TITLE, LINKS, NAME, ROLE
from .layout import (
    A_W, ART_FS, ART_LH, ART_W, CELL, CGAP, CHIP_FS, CHIP_GAP, CHIP_H, CHIP_PADX,
    CONTACT_H, CSTEP, DET_FS, HM_LEFT, INNER, LABEL_COL, LINK_FS,
    LINK_GAP, LINK_H, MID, PANEL_RX, ROW_GAP, ROW_H, ROW_W, SLICE_W, STRIP_H,
    T_W, TERM_W, curtain, esc, fade, head, panel, w, wipe,
)
from .theme import ADV, CELL_DUR, COL_T, FONT, LS, ROW_T, THEMES

def level_for(c):
    if c == 0: return 0
    if c <= 5: return 1
    if c <= 15: return 2
    if c <= 30: return 3
    if c <= 50: return 4
    return 5


def build_grid(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    grid, col = [], [None] * ((first.weekday() + 1) % 7)
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        wd = (date.weekday() + 1) % 7
        while len(col) < wd:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col); col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


# -------------------------------------------------------------- animacoes ---
# Tempos copiados do dark.svg original: a cortina da arte desce, as tres linhas


def art_panel(x, y, ph, t):
    o = panel(x, y, ART_W, ph, "VISUAL_ART.asc", t)
    art_h = len(ART) * ART_LH
    foot_h = 28
    top = y + STRIP_H + (ph - STRIP_H - foot_h - art_h) / 2
    tw = 75 * (ART_FS * ADV)
    ax = x + (ART_W - tw) / 2
    # cortina descendo sobre a arte (2s), como no dark.svg
    o.append(curtain("artReveal", x, y + STRIP_H, ART_W, ph - STRIP_H, "0.2s", "2s"))
    o.append('<g clip-path="url(#artReveal)">')
    o.append(f'<text x="{ax}" y="{top}" fill="url(#artGrad)" font-size="{ART_FS}" '
             f'font-weight="700" xml:space="preserve">')
    for row in ART:
        o.append(f'<tspan x="{ax:.1f}" dy="{ART_LH}" textLength="{tw:.1f}" '
                 f'lengthAdjust="spacingAndGlyphs">{esc(row)}</tspan>')
    o.append("</text>")
    o.append("</g>")
    # o rodape entra depois que a cortina termina
    o.append(f'<g opacity="0">{fade("2.2s")}'
             f'<text x="{x+ART_W/2}" y="{y+ph-11}" fill="{t["cy"]}" font-size="10" '
             f'letter-spacing="1" text-anchor="middle">&lt; SYSTEM_INITIALIZED /&gt;</text></g>')
    return o


def term_panel(x, y, ph, t):
    o = panel(x, y, TERM_W, ph, "bash - profile.sh", t, dots=True)
    cx, cy0 = x + 26, y + STRIP_H + 22

    cy0 += 24
    o.append(wipe("t-line1", x, cy0 - 30, TERM_W, 40, "0.8s", "1s"))
    o.append('<g clip-path="url(#t-line1)">')
    o.append(f'<text x="{cx}" y="{cy0}" font-size="24" font-weight="700" fill="{t["text"]}">'
             f'Hi, I\'m <tspan fill="url(#nameGrad)">{esc(NAME)}</tspan></text>')
    o.append("</g>")
    cy0 += 14 + 18
    o.append(wipe("t-line2", x, cy0 - 20, TERM_W, 28, "1.9s", "1.2s"))
    o.append('<g clip-path="url(#t-line2)">')
    o.append(f'<text x="{cx}" y="{cy0}" font-size="14" font-weight="600" fill="{t["sub"]}">'
             f'&gt; {esc(ROLE)}</text>')
    o.append("</g>")

    cy0 += 14 + 14
    det_h = len(DETAILS) * (DET_FS + ROW_GAP) + 8
    o.append(wipe("t-details", x, cy0 + 2, TERM_W, det_h, "3.2s", "1.8s"))
    o.append('<g clip-path="url(#t-details)">')
    for label, value, cursor in DETAILS:
        cy0 += DET_FS + ROW_GAP
        o.append(f'<text x="{cx}" y="{cy0}" font-size="{DET_FS}" font-weight="600" '
                 f'fill="{t["pu2"]}">{label}</text>')
        fill = t["sub"] if cursor else t["text"]
        o.append(f'<text x="{cx+LABEL_COL+12}" y="{cy0}" font-size="{DET_FS}" '
                 f'fill="{fill}">{esc(value)}</text>')
        if cursor:
            bx = cx + LABEL_COL + 12 + w(value, DET_FS) + 4
            o.append(f'<rect x="{bx:.1f}" y="{cy0-10}" width="8" height="13" fill="{t["cy"]}">'
                     f'<animate attributeName="opacity" values="1;1;0;0" dur="1s" '
                     f'repeatCount="indefinite"/></rect>')

    o.append("</g>")

    cy0 += 18
    o.append(f'<g opacity="0">{fade("1.5s")}'
             f'<line x1="{cx}" y1="{cy0}" x2="{x+TERM_W-26}" y2="{cy0}" stroke="{t["border"]}"/></g>')
    cy0 += 14 + 14
    # o bloco da stack entra junto, em fade, como no dark.svg
    o.append(f'<g opacity="0">{fade("2s")}')
    o.append(f'<text x="{cx}" y="{cy0}" font-size="14" font-weight="700" fill="{t["text"]}">'
             f'Core Tech Stack</text>')

    cy0 += 10
    avail = TERM_W - 52
    lx, ly = cx, cy0
    for label, key in CHIPS:
        cw = CHIP_PADX * 2 + w(label, CHIP_FS)
        if lx > cx and lx + cw - cx > avail:
            lx, ly = cx, ly + CHIP_H + CHIP_GAP
        color = t[key] if key != "pu" else t["pu2"]
        border = t["chip_wt_border"] if key == "wt" else (t["pu"] if key == "pu" else t[key])
        bg = t["chip_wt_bg"] if key == "wt" else f'{t[key if key != "pu" else "pu"]}1a'
        o.append(f'<rect x="{lx:.1f}" y="{ly}" width="{cw:.1f}" height="{CHIP_H}" '
                 f'rx="{CHIP_H/2}" fill="{bg}" stroke="{border}" stroke-width="1"/>')
        o.append(f'<text x="{lx+cw/2:.1f}" y="{ly+CHIP_H/2+4}" font-size="{CHIP_FS}" '
                 f'font-weight="600" fill="{t["wt"] if key == "wt" else color}" '
                 f'text-anchor="middle">{esc(label)}</text>')
        lx += cw + CHIP_GAP
    o.append("</g>")
    return o, ly + CHIP_H



def grads(art=False, name=False, scan=False, w=0, h=0):
    o = ['<defs>']
    if art:
        o.append('<linearGradient id="artGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
                 '<stop offset="0%" stop-color="#7C3AED"/><stop offset="50%" stop-color="#22D3EE"/>'
                 '<stop offset="100%" stop-color="#10B981"/></linearGradient>')
    if name:
        o.append('<linearGradient id="nameGrad" x1="0%" y1="0%" x2="100%" y2="0%">'
                 '<stop offset="0%" stop-color="#7C3AED"/><stop offset="50%" stop-color="#22D3EE"/>'
                 '<stop offset="100%" stop-color="#10B981"/></linearGradient>')
    if scan:
        # barra horizontal descendo -> o degrade corre na horizontal, para ela
        # esmaecer nas pontas esquerda e direita
        r = 12
        o.append('<linearGradient id="scanline" x1="0%" y1="0%" x2="100%" y2="0%">'
                 '<stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>'
                 '<stop offset="30%" stop-color="#22D3EE" stop-opacity="1"/>'
                 '<stop offset="70%" stop-color="#7C3AED" stop-opacity="1"/>'
                 '<stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/></linearGradient>'
                 '<filter id="neonGlow" x="-20%" y="-50%" width="140%" height="200%">'
                 '<feGaussianBlur stdDeviation="4" result="b"/><feMerge>'
                 '<feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
                 # recorte so do corpo do painel: comeca abaixo da faixa do titulo
                 # (topo reto) e acompanha os cantos arredondados de baixo
                 f'<clipPath id="artClip"><path d="M0,{STRIP_H} L{w},{STRIP_H} '
                 f'L{w},{h-r:.0f} Q{w},{h:.0f} {w-r},{h:.0f} L{r},{h:.0f} '
                 f'Q0,{h:.0f} 0,{h-r:.0f} Z"/></clipPath>')
    o.append('</defs>')
    return "".join(o)


# ------------------------------------------------------- 1. VISUAL_ART.asc ---
def render_art(theme):
    """Unico bloco com scanline, varrendo so dentro dele."""
    t = THEMES[theme]
    o = [head(A_W, ROW_H), grads(art=True, scan=True, w=ART_W, h=ROW_H)]
    o += art_panel(0, 0, ROW_H, t)
    # barra na horizontal descendo e voltando, presa ao corpo do painel:
    # o artClip comeca em STRIP_H, entao ela nunca invade a faixa VISUAL_ART.asc
    o.append(f'<g clip-path="url(#artClip)"><rect x="0" y="0" width="{ART_W}" height="3" '
             f'fill="url(#scanline)" filter="url(#neonGlow)" opacity="0.7">'
             f'<animate attributeName="y" values="{STRIP_H};{ROW_H:.0f};{STRIP_H}" dur="8s" '
             f'repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1"/>'
             f'</rect></g>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------- 2. bash - profile.sh ---
def render_profile(theme):
    t = THEMES[theme]
    o = [head(T_W, ROW_H), grads(name=True)]
    tp, _ = term_panel(MID, 0, ROW_H, t)
    o += tp
    o.append("</svg>")
    return "".join(o)


# -------------------------------------------------------- 3. contact.sh -----
def render_contact(theme, idx):
    """Fatia idx: desenha o bloco inteiro, o viewBox recorta a janela."""
    t = THEMES[theme]
    o = [head(SLICE_W, CONTACT_H, f"{SLICE_W*idx} 0 {SLICE_W} {CONTACT_H:.0f}"), grads()]
    o += panel(0, 0, INNER, CONTACT_H, "contact.sh", t)

    # fade dos botoes em 2.5s, o mesmo tempo da fileira de icones do dark.svg.
    # Duracao longa (1s) de proposito: cada fatia e um documento independente e
    # um desencontro de alguns milissegundos entre elas fica imperceptivel.
    o.append(f'<g opacity="0">{fade("2.5s", "1s")}')
    bw = (INNER - 32 - 3 * LINK_GAP) / 4
    for i, (label, key, _) in enumerate(LINKS):
        bx = 16 + i * (bw + LINK_GAP)
        by = STRIP_H + 16
        color = t["pu2"] if key == "pu" else t[key]
        stroke = t["pu"] if key == "pu" else t[key]
        o.append(f'<rect x="{bx:.1f}" y="{by}" width="{bw:.1f}" height="{LINK_H}" rx="8" '
                 f'fill="{t["pu" if key == "pu" else key]}14" stroke="{stroke}" stroke-width="1"/>')
        o.append(f'<text x="{bx+bw/2:.1f}" y="{by+LINK_H/2+4.5}" font-size="{LINK_FS}" '
                 f'font-weight="700" fill="{color}" text-anchor="middle">{esc(label)}</text>')
    o.append("</g>")
    o.append("</svg>")
    return "".join(o)


# ------------------------------------------------------------- 4. graph -----
def render_graph(theme, data):
    t = THEMES[theme]
    grid = build_grid(data["days"])
    art_h = 7 * CELL + 6 * CGAP
    h = STRIP_H + 16 + 16 + art_h + 8 + CELL + 26 + 40 + 16

    o = [head(INNER, h),
         f'<style>.cell{{opacity:0;animation:cell {CELL_DUR}s cubic-bezier(.2,.8,.2,1) both}}'
         '@keyframes cell{0%{opacity:0;transform:translateY(-6px)}'
         '100%{opacity:1;transform:translateY(0)}}</style>',
         grads()]
    o += panel(0, 0, INNER, h, GRAPH_TITLE, t)

    gx0, gy0 = 18 + HM_LEFT, STRIP_H + 16 + 16
    prev_m = None
    for ci, column in enumerate(grid):
        for c in column:
            if c is None:
                continue
            d = datetime.date.fromisoformat(c[0])
            if prev_m is not None and d.month != prev_m and d.day <= 7:
                o.append(f'<text x="{gx0+ci*CSTEP}" y="{gy0-6}" fill="{t["muted"]}" '
                         f'font-size="10">{d.strftime("%b")}</text>')
            if prev_m is None or d.month != prev_m:
                prev_m = d.month
            break
    for wi, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        o.append(f'<text x="18" y="{gy0+wi*CSTEP+CELL*0.8:.1f}" fill="{t["muted"]}" '
                 f'font-size="9">{name}</text>')
    for ci, column in enumerate(grid):
        for ri, c in enumerate(column):
            if c is None:
                continue
            date_s, count, lvl = c
            pl = "s" if count != 1 else ""
            o.append(f'<rect class="cell" x="{gx0+ci*CSTEP}" y="{gy0+ri*CSTEP}" width="{CELL}" '
                     f'height="{CELL}" rx="2" fill="{t["ramp"][lvl]}" '
                     f'style="animation-delay:{ci*COL_T+ri*ROW_T:.3f}s">'
                     f'<title>{date_s}: {count} contribution{pl}</title></rect>')

    ly = gy0 + art_h + 8
    lx = INNER - 18 - (len(t["ramp"]) * (CELL + 2) + 40)
    o.append(f'<text x="{lx-6}" y="{ly+CELL*0.85:.1f}" fill="{t["muted"]}" font-size="10" '
             f'text-anchor="end">Less</text>')
    for color in t["ramp"]:
        o.append(f'<rect x="{lx:.1f}" y="{ly}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>')
        lx += CELL + 2
    o.append(f'<text x="{lx+4:.1f}" y="{ly+CELL*0.85:.1f}" fill="{t["muted"]}" font-size="10">More</text>')

    sy = ly + CELL + 26
    total, rng = data["total_contributions"], data["range"]
    cs, ls_, best = data["current_streak"]["length"], data["longest_streak"]["length"], data["best_day"]
    o.append(f'<text x="18" y="{sy}" font-size="12" fill="{t["text"]}">'
             f'<tspan fill="{t["gr"]}" font-weight="700">{total}</tspan>'
             f'<tspan> contributions in the last year</tspan></text>')
    o.append(f'<text x="{INNER-18}" y="{sy}" font-size="12" fill="{t["muted"]}" '
             f'text-anchor="end">{rng["start"]} &#8594; {rng["end"]}</text>')
    sy += 20
    o.append(f'<text x="18" y="{sy}" font-size="12" fill="{t["muted"]}">current streak '
             f'<tspan fill="{t["cy"]}" font-weight="700">{cs} days</tspan>'
             f'<tspan> &#183; longest </tspan>'
             f'<tspan fill="{t["cy"]}" font-weight="700">{ls_} days</tspan></text>')
    o.append(f'<text x="{INNER-18}" y="{sy}" font-size="12" fill="{t["muted"]}" text-anchor="end">'
             f'best day <tspan fill="{t["gr"]}" font-weight="700">{best["count"]}</tspan> '
             f'on {best["date"]}</text>')
    o.append("</svg>")
    return "".join(o)
