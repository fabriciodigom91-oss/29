"""
Narración para los videos.

- Si existe la variable de entorno GEMINI_API_KEY, usa Gemini TTS (voz más natural).
- Si no, usa las voces gratuitas de Microsoft Edge (edge-tts).

Variables opcionales:
  GEMINI_TTS_MODEL  modelo de Gemini TTS (por defecto gemini-2.5-flash-preview-tts)
  GEMINI_TTS_VOICE  voz de Gemini (por defecto Kore)
"""

import asyncio
import base64
import json
import os
import ssl
import time
import urllib.request
import wave

CA = "/root/.ccr/ca-bundle.crt"
SSL_CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")
GEMINI_VOICE = os.environ.get("GEMINI_TTS_VOICE", "Kore")
ESTILO = ("Lee en español latinoamericano, con tono cálido, cercano y natural, "
          "como una maestra paciente que explica algo interesante a un amigo: ")

EDGE_VOICE = "es-MX-DaliaNeural"


def _gemini(texto, salida_wav):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    cuerpo = {
        "contents": [{"parts": [{"text": ESTILO + texto}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": GEMINI_VOICE}}},
        },
    }
    req = urllib.request.Request(url, data=json.dumps(cuerpo).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": GEMINI_KEY})
    for intento in range(5):
        try:
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=180) as r:
                datos = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and intento < 4:
                time.sleep(2 ** (intento + 2))   # límite de uso: esperar y reintentar
                continue
            raise RuntimeError(f"Gemini TTS respondió {e.code}: {e.read().decode()[:300]}") from e
    pcm = base64.b64decode(datos["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    with wave.open(salida_wav, "wb") as w:   # Gemini devuelve PCM 16 bits, mono, 24 kHz
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(pcm)


def _edge(texto, salida_mp3):
    import edge_tts
    import edge_tts.communicate as ec
    ec._SSL_CTX = SSL_CTX
    asyncio.run(edge_tts.Communicate(texto, EDGE_VOICE).save(salida_mp3))


def extension():
    return "wav" if GEMINI_KEY else "mp3"


def narrar(texto, ruta_sin_ext):
    """Genera el audio (si no existe) y devuelve (ruta, duración en segundos)."""
    ruta = f"{ruta_sin_ext}.{extension()}"
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        (_gemini if GEMINI_KEY else _edge)(texto, ruta)
    if ruta.endswith(".wav"):
        with wave.open(ruta) as w:
            return ruta, w.getnframes() / w.getframerate()
    from mutagen.mp3 import MP3
    return ruta, MP3(ruta).info.length


def motor():
    return f"Gemini TTS ({GEMINI_MODEL}, voz {GEMINI_VOICE})" if GEMINI_KEY else f"edge-tts ({EDGE_VOICE})"
