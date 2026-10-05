# Note per Claude

- Sito: WordPress su https://www.roccoandrealigorio.it (nome sito "R.A.L.", tema Astra + Elementor).
  Utente WordPress: `admin`. Lingua dei contenuti: italiano.
- Il blog si gestisce con `blog-automatico/pubblica.py` (solo libreria standard Python).
  Credenziali in `blog-automatico/.env` (mai committare, mai chiederle in chat).
- Ogni articolo: `blog-automatico/articoli/<slug>/meta.json` + `articolo.html` (+ immagine).
  Pubblicare sempre prima come bozza (`draft`), salvo richiesta esplicita.
- Categorie esistenti: "Informatica", "Software su misura".
- Regole complete per scrivere articoli (quantità, argomenti, struttura, SEO, consegna):
  `blog-automatico/ISTRUZIONI-REDAZIONE.md`. Le bozze su WordPress le crea il workflow
  GitHub `bozze-wordpress.yml` al push su main: dal cloud di Claude il sito non è raggiungibile.
- Metadati SEO: `meta.json["seo"]` → post meta `ral_seo_*`, letti dallo snippet
  `wordpress/ral-seo.snippet.php` (WPCode).
- Stile degli articoli: pubblico di studi professionali e PMI, tono pratico e senza gergo,
  in prima persona; H2 per le sezioni, H3 per i sottopunti; chiusura con "Domande frequenti";
  link interni a /servizi/, /portfolio/, /come-lavoro/ quando pertinenti; fonti autorevoli
  con target="_blank" rel="noopener".
- Il lavoro va sempre committato e pushato su GitHub: niente deve esistere solo su un PC.
