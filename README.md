# YouTube Video Localizer

Questo progetto consente di localizzare automaticamente il titolo e la descrizione di un video di YouTube in tutte le lingue supportate, utilizzando le API di YouTube e Google Translate. Il tool verifica l'esistenza di un video dato il suo ID, traduce titolo e descrizione, e aggiunge le localizzazioni nelle lingue specificate.

## Funzionalità

- Verifica l'esistenza di un video su YouTube tramite il suo ID.
- Traduce il titolo e la descrizione del video in tutte le lingue supportate da YouTube.
- Aggiunge localizzazioni per titolo e descrizione in base alle lingue selezionate.
- Verifica le localizzazioni aggiunte per ogni lingua.

## RICORDATI CHE:

- Devi avere una **lingua di default impostata per il video**, altrimenti non funzionerà.
- Devi accedere e dare autorizzazione con **l'account del canale YouTube**.
- L'**ID del video** deve essere passato via terminale.
- Se non funziona, prova a **cambiare la lingua di default del video** nelle impostazioni del video e riprova.

## Prerequisiti

Prima di utilizzare il progetto, è necessario configurare l'ambiente con i seguenti requisiti:

1. **Python 3.6+**
2. **Librerie Python**:
   - `google-auth-oauthlib`
   - `google-api-python-client`
   - `googletrans==4.0.0rc1`

   Puoi installare le dipendenze con il comando:

   ```bash
   pip install -r requirements.txt

## ESEMPIO DI OUTPUT SUL TERMINALE:
Video trovato: "Never Gonna Give You Up"
Il video esiste e puoi procedere.
Traduzione completata per la lingua it.
Localizzazione aggiunta per la lingua it.
Traduzione completata per la lingua fr.
Localizzazione aggiunta per la lingua fr.
...
Localizzazione del video in 5 lingue su 5 contenute nel file.