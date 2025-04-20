import logging
import httpx
import time
import json

# Enable only important logs
logging.basicConfig(level=logging.INFO)

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Max characters to keep prompt under safe limit
MAX_CHAR_LIMIT = 12000  


def trim_prompt(prompt: str, max_length: int = MAX_CHAR_LIMIT) -> str:
    """Trim prompt to fit within token/char limit."""
    if len(prompt) > max_length:
        return prompt[-max_length:]  # Keep latest part
    return prompt


def query_groq(prompt: str, lang: str = "en", max_retries: int = 3, retry_delay: float = 2.0) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    # Trim the prompt first
    prompt = trim_prompt(prompt)

    messages = build_messages(prompt, lang)

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.7,
    }

    for attempt in range(max_retries):
        try:
            response = httpx.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]
            return reply.strip()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logging.warning(f"[429] Rate limit hit. Retrying in {retry_delay} sec (Attempt {attempt+1}/{max_retries})...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            elif e.response.status_code == 413:
                logging.error("[413] Payload too large. Try reducing prompt size.")
                break
            else:
                logging.exception("Groq API HTTP error:")
                break
        except Exception:
            logging.exception("Groq API Error:")
            break

    return "Bhai, thoda ruk ja. Abhi zyada requests ya bada prompt bhej diya lagta hai. Retry kar thodi der baad."


def build_messages(prompt: str, lang: str):
    """Return messages list based on language detection (Hindi/English)."""
    is_hindi = (
        lang.startswith("hi") or
        any(word in prompt.lower() for word in ["bata", "bhai", "hai kya", "mujhe", "kaise", "kyu", "scene", "chal", "kya", "suna"])
    )
    if is_hindi:
        return [
            {"role": "system", "content": "Tu ek bindass aur chilled out dost hai. Har sawal ka jawab friendly Hindi ya Hinglish mein de."},
            {"role": "user", "content": "Kaise ho?"},
            {"role": "assistant", "content": "Mast bhai! Tu suna, kya chal raha hai life mein?"},
            {"role": "user", "content": prompt}
        ]
    else:
        return [
            {"role": "system", "content": f"You are a helpful assistant. Reply in {lang}."},
            {"role": "user", "content": prompt}
        ]
