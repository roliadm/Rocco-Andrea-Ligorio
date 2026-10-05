# Istruzioni di redazione — blog di roccoandrealigorio.it

Queste regole valgono per chi scrive gli articoli, in particolare per l'attività
programmata giornaliera di Claude. Ogni articolo diventa una **bozza** su WordPress:
Rocco la rilegge e la pubblica lui.

## Quantità

- Massimo **2 articoli per esecuzione** (e quindi al giorno). Meglio 1 articolo solido che 2 deboli.
- Se non trovi un argomento valido e non già trattato, non scrivere nulla e dillo nel riepilogo.

## Argomenti

Tutto il mondo dell'informatica: sicurezza, backup, reti, cloud, hardware, sistemi operativi,
software e sviluppo, intelligenza artificiale, privacy e normative digitali (GDPR, NIS2…),
strumenti per l'ufficio, notizie e novità rilevanti, guide pratiche.

- Alterna: guide pratiche "evergreen" e temi d'attualità degli ultimi giorni.
- **Niente doppioni**: prima di scegliere, leggi titoli, slug e `seo.keyword` di tutte le
  cartelle in `articoli/` (contengono anche gli articoli già sul sito). Scarta temi già trattati
  o troppo simili, a meno di un aggiornamento con fatti nuovi.
- Per l'attualità cerca sul web le notizie degli ultimi giorni e verifica le date.

## Pubblico e tono

- Lettori: titolari e dipendenti di **studi professionali e PMI italiane**, non tecnici.
- Italiano chiaro, prima persona ("ti spiego", "vedo spesso"), pratico, senza gergo inutile;
  i termini tecnici vanno spiegati la prima volta.
- Nessuna affermazione inventata: ogni dato, data, versione o statistica va verificato
  con una ricerca. Cita fonti autorevoli (enti pubblici, ACN, CSIRT Italia, Garante Privacy,
  CISA, ENISA, documentazione ufficiale dei produttori) con link
  `target="_blank" rel="noopener"`. Parafrasa, non copiare: al massimo una citazione breve.

## Struttura (HTML in `articolo.html`)

- 900–1500 parole.
- Paragrafo iniziale con il problema concreto del lettore e cosa troverà nell'articolo.
- Sezioni con `<h2>`, sottopunti con `<h3>`; elenchi `<ul>`/`<ol>`; `<strong>` per i concetti chiave.
- Niente `<h1>` (lo mette il tema), niente stili inline, niente immagini nel testo.
- Quando pertinente, un link interno: `https://www.roccoandrealigorio.it/servizi/`,
  `/portfolio/`, `/come-lavoro/`, `/contatti/`, oppure a un articolo precedente del blog.
- Chiusura con `<h2>Domande frequenti</h2>` e 2–4 domande in `<h3>` con risposta breve.

## Metadati (`meta.json`)

```json
{
  "titolo": "Titolo dell'articolo (H1 della pagina)",
  "slug": "parole-chiave-separate-da-trattini",
  "estratto": "120–155 caratteri: è la meta description che il sito mostra a Google e sui social.",
  "categorie": ["Informatica"],
  "tag": ["3–5 tag"],
  "seo": {
    "titolo": "Titolo per Google, 50–60 caratteri, con la parola chiave all'inizio",
    "descrizione": "Meta description 120–155 caratteri, con parola chiave e beneficio per il lettore.",
    "keyword": "parola chiave principale"
  },
  "stato": "draft"
}
```

- **Categorie**: solo `Informatica` oppure `Software su misura` (sviluppo, app, gestionali).
- **Tag**: riusa quelli già presenti negli altri articoli quando ha senso; massimo 5.
- **Slug**: minuscolo, senza accenti né articoli/preposizioni inutili, max 6 parole.
- La parola chiave compare nel titolo SEO, nella descrizione, nel primo paragrafo e in almeno un `<h2>`.
- Non serve l'immagine: la copertina la genera automaticamente il workflow GitHub.

## Consegna

1. Crea `blog-automatico/articoli/<slug>/meta.json` e `articolo.html`.
2. Valida: `python3 -c "import json;json.load(open('…/meta.json'))"`, conta le parole,
   controlla le lunghezze dei campi SEO e che l'HTML sia ben formato.
3. Commit su `main` (un commit per esecuzione) e push. Il workflow **Bozze WordPress**
   crea le bozze sul sito.
4. Riepilogo finale: per ogni articolo titolo, parola chiave e una riga sul contenuto, più il link
   per approvare le bozze: https://www.roccoandrealigorio.it/wp-admin/edit.php?post_status=draft&post_type=post
