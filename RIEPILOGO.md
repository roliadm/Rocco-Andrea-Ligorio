# Sito Rocco — riepilogo del lavoro

Sito: **https://www.roccoandrealigorio.it** (WordPress, tema Astra + Elementor, hosting Aruba)
Repository: **https://github.com/roliadm/Rocco-Andrea-Ligorio** (ramo `main`)
Ultimo aggiornamento di questo riepilogo: 5 ottobre 2026

---

## 1. Cosa è successo

- Il disco del vecchio PC si è rotto. La cartella `blog-automatico`, che esisteva solo lì,
  è andata persa. La sessione "Sito Rocco" di Claude era legata a quel PC e non si può più riprendere.
- Su Google Drive esiste un backup di **Progetti** dell'8 settembre 2026 (Ferruzzi-CRM, Preventivi,
  Interventi, Sito, ecc.), ma `blog-automatico` non c'era.
- Il 5 ottobre 2026 è stato tutto **ricostruito da zero su GitHub**, in modo che non dipenda più
  da nessun PC.

## 2. Come funziona il blog automatico (PC spento)

```
 12:54 ogni giorno            GitHub Actions                     Tu
 ──────────────────           ─────────────────                  ─────────────────
 Claude (nel cloud)    push   "Bozze WordPress"         email    Approvi e pubblichi
 scrive 1-2 articoli  ─────►  copertina + bozza  ─────────────►  da wp-admin o
 e li mette su GitHub         su WordPress + backup              dall'app WordPress
```

1. **Attività programmata di Claude** "Blog automatico - bozze giornaliere": ogni giorno alle
   **12:54** (ora di Roma) scrive al massimo **2 articoli** di informatica per studi e PMI,
   verifica i fatti sul web, evita i doppioni e li inserisce in `blog-automatico/articoli/`.
   A fine lavoro manda **email e notifica** con il riepilogo.
2. **Workflow GitHub** `.github/workflows/bozze-wordpress.yml`: quando arrivano articoli nuovi
   genera la copertina 1200×630, crea la **bozza** su WordPress (categorie, tag, estratto,
   campi SEO, immagine in evidenza) e salva nel repository il backup degli articoli del sito.
3. **WordPress** manda l'email **"Nuova bozza da approvare"** per ogni bozza.
4. **Tu** rileggi e pubblichi. Quando pubblichi, la cache di Aruba si svuota da sola.

Regole di scrittura (argomenti, tono, struttura, SEO): `blog-automatico/ISTRUZIONI-REDAZIONE.md`.

### Credenziali

- GitHub usa una password applicativa WordPress **"Blog automatico - GitHub"**, salvata come
  secret `WP_APP_PASSWORD` del repository (Settings → Secrets and variables → Actions).
  Non è scritta da nessuna parte e non si può rileggere.
- Per usare `pubblica.py` da un PC serve un file `blog-automatico/.env` (vedi `.env.example`)
  con una password applicativa dedicata a quel PC. Il file `.env` non va mai su GitHub.
- Le altre password applicative presenti in WordPress ("Blog automatico", due "Elementor MCP")
  sono state lasciate come sono, per tua scelta.

## 3. Cosa c'è in questa cartella

| Percorso | Cosa contiene |
|---|---|
| `RIEPILOGO.md` | Questo documento |
| `README.md` | Istruzioni tecniche: installazione su un nuovo PC e comandi |
| `CLAUDE.md` | Note che Claude legge a ogni sessione su questo progetto |
| `blog-automatico/pubblica.py` | Crea o aggiorna articoli su WordPress (`verifica`, `elenco`, `pubblica`, `scarica`) |
| `blog-automatico/copertina.py` | Genera la copertina se l'articolo non ne ha una |
| `blog-automatico/ISTRUZIONI-REDAZIONE.md` | Regole editoriali e SEO |
| `blog-automatico/articoli/` | Un articolo per cartella (`meta.json` + `articolo.html`): backup di tutti gli articoli |
| `.github/workflows/bozze-wordpress.yml` | Automazione GitHub che crea le bozze |
| `wordpress/ral-seo.snippet.php` | Copia dello snippet WPCode "RAL SEO" installato sul sito |

Gli articoli presenti al 5 ottobre 2026:

