#!/usr/bin/env python3
"""
Genera l'immagine di copertina (1200x630, formato anteprima social) per un articolo
che non ne ha una, e la registra in meta.json.

  python copertina.py articoli/<cartella>

Richiede Pillow (pip install pillow). Usata dal workflow GitHub prima della pubblicazione.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LARG, ALT = 1200, 630
MARGINE = 80
FONT_CANDIDATI = {
    "bold": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf",
             "/System/Library/Fonts/Supplemental/Arial Bold.ttf"],
    "regular": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf",
                "/System/Library/Fonts/Supplemental/Arial.ttf"],
}
# coppie di colori scure per lo sfondo, scelte in modo stabile dallo slug
PALETTE = [((15, 32, 67), (32, 92, 160)), ((20, 40, 40), (22, 120, 110)),
           ((40, 24, 60), (110, 60, 160)), ((30, 30, 36), (70, 80, 100)),
           ((50, 26, 20), (170, 80, 40))]


def font(tipo: str, dim: int):
    for percorso in FONT_CANDIDATI[tipo]:
        if Path(percorso).exists():
            return ImageFont.truetype(percorso, dim)
    return ImageFont.load_default(size=dim)


def a_capo(testo: str, f, larghezza: int, draw) -> list[str]:
    righe, riga = [], ""
    for parola in testo.split():
        prova = f"{riga} {parola}".strip()
        if draw.textlength(prova, font=f) <= larghezza:
            riga = prova
        else:
            righe.append(riga)
            riga = parola
    righe.append(riga)
    return righe


def genera(titolo: str, categoria: str, slug: str, destinazione: Path):
    indice = int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(PALETTE)
    c1, c2 = PALETTE[indice]
    img = Image.new("RGB", (LARG, ALT), c1)
    draw = ImageDraw.Draw(img)
    for y in range(ALT):  # sfumatura diagonale semplice
        t = y / ALT
        colore = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        draw.line([(0, y), (LARG, y)], fill=colore)
    accento = tuple(min(255, int(v * 0.35 + 255 * 0.65)) for v in c2)

    # titolo: riduce il corpo finché sta in 4 righe
    for dim in (68, 60, 54, 48, 42):
        f_tit = font("bold", dim)
        righe = a_capo(titolo, f_tit, LARG - 2 * MARGINE, draw)
        if len(righe) <= 4:
            break
    f_cat = font("regular", 28)
    draw.text((MARGINE, 70), categoria.upper(), font=f_cat, fill=accento)
    draw.rectangle([MARGINE, 118, MARGINE + 90, 124], fill=accento)
    y = 160
    for riga in righe[:4]:
        draw.text((MARGINE, y), riga, font=f_tit, fill="white")
        y += int(dim * 1.22)
    f_sito = font("bold", 26)
    draw.text((MARGINE, ALT - 110), "roccoandrealigorio.it", font=f_sito, fill=(230, 236, 245))
    img.save(destinazione, "PNG", optimize=True)


def main():
    if len(sys.argv) != 2:
        sys.exit("Uso: python copertina.py articoli/<cartella>")
    cartella = Path(sys.argv[1])
    meta_file = cartella / "meta.json"
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    if meta.get("immagine") and (cartella / meta["immagine"]).exists():
        print(f"{cartella.name}: copertina già presente")
        return
    nome = "copertina.png"
    categoria = (meta.get("categorie") or ["Informatica"])[0]
    genera(meta["titolo"], categoria, meta["slug"], cartella / nome)
    meta["immagine"] = nome
    meta.setdefault("immagine_alt", meta["titolo"])
    meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{cartella.name}: copertina generata")


if __name__ == "__main__":
    main()
