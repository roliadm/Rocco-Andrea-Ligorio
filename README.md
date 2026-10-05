# roccoandrealigorio.it

Repository del sito di Rocco Andrea Ligorio (WordPress su https://www.roccoandrealigorio.it)
e degli strumenti che lo alimentano.

## Contenuto

| Cartella | Cosa contiene |
|---|---|
| `blog-automatico/` | Script che pubblica gli articoli del blog su WordPress tramite API REST |
| `blog-automatico/articoli/` | Un articolo per cartella: `meta.json` + `articolo.html` (+ immagine) |

## blog-automatico: configurazione su un nuovo PC

Serve Python 3.9 o successivo. Non ci sono librerie da installare.

1. Clona il repository:
   ```
   git clone https://github.com/roliadm/Rocco-Andrea-Ligorio.git
   ```
2. In WordPress vai su **Utenti → Profilo → Password applicative**, scrivi un nome che
   identifichi il PC (es. `Blog automatico - PC ufficio`) e clicca **Aggiungi**.
   Copia la password: WordPress la mostra una volta sola.
3. In `blog-automatico/` copia `.env.example` in `.env` e incolla la password in
   `WP_APP_PASSWORD`. Il file `.env` è escluso da Git e non finisce mai su GitHub.
4. Prova la connessione:
   ```
   cd blog-automatico
   python pubblica.py verifica
   ```

## Uso

```
python pubblica.py elenco                                   # ultimi articoli sul sito
python pubblica.py pubblica articoli/mio-articolo           # crea/aggiorna come bozza
python pubblica.py pubblica articoli/mio-articolo --stato publish
python pubblica.py pubblica articoli/mio-articolo --stato future --data 2026-10-12T09:00
python pubblica.py scarica                                  # copia nel repo gli articoli del sito
```

- L'articolo è riconosciuto dallo **slug**: se esiste già sul sito viene aggiornato, non duplicato.
- Lo stato predefinito è **bozza** (`draft`): si controlla in WordPress prima di pubblicare.
- Categorie e tag si indicano per nome; i tag mancanti vengono creati.
- L'immagine in evidenza viene caricata solo la prima volta (`--nuova-immagine` per sostituirla).

Formato di un articolo: vedi `blog-automatico/articoli/_esempio/`.

## Se perdi un PC

In WordPress → Profilo → Password applicative revoca la password di quel PC.
Tutto il resto è su GitHub: basta clonare il repository e creare una nuova password.
