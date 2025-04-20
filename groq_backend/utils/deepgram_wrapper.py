from dotenv import load_dotenv
import os

load_dotenv()  # <- This loads .env file

from deepgram import Deepgram

dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

from deepgram import Deepgram
import os

dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

async def transcribe_audio(audio_bytes: bytes):
    source = {
        'buffer': audio_bytes,
        'mimetype': 'audio/wav'  # or 'audio/mp3'
    }

    options = {
        'punctuate': True,
        'language': 'en'
    }

    response = await dg_client.transcription.prerecorded(source, options)
    return response['results']['channels'][0]['alternatives'][0]['transcript']
