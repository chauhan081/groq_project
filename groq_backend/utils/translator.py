from langdetect import detect
from deep_translator import GoogleTranslator

def detect_and_translate(text):
    # Step 1: Detect language using langdetect
    detected_lang = detect(text)

    # Step 2: Translate using detected language
    translated = GoogleTranslator(source=detected_lang, target='en').translate(text)
    
    return detected_lang, translated
