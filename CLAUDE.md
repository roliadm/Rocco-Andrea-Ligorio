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
- Snippet WPCode attivi sul sito che riguardano il blog:
  - id 151 "Blog – stile, intestazione e SEO articoli" (non nel repo, creato prima): stile scuro,
    meta description dall'estratto, Open Graph, JSON-LD, autenticazione `X-RAL-Auth`
    (Aruba elimina `Authorization`) ed email "Nuova bozza da approvare" a ogni bozza creata dallo script.
  - id 213 "RAL SEO" = `wordpress/ral-seo.snippet.php`: campi `ral_seo_*`, `ral_seo_title` come
    `<title>`, e completa ciò che il 151 non fa: canonical della pagina Blog, twitter:title/
    description/image delle categorie, SEO completa (titolo, canonical, description, OG, Twitter)
    delle pagine tag, canonical di archivi autore/data. Non ripetere tag già stampati dal 151.
  - Verifica: ogni pagina pubblica deve avere esattamente 1 canonical, 1 description e 1 di
    og:title/og:description/og:image/og:url/twitter:card/title/description/image.
- `meta.json["seo"]` → post meta `ral_seo_*`. La meta description pubblicata è l'**estratto**:
  scriverlo come una meta description (120–155 caratteri).
- Stile degli articoli: pubblico di studi professionali e PMI, tono pratico e senza gergo,
  in prima persona; H2 per le sezioni, H3 per i sottopunti; chiusura con "Domande frequenti";
  link interni a /servizi/, /portfolio/, /come-lavoro/ quando pertinenti; fonti autorevoli
  con target="_blank" rel="noopener".
- Il lavoro va sempre committato e pushato su GitHub: niente deve esistere solo su un PC.
- Cache Aruba HiSpeed Cache: il plugin la svuota da solo quando cambiano articoli, pagine,
  categorie, tag, menu o commenti (blog automatico compreso). NON la svuota per modifiche
  tecniche (snippet WPCode, personalizzazione tema, plugin, widget): dopo ognuna di queste,
  cliccare "Cancella cache" nella barra nera di wp-admin (voce `wp-admin-bar-ahsc-purge-link`;
  se il pannello è stretto e la voce non è visibile, simularne il click via JavaScript) e
  verificare la risposta "Cache cancellata correttamente".