- Progressive Web App: cos'è e quando conviene a una PMI (1 ottobre)
- Backup 3-2-1: come proteggere i dati di studi e PMI (2 ottobre)
- Autenticazione a due fattori: guida pratica per studi e PMI (5 ottobre, primo articolo automatico)
- Windows 10 ESU: cosa cambia dal 13 ottobre 2026 per studi e PMI (5 ottobre, primo articolo automatico)

## 4. Modifiche fatte sul sito WordPress

**Snippet WPCode attivi che riguardano il blog**

- **151 "Blog – stile, intestazione e SEO articoli"** (esisteva già): stile scuro del blog,
  meta description, Open Graph e JSON-LD di articoli e pagina Blog, accesso dello script
  tramite intestazione `X-RAL-Auth` (Aruba blocca `Authorization`), email "Nuova bozza da approvare".
- **213 "RAL SEO - metadati articoli"** (nuovo): campi SEO degli articoli (`ral_seo_title`,
  `ral_seo_description`, `ral_seo_keyword`) e titolo SEO come `<title>`. Completa quello che
  il 151 non fa:
  - pagina `/blog/`: **link canonical**;
  - categorie: `twitter:title`, `twitter:description`, `twitter:image`;
  - pagine tag: titolo, canonical, meta description, Open Graph e Twitter card completi;
  - archivi autore e data: canonical.

Verifica fatta su tutte le 25 pagine pubbliche: ognuna ha **un solo** canonical, una meta
description e un set completo di Open Graph e Twitter card, senza duplicati.

**Cache Aruba HiSpeed Cache**

- Si svuota da sola quando cambiano articoli, pagine, categorie, tag, menu o commenti.
- **Non** si svuota per modifiche tecniche (snippet, tema, plugin, widget). In quei casi
  va premuto **"Cancella cache"** nella barra nera di WordPress.

## 5. Google Search Console (proprietà `https://www.roccoandrealigorio.it/`)

Fatto il 5 ottobre 2026:

- `sitemap.xml` reinviata (13 pagine) e `feed/` aggiunto come sitemap del blog.
- Rimosse le sitemap vecchie e non più esistenti: `/sitemap.rss`, `/sitemap-index.xml`.
- Indicizzazione richiesta per la home, per "Autenticazione a due fattori" e per "Windows 10 ESU".

Nota: Google segnalava la home come "pagina con reindirizzamento" perché l'ultima scansione
(17 settembre) risaliva a quando il sito era senza `www`. Oggi il sito è corretto: `www`
più canonical giusto. Il rapporto si aggiorna con la prossima scansione.

## 6. Cose ancora da fare (tue)

- [ ] Search Console → Sitemap → **/mappa-sito** → tre puntini → **Rimuovi sitemap**
      (non ho potuto farlo io). Non è urgente.
- [ ] Facoltativo: WordPress → Impostazioni → Generali → **Fuso orario** su "Roma"
      (oggi è UTC: gli articoli programmati uscirebbero 1-2 ore sfalsati).
- [ ] Ogni giorno, dopo le 13: rileggere e pubblicare le bozze arrivate.

## 7. Ripartire da un nuovo PC

1. Non serve copiare nulla a mano: tutto è su GitHub.
   `git clone https://github.com/roliadm/Rocco-Andrea-Ligorio.git`
2. Per lavorarci con Claude: apri una sessione e chiedi di collegare il repository
   `roliadm/Rocco-Andrea-Ligorio`. Le note in `CLAUDE.md` danno a Claude tutto il contesto.
3. Il blog automatico continua comunque a funzionare anche senza nessun PC.

## 8. Link utili

- Bozze da approvare: https://www.roccoandrealigorio.it/wp-admin/edit.php?post_status=draft&post_type=post
- Snippet WPCode: https://www.roccoandrealigorio.it/wp-admin/admin.php?page=wpcode
- Esecuzioni del workflow: https://github.com/roliadm/Rocco-Andrea-Ligorio/actions
- Secret di GitHub: https://github.com/roliadm/Rocco-Andrea-Ligorio/settings/secrets/actions
- Search Console: https://search.google.com/search-console?resource_id=https://www.roccoandrealigorio.it/
