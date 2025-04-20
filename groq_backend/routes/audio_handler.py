from fastapi import APIRouter, File, UploadFile
from utils.deepgram_wrapper import transcribe_audio
from utils.tts import text_to_audio  # Tumhara gTTS function yahan import ho
import os

router = APIRouter()

@router.post("/audio")
async def handle_audio(file: UploadFile = File(...)):
    # Step 1: Read the uploaded file content
    audio_bytes = await file.read()

    # Step 2: Transcribe the audio
    transcription = await transcribe_audio(audio_bytes)

    # Step 3: Convert transcription to audio (TTS)
    tts_audio_path = text_to_audio(transcription)

    # Optional: Return audio file path or audio as bytes if needed
    return {
        "transcription": transcription,
        "tts_audio_file": tts_audio_path
    }
