"""Gerador dos blocos SVG do README.

Camadas:
    theme    paleta dos temas e ritmo das animacoes
    content  le content/ (conteudo editavel, sem codigo)
    layout   geometria dos paineis e helpers de SVG
    blocks   os quatro blocos
    page     monta o README.md a partir da geometria
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content")
ASSETS_DIR = os.path.join(ROOT, "assets")
DATA_FILE = os.path.join(ROOT, "data", "contributions.json")
README_FILE = os.path.join(ROOT, "README.md")
