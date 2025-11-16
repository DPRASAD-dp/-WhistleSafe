import os
import asyncio
from lingodotdev.engine import LingoDotDevEngine

API_KEY = "YOUR API KEY HERE"

async def translate_text(text, target_lang="en"):
    if not text or text.strip() == "":
        return text

    result = await LingoDotDevEngine.quick_translate(
        text,
        api_key=API_KEY,
        source_locale="auto",
        target_locale=target_lang
    )
    return result


def translate(text, target_lang="en"):
    """Sync wrapper for streamlit usage"""
    return asyncio.run(translate_text(text, target_lang))


LANGUAGES = {
    "English": "en",
    "हिन्दी": "hi",
    "తెలుగు": "te",
    "தமிழ்": "ta",
    "Español": "es",
    "Français": "fr"
}
