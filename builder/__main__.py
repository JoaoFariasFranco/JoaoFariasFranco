"""python -m builder            regera tudo (mudou o design ou o conteudo)
python -m builder --graph     regera so o grafico (o unico que depende dos dados)
"""
import argparse
import json
import os
import xml.etree.ElementTree as ET

from . import ASSETS_DIR, DATA_FILE
from .blocks import render_art, render_contact, render_graph, render_profile
from . import page


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--graph", action="store_true",
                    help="so os blocos do grafico, os unicos que dependem de data/")
    so_grafico = ap.parse_args().graph

    os.makedirs(ASSETS_DIR, exist_ok=True)
    with open(DATA_FILE, encoding="utf-8") as f:
        dados = json.load(f)

    for tema in ("dark", "light"):
        saidas = [(f"graph-{tema}.svg", render_graph(tema, dados))]
        if not so_grafico:
            saidas += [(f"art-{tema}.svg", render_art(tema)),
                       (f"profile-{tema}.svg", render_profile(tema))]
            saidas += [(f"contact-{i}-{tema}.svg", render_contact(tema, i))
                       for i in range(4)]
        for nome, svg in saidas:
            caminho = os.path.join(ASSETS_DIR, nome)
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(svg)
            ET.parse(caminho)
        print(f"assets/{tema}: {len(saidas)} arquivo(s)")

    if not so_grafico:
        print("README.md:", os.path.basename(page.write()))


main()
