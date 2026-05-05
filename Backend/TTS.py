import pygame
import re
import os
import unicodedata
import time
import asyncio
from langdetect import detect
import edge_tts

# ==========================================
# 🌍 Language to Neural Voice Mapping
# ==========================================
EDGE_TTS_VOICES = {
    "en": "en-US-JennyNeural",
    "hi": "hi-IN-MadhurNeural",
    "ur": "ur-PK-AsadNeural",        # ✅ Added Urdu
    "mr": "mr-IN-AarohiNeural",
    "fr": "fr-FR-HenriNeural",
    "es": "es-ES-AlvaroNeural",
    "de": "de-DE-KatjaNeural",
    "zh-cn": "zh-CN-XiaoxiaoNeural",
    "ru": "ru-RU-DmitryNeural",
    "ja": "ja-JP-NanamiNeural",
    "pt": "pt-BR-AntonioNeural",
    "ar": "ar-SA-HamedNeural",
}

# ==========================================
# 🧹 Clean Text (Removes emojis & junk safely)
# ==========================================
def clean_text(text):
    normalized_text = unicodedata.normalize('NFKD', text)
    cleaned_text = ''.join(
        char for char in normalized_text
        if not unicodedata.category(char).startswith(('So', 'Cs', 'Co'))
    )
    cleaned_text = re.sub(r'[^\w\s.,!?:;\'"-]', '', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

# ==========================================
# 🌎 Detect Language Safely
# ==========================================
def detect_language(text):
    try:
        lang = detect(text)

        # Fix common detection mistakes
        if lang.startswith("zh"):
            return "zh-cn"

        return lang
    except Exception:
        return "en"

# ==========================================
# 🎤 Select Voice
# ==========================================
def get_voice_for_language(lang_code):
    return EDGE_TTS_VOICES.get(lang_code, EDGE_TTS_VOICES["en"])

# ==========================================
# 🔊 Convert Text to Audio File
# ==========================================
async def text_to_audio_file(text, lang_code=None):
    timestamp = int(time.time() * 1000)
    file_path = f"Database/TTS_{timestamp}.mp3"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if not lang_code:
        lang_code = detect_language(text)

    voice = get_voice_for_language(lang_code)

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)

    return file_path

# ==========================================
# 🧹 Cleanup Old Files
# ==========================================
def cleanup_old_tts_files():
    try:
        database_dir = "Database"
        if os.path.exists(database_dir):
            for filename in os.listdir(database_dir):
                if filename.startswith("TTS_") and filename.endswith(".mp3"):
                    file_path = os.path.join(database_dir, filename)
                    if time.time() - os.path.getctime(file_path) > 300:
                        try:
                            os.remove(file_path)
                        except:
                            pass
    except:
        pass

# ==========================================
# 🔊 Main Speech Engine
# ==========================================
def text_to_speech(text, callback_func=None):
    if callback_func is None:
        callback_func = lambda r=None: True

    audio_file = None

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        cleanup_old_tts_files()

        cleaned_text = clean_text(text)
        lang_code = detect_language(cleaned_text)

        audio_file = asyncio.run(
            text_to_audio_file(cleaned_text, lang_code=lang_code)
        )

        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if callback_func() is False:
                break
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Text-to-speech error: {e}")

    finally:
        callback_func(False)

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            try:
                pygame.mixer.music.unload()
            except:
                pass

        if audio_file and os.path.exists(audio_file):
            try:
                time.sleep(0.1)
                os.remove(audio_file)
            except:
                pass

# ==========================================
# 🦅 Speak Function
# ==========================================
def SpeakFalcon(text, callback_func=None):
    if callback_func is None:
        callback_func = lambda r=None: True

    cleaned_text = clean_text(text)

    if not cleaned_text:
        return

    # If text is too long → shorten
    if len(cleaned_text) >= 1000:
        sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)
        shortened_text = ' '.join(sentences[:2])
        text_to_speech(shortened_text, callback_func)
    else:
        text_to_speech(cleaned_text, callback_func)