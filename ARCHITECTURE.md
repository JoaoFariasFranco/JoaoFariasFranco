# Como este repositório funciona

O `README.md` do perfil é composto por quatro blocos SVG gerados por código. Nada
nele é escrito à mão.

> **O `README.md` é gerado.** Editar o arquivo direto funciona até alguém rodar
> `python -m builder`, que o sobrescreve. Para mudar o conteúdo, mexa em
> `content/` e regere.

```
┌──────────────────────────┬───────────────────────────────────┐
│  VISUAL_ART.asc          │  bash - profile.sh                │
│  arte ASCII + scanline   │  nome, cargo, detalhes, stack     │
├──────────────────────────┴───────────────────────────────────┤
│  contact.sh   ❯ GitHub  ❯ LinkedIn  ❯ Portfólio  ❯ E-mail    │
├──────────────────────────────────────────────────────────────┤
│  JoaoFariasFranco@github: ~/contributions --graph            │
└──────────────────────────────────────────────────────────────┘
```

---

## Estrutura

```
content/            conteúdo editável, sem código
  profile.json      nome, cargo, detalhes, stack, links
  ascii-art.txt     a arte (38 linhas)
data/
  contributions.json    buscado da API do GitHub, diariamente
assets/             gerado — 14 SVGs
builder/            o gerador, em camadas
scripts/
  fetch_contributions.py
README.md           gerado
```

O `builder` tem dependência em uma direção só:

```
theme → content → layout → blocks → page
```

| módulo | responsabilidade |
|---|---|
| `theme.py` | paleta dos dois temas e ritmo das animações |
| `content.py` | lê `content/`, expõe como constantes |
| `layout.py` | geometria dos painéis e helpers de SVG |
| `blocks.py` | desenha os quatro blocos |
| `page.py` | monta o `README.md` |
| `__main__.py` | linha de comando |

---

## Comandos

```bash
python -m builder            # regera os 14 SVGs e o README.md
python -m builder --graph    # regera só os 2 do gráfico
```

O `--graph` existe porque **só o gráfico depende de dados**. Arte, perfil e
contact são estáticos: o conteúdo deles não muda de um dia para o outro. O cron
diário usa `--graph` e commita apenas `assets/graph-*.svg`.

## O que mexer para mudar o quê

| quero mudar | onde |
|---|---|
| nome, cargo, detalhes, chips da stack, links | `content/profile.json` |
| a arte ASCII | `content/ascii-art.txt` |
| cores dos temas | `builder/theme.py`, dicionário `THEMES` |
| velocidade do preenchimento do gráfico | `builder/theme.py`: `COL_T`, `ROW_T`, `CELL_DUR` |
| tempos das revelações | `builder/blocks.py`, argumentos `begin`/`dur` |
| tamanho dos painéis | `builder/layout.py` |

Depois de qualquer mudança: `python -m builder`.

---

## O que restringe o desenho

O GitHub remove `style` e `<style>` do markdown. Sem CSS, três coisas ficam
impossíveis, e elas explicam quase todas as decisões aqui:

- **Não dá para sobrepor imagens.** Não existe fundo compartilhado nem uma
  scanline atravessando os quatro blocos — cada SVG carrega os próprios efeitos.
- **Não dá para impedir quebra de linha.** Imagens têm ponto de quebra entre si
  mesmo sem espaço em branco no HTML (são *contingent break* no algoritmo do
  Unicode). A única defesa é largura percentual.
- **Não existe `:hover`.** SVG dentro de `<img>` não recebe interação.

E uma quarta, do próprio HTML: **uma imagem aceita um link só**. É por isso que o
`contact.sh` é fatiado.

---

## As sete armadilhas

Coisas que quebram em silêncio e já quebraram pelo menos uma vez.

### 1. As larguras têm que ser proporcionais aos viewBox

Os dois blocos da primeira fileira precisam terminar com a **mesma altura**.
Como escalam por `max-width`, isso só acontece se as porcentagens forem
proporcionais às larguras do viewBox:

```
art     328 × 391  →  38.3%     328/840 × 98%
profile 512 × 391  →  59.7%     512/840 × 98%
```

