#!/usr/bin/env python3
"""
blog-automatico — pubblica articoli su WordPress (roccoandrealigorio.it)
tramite API REST e password applicativa.

Solo libreria standard Python 3.9+, nessuna dipendenza da installare.

Comandi:
  python pubblica.py verifica                     controlla credenziali e connessione
  python pubblica.py elenco                       mostra gli ultimi articoli sul sito
  python pubblica.py pubblica articoli/<cartella> [--stato draft|publish|future] [--data 2026-10-10T09:00]
  python pubblica.py scarica [--tutti]            salva gli articoli del sito in articoli/<slug>/

Ogni articolo è una cartella con:
  meta.json      titolo, slug, estratto, categorie, tag, immagine, stato, data
  articolo.html  corpo dell'articolo in HTML
  (opzionale) l'immagine in evidenza indicata in meta.json
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARTICOLI_DIR = BASE_DIR / "articoli"


# --------------------------------------------------------------------------- config

def carica_env() -> dict:
    """Legge .env (chiave=valore) accanto allo script, senza dipendenze."""
    env = {}
    file_env = BASE_DIR / ".env"
    if file_env.exists():
        for riga in file_env.read_text(encoding="utf-8").splitlines():
            riga = riga.strip()
            if not riga or riga.startswith("#") or "=" not in riga:
                continue
            k, v = riga.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("WP_URL", "WP_USER", "WP_APP_PASSWORD"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    mancanti = [k for k in ("WP_URL", "WP_USER", "WP_APP_PASSWORD") if not env.get(k)]
    if mancanti:
        sys.exit(f"Mancano in .env: {', '.join(mancanti)}. Copia .env.example in .env e compilalo.")
    env["WP_URL"] = env["WP_URL"].rstrip("/")
    # le password applicative si mostrano con spazi: vanno bene anche senza
    env["WP_APP_PASSWORD"] = env["WP_APP_PASSWORD"].replace(" ", "")
    return env


# --------------------------------------------------------------------------- client

class WordPress:
    def __init__(self, url: str, utente: str, password_app: str):
        self.api = f"{url}/wp-json/wp/v2"
        token = base64.b64encode(f"{utente}:{password_app}".encode()).decode()
        self.headers = {"Authorization": f"Basic {token}", "User-Agent": "blog-automatico/1.0"}

    def _richiesta(self, metodo: str, percorso: str, dati=None, corpo: bytes | None = None,
                   headers_extra: dict | None = None):
        url = percorso if percorso.startswith("http") else f"{self.api}{percorso}"
        headers = dict(self.headers)
        if dati is not None:
            corpo = json.dumps(dati).encode("utf-8")
            headers["Content-Type"] = "application/json; charset=utf-8"
        if headers_extra:
            headers.update(headers_extra)
        req = urllib.request.Request(url, data=corpo, method=metodo, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                testo = r.read().decode("utf-8")
                return json.loads(testo) if testo else None, r.headers
        except urllib.error.HTTPError as e:
            dettaglio = e.read().decode("utf-8", "replace")
            try:
                dettaglio = json.loads(dettaglio).get("message", dettaglio)
            except ValueError:
                pass
            sys.exit(f"Errore {e.code} su {metodo} {url}: {dettaglio}")
        except urllib.error.URLError as e:
            sys.exit(f"Impossibile raggiungere {url}: {e.reason}")

    def get(self, percorso, **params):
        q = f"?{urllib.parse.urlencode(params)}" if params else ""
        return self._richiesta("GET", f"{percorso}{q}")[0]

    def get_con_headers(self, percorso, **params):
        q = f"?{urllib.parse.urlencode(params)}" if params else ""
        return self._richiesta("GET", f"{percorso}{q}")

    def post(self, percorso, dati):
        return self._richiesta("POST", percorso, dati=dati)[0]

    # ---- tassonomie: risolve per nome, crea se manca
    def id_termini(self, tipo: str, nomi: list[str]) -> list[int]:
        ids = []
        for nome in nomi:
            trovati = self.get(f"/{tipo}", search=nome, per_page=100)
            esatto = next((t for t in trovati if t["name"].lower() == nome.lower()), None)
            if esatto:
                ids.append(esatto["id"])
            else:
                nuovo = self.post(f"/{tipo}", {"name": nome})
                print(f"  creato {'tag' if tipo == 'tags' else 'categoria'}: {nome}")
                ids.append(nuovo["id"])
        return ids

    def carica_media(self, file: Path, alt: str = "") -> int:
        tipo = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
        nome = urllib.parse.quote(file.name)
        media, _ = self._richiesta(
            "POST", "/media", corpo=file.read_bytes(),
            headers_extra={"Content-Type": tipo,
                           "Content-Disposition": f"attachment; filename*=UTF-8''{nome}"})
        if alt:
            self.post(f"/media/{media['id']}", {"alt_text": alt})
        return media["id"]

    def post_per_slug(self, slug: str):
        trovati = self.get("/posts", slug=slug, status="publish,draft,future,pending,private",
                           context="edit")
        return trovati[0] if trovati else None


# --------------------------------------------------------------------------- comandi

def cmd_verifica(wp: WordPress, _args):
    me = wp.get("/users/me", context="edit")
    print(f"OK: connesso come '{me['username']}' (ruoli: {', '.join(me.get('roles', []))})")


def cmd_elenco(wp: WordPress, _args):
    posts = wp.get("/posts", per_page=20, status="publish,draft,future", context="edit",
                   orderby="date", order="desc")
    for p in posts:
        print(f"{p['id']:>5}  {p['status']:<8} {p['date'][:16]}  {p['slug']:<45} {p['title']['raw']}")


def cmd_pubblica(wp: WordPress, args):
    cartella = Path(args.cartella)
    if not cartella.is_absolute():
        cartella = (Path.cwd() / cartella) if (Path.cwd() / cartella).exists() else BASE_DIR / cartella
    meta_file, html_file = cartella / "meta.json", cartella / "articolo.html"
    if not meta_file.exists() or not html_file.exists():
        sys.exit(f"In {cartella} servono meta.json e articolo.html")

    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    contenuto = html_file.read_text(encoding="utf-8")
    for campo in ("titolo", "slug"):
        if not meta.get(campo):
            sys.exit(f"meta.json: manca '{campo}'")

    stato = args.stato or meta.get("stato", "draft")
    data = args.data or meta.get("data")
    if stato == "future" and not data:
        sys.exit("Per programmare (stato 'future') serve una data, es. --data 2026-10-10T09:00")

    print(f"Articolo: {meta['titolo']}")
    dati = {
        "title": meta["titolo"],
        "slug": meta["slug"],
        "content": contenuto,
        "excerpt": meta.get("estratto", ""),
        "status": stato,
        "categories": wp.id_termini("categories", meta.get("categorie", [])) or [1],
        "tags": wp.id_termini("tags", meta.get("tag", [])),
    }
    if data:
        dati["date"] = data

    esistente = wp.post_per_slug(meta["slug"])

    immagine = meta.get("immagine")
    if immagine:
        file_img = cartella / immagine
        if not file_img.exists():
            sys.exit(f"Immagine non trovata: {file_img}")
        if esistente and esistente.get("featured_media") and not args.nuova_immagine:
            dati["featured_media"] = esistente["featured_media"]
        else:
            print(f"  carico immagine {file_img.name}…")
            dati["featured_media"] = wp.carica_media(file_img, meta.get("immagine_alt", meta["titolo"]))

    if esistente:
        risultato = wp.post(f"/posts/{esistente['id']}", dati)
        azione = "aggiornato"
    else:
        risultato = wp.post("/posts", dati)
        azione = "creato"

    meta["id"] = risultato["id"]
    meta["stato"] = risultato["status"]
    meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Fatto: {azione} (id {risultato['id']}, stato {risultato['status']})")
    print(f"  {risultato['link']}")


def cmd_scarica(wp: WordPress, args):
    """Salva gli articoli del sito nel repository: backup e base per modifiche."""
    pagina, salvati = 1, 0
    cache_cat, cache_tag = {}, {}

    def nomi(tipo, ids, cache):
        mancanti = [i for i in ids if i not in cache]
        if mancanti:
            for t in wp.get(f"/{tipo}", include=",".join(map(str, mancanti)), per_page=100):
                cache[t["id"]] = t["name"]
        return [cache[i] for i in ids if i in cache]

    while True:
        posts, headers = wp.get_con_headers("/posts", per_page=50, page=pagina, context="edit",
                                            status="publish,draft,future,pending,private")
        for p in posts:
            cartella = ARTICOLI_DIR / p["slug"]
            if cartella.exists() and not args.tutti:
                continue
            cartella.mkdir(parents=True, exist_ok=True)
            meta = {
                "id": p["id"],
                "titolo": p["title"]["raw"],
                "slug": p["slug"],
                "estratto": p["excerpt"]["raw"],
                "categorie": nomi("categories", p["categories"], cache_cat),
                "tag": nomi("tags", p["tags"], cache_tag),
                "stato": p["status"],
                "data": p["date"],
            }
            (cartella / "meta.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            (cartella / "articolo.html").write_text(p["content"]["raw"], encoding="utf-8")
            print(f"  salvato {p['slug']}")
            salvati += 1
        if pagina >= int(headers.get("X-WP-TotalPages", 1)):
            break
        pagina += 1
    print(f"Fatto: {salvati} articoli salvati in {ARTICOLI_DIR}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Pubblica articoli su WordPress")
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("verifica", help="controlla credenziali")
    sub.add_parser("elenco", help="ultimi articoli sul sito")
    p = sub.add_parser("pubblica", help="crea o aggiorna un articolo (per slug)")
    p.add_argument("cartella")
    p.add_argument("--stato", choices=["draft", "publish", "future", "pending", "private"])
    p.add_argument("--data", help="data di pubblicazione, es. 2026-10-10T09:00 (ora del sito)")
    p.add_argument("--nuova-immagine", action="store_true",
                   help="ricarica l'immagine anche se l'articolo ne ha già una")
    s = sub.add_parser("scarica", help="salva gli articoli del sito in articoli/")
    s.add_argument("--tutti", action="store_true", help="sovrascrive anche quelli già presenti")
    args = parser.parse_args()

    env = carica_env()
    wp = WordPress(env["WP_URL"], env["WP_USER"], env["WP_APP_PASSWORD"])
    {"verifica": cmd_verifica, "elenco": cmd_elenco,
     "pubblica": cmd_pubblica, "scarica": cmd_scarica}[args.comando](wp, args)


if __name__ == "__main__":
    main()
