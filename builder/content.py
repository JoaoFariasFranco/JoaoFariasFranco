"""Carrega o conteudo editavel de content/, para que trocar nome, cargo,
stack ou links nao exija mexer em codigo."""
import json
import os

from . import CONTENT_DIR

with open(os.path.join(CONTENT_DIR, "profile.json"), encoding="utf-8") as f:
    _p = json.load(f)

USERNAME = _p["username"]
NAME = _p["name"]
ROLE = _p["role"]
DETAILS = [(d["label"], d["value"], d.get("cursor", False)) for d in _p["details"]]
CHIPS = [(c["label"], c["color"]) for c in _p["chips"]]
LINKS = [(l["label"], l["color"], l["href"]) for l in _p["links"]]

with open(os.path.join(CONTENT_DIR, "ascii-art.txt"), encoding="utf-8") as f:
    # rstrip: o arquivo termina com quebra de linha, que viraria uma 39a linha
    # vazia e mudaria a altura dos blocos da primeira fileira
    ART = f.read().rstrip("\n").split("\n")

GRAPH_TITLE = f"{USERNAME}@github: ~/contributions --graph"