Mexeu em `ART_W`? As porcentagens mudam junto. É por isso que o `README.md` é
gerado por `page.py` a partir das mesmas constantes, em vez de escrito à mão.

### 2. Espaço em branco entre as tags vira quebra de linha

No `README.md`, as tags de uma mesma fileira ficam **coladas**, sem espaço nem
newline entre elas. O respiro visual vem de margem transparente **dentro** do
SVG (`MID = 8`), não do HTML.

### 3. Cada fatia do contact desenha o card inteiro

O `contact.sh` é um card de 840px cortado em quatro janelas de 210px pelo
`viewBox`. Cada fatia contém o **desenho completo**, e só a janela muda:

```
fatia 0: viewBox="0 0 210 104"     fatia 2: viewBox="420 0 210 104"
fatia 1: viewBox="210 0 210 104"   fatia 3: viewBox="630 0 210 104"
```

Se cada fatia desenhasse só o próprio pedaço, os gradientes seriam calculados
sobre 210px e reiniciariam quatro vezes — a borda teria quatro ciclos de cor em
vez de um atravessando o bloco.

### 4. Texto precisa de `textLength`

Consolas não existe em macOS nem em Linux, e o monoespaçado substituto é mais
largo. Sem `textLength` + `lengthAdjust="spacingAndGlyphs"`, o texto vaza para
fora do painel nesses sistemas. Foi assim que a arte ASCII estourava o card.

### 5. `&` em atributo tem que ser escapado

O cargo tem um `&`. Um `&` cru dentro de `alt` ou `title` é HTML inválido:
navegador tolera, parser de markdown estrito descarta o bloco inteiro e o
preview não abre. `page.py` escapa via `attr()`.

### 6. `ascii-art.txt` termina com quebra de linha

`split("\n")` produziria uma 39ª linha vazia, mudando `len(ART)` e portanto a
altura da fileira inteira. `content.py` faz `rstrip("\n")` antes.

### 7. A scanline vive só no bloco da arte

Cada SVG é um documento independente, com relógio de animação próprio. Uma
scanline em vários blocos apareceria dessincronizada entre eles. Como só o bloco
da arte anima, o problema não existe.

---

## Animações

Tudo congela no fim (`fill="freeze"`), exceto a scanline e o cursor.

| bloco | animação | início | duração |
|---|---|---|---|
| art | cortina descendo sobre a arte | 0,2s | 2s |
| art | `< SYSTEM_INITIALIZED />` em fade | 2,2s | 0,8s |
| art | scanline | — | 8s, em loop |
| profile | nome revelado da esquerda p/ direita | 0,8s | 1s |
| profile | linha do cargo revelada | 1,9s | 1,2s |
| profile | bloco de detalhes revelado | 3,2s | 1,8s |
| profile | divisória em fade | 1,5s | 0,8s |
| profile | Core Tech Stack em fade | 2,0s | 0,8s |
| profile | cursor piscando | — | 1s, em loop |
| contact | botões em fade | 2,5s | 1s |
| graph | células subindo, escalonadas | — | 9,65s no total |

O ritmo do gráfico vem de `COL_T`, `ROW_T` e `CELL_DUR`: cada coluna atrasa
0,108s, cada linha 0,270s, cada célula dura 2,52s. Daí os 9,65s até preencher.

---

## O ciclo diário

`.github/workflows/update-contributions.yml`, todo dia à 01:00 UTC:

1. `scripts/fetch_contributions.py` → grava `data/contributions.json`
2. `python -m builder --graph` → regera `assets/graph-{dark,light}.svg`
3. commita se houver diferença

Não toca no `README.md` nem nos outros 12 SVGs.

---

## Como conferir uma mudança

```bash
python -m builder
python -c "import glob,xml.etree.ElementTree as ET; [ET.parse(f) for f in glob.glob('assets/*.svg')]"
python -c "import re,os; s=open('README.md',encoding='utf-8').read(); \
print([p for p in re.findall(r'srcset=\"([^\"]+)\"',s) if not os.path.exists(p.lstrip('./'))] or 'ok')"
```

Renderizar num navegador **não** pega tudo: navegador é tolerante justamente
onde o parser do markdown é estrito. O `&` cru da armadilha 5 passou nesse teste
e quebrou o preview.
