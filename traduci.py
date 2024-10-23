import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googletrans import Translator, LANGUAGES
import sys

# Funzione per autenticarsi e ottenere il servizio YouTube
def get_youtube_service():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # Path del file client_secrets.json
    client_secrets_file = os.path.join(os.path.dirname(__file__), "client_secrets.json")
    
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    credentials = flow.run_local_server(port=0)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    return youtube

# Funzione per controllare se un video esiste
def check_video_exists(youtube, video_id):
    try:
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()

        if len(response.get("items", [])) > 0:
            # Pulisco il terminale
            os.system('cls' if os.name == 'nt' else 'clear')
            # Stampo il titolo del video
            print(f"Video trovato: {response['items'][0]['snippet']['title']}")
            return response['items'][0]['snippet']  # Restituisci i dettagli del video
        else:
            print("Video non trovato.")
            return None

    except googleapiclient.errors.HttpError as e:
        print(f"Errore durante la richiesta API: {e}")
        return None

# Funzione per tradurre il testo
def translate_text(text, target_language="it"):
    translator = Translator()
    
    # Controlla se il codice lingua è valido
    if target_language not in LANGUAGES:
        print(f"Codice lingua non valido: {target_language}.")
        return None
    
    try:
        translated = translator.translate(text, dest=target_language)
        if translated is None or not translated.text:
            print(f"Errore durante la traduzione per la lingua {target_language}.")
            return None
        return translated.text
    except Exception as e:
        print(f"Errore durante la traduzione per la lingua {target_language}: {e}")
        return None

# Funzione per aggiungere localizzazione al titolo e alla descrizione
def add_localization(youtube, video_id, language_code, localized_title, localized_description):
    try:
        request = youtube.videos().list(part="localizations", id=video_id)
        response = request.execute()
        
        localizations = response["items"][0].get("localizations", {})
        localizations[language_code] = {
            "title": localized_title,
            "description": localized_description
        }

        request = youtube.videos().update(
            part="localizations",
            body={
                "id": video_id,
                "localizations": localizations
            }
        )
        response = request.execute()

        print(f"Localizzazione aggiunta per la lingua {language_code}.")
        return True

    except googleapiclient.errors.HttpError as e:
        print(f"Errore durante la richiesta API: {e}")
        return False

# Funzione per verificare la localizzazione aggiunta
def verify_localization(youtube, video_id, language_code):
    request = youtube.videos().list(part="localizations", id=video_id)
    response = request.execute()

    if response.get("items", []):
        localizations = response["items"][0].get("localizations", {})
        if language_code in localizations:
            localized_title = localizations[language_code]["title"]
            localized_description = localizations[language_code]["description"]
            print(f"Titolo localizzato ({language_code}): {localized_title}")
            print(f"Descrizione localizzata ({language_code}): {localized_description}")
        #else:
          #  print(f"Nessuna localizzazione trovata per la lingua {language_code}.")

# Funzione per leggere le lingue da un file di testo
def read_languages_from_file(file_path):
    try:
        with open(file_path, "r") as f:
            languages = [line.strip() for line in f if line.strip()]  # Rimuovi righe vuote
        return languages
    except FileNotFoundError:
        print(f"Errore: il file {file_path} non è stato trovato.")
        return None
    except IOError as e:
        print(f"Errore durante la lettura del file {file_path}: {e}")
        return None

# Esempio di utilizzo
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Errore: devi fornire l'ID del video come argomento.")
        sys.exit(1)
    # ( https://www.youtube.com/watch?v=VIDEO_ID ) o ( https://studio.youtube.com/video/VIDEO_ID/edit)
    video_id = sys.argv[1]  # Inserisci l'ID del video che hai caricato

    youtube = get_youtube_service()

    # Verifica se il video esiste
    video_details = check_video_exists(youtube, video_id)

    if video_details:
        print("Il video esiste e puoi procedere.")

        # Ottieni il titolo e la descrizione originali
        original_title = video_details['title']
        original_description = video_details['description']

        # Ottieni la lingua di default del video
        default_language = video_details.get('defaultLanguage', None)

        # Leggi le lingue dal file
        language_codes = read_languages_from_file(os.path.join(os.path.dirname(__file__), "youtube_languages.txt"))

        # Aggiungi localizzazione per ciascuna lingua non esistente e non di default
        counter = 0

        for language_code in language_codes:
            if language_code != default_language:
                # Traduci solo se il codice lingua è valido
                translated_title = translate_text(original_title, language_code)
                if translated_title is None:
                    continue  # Salta l'iterazione se la traduzione fallisce

                translated_description = translate_text(original_description, language_code)
                if translated_description is None:
                    continue  # Salta l'iterazione se la traduzione fallisce

                # Verifica se la lingua è già localizzata
                request = youtube.videos().list(part="localizations", id=video_id)
                response = request.execute()
                localizations = response["items"][0].get("localizations", {})
                
                if language_code not in localizations:
                    add_localization(youtube, video_id, language_code, translated_title, translated_description)
                    verify_localization(youtube, video_id, language_code)
                    counter += 1
                else:
                    print(f"La lingua {language_code} è già localizzata.")
                    counter += 1

        print("Localizzazione del video di ", counter, "rispetto a ", len(language_codes), "lingue contenute nel file.")
    else:
        print("Non puoi procedere, il video non esiste.")