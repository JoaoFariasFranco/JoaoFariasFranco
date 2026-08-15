"""Paleta dos dois temas e ritmo das animacoes.

Tokens extraidos de vars(t) em "GitHub README v3.dc.html".
"""
THEMES = {
    "dark": dict(
        card="#030712", panel="rgba(15,23,42,0.6)", border="rgba(255,255,255,0.08)",
        strip="rgba(255,255,255,0.03)", glow="rgba(34,211,238,0.08)",
        gborder="rgba(34,211,238,0.25)", text="#F8FAFC", muted="#64748B", sub="#94A3B8",
        pu="#7C3AED", pu2="#A78BFA", cy="#22D3EE", gr="#10B981", am="#F59E0B", wt="#E2E8F0",
        ramp=["#1E293B", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"],
        chip_wt_border="rgba(226,232,240,0.3)", chip_wt_bg="rgba(226,232,240,0.06)",
    ),
    "light": dict(
        card="#F8FAFC", panel="#ffffff", border="rgba(15,23,42,0.12)",
        strip="rgba(15,23,42,0.03)", glow="rgba(8,145,178,0.06)",
        gborder="rgba(8,145,178,0.3)", text="#0F172A", muted="#64748B", sub="#475569",
        pu="#7C3AED", pu2="#7C3AED", cy="#0891B2", gr="#059669", am="#B45309", wt="#334155",
        ramp=["#E2E8F0", "#9be9a8", "#40c463", "#30a14e", "#216e39", "#15522a"],
        chip_wt_border="rgba(51,65,85,0.3)", chip_wt_bg="rgba(51,65,85,0.06)",
    ),
}

FONT = "Consolas, 'Courier New', ui-monospace, monospace"
ADV = 0.5498          # avanco do Consolas por em
LS = 0.3              # letter-spacing do mockup

# Ritmo do preenchimento do grafico: atraso por coluna, por linha e duracao de
# cada celula. Sao os valores calibrados no projeto original.
COL_T = 0.108
ROW_T = 0.270
CELL_DUR = 2.52
