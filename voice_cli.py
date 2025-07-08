import os
import tempfile
import requests
import speech_recognition as sr
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
import whisper

load_dotenv()
tg_api = os.getenv("TOGETHER_API_KEY")
eleven = os.getenv("ELEVENLABS_API_KEY")

#Load knowledge for RAG
with open("knowledge.txt", "r", encoding="utf-8") as f:
    context = f.read()

model = whisper.load_model("base")

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        print("🛠 Recording... speak now")
        audio = r.listen(mic)
    return audio

def transcribe(audio):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_path = temp_audio.name
        with open(temp_path, "wb") as f:
            f.write(audio.get_wav_data())

    result = model.transcribe(temp_path)
    return result["text"]

def chat_gpt(user_input):
    prompt = f"""You are an assistant that only knows the following information:

{context}

Based on this knowledge, answer the following question:

{user_input}
"""

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {tg_api}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/Meta-Llama-3-8B-Instruct-Lite",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("⚠️ GPT error:", response.text)
        return ""

def synthesize_voice(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"
    headers = {"xi-api-key": eleven}
    payload = {"text": text}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp.write(response.content)
        temp.flush()
        return temp.name
    else:
        print("🛑 TTS failed:", response.status_code, response.text)
        return ""

def main():
    audio = record_audio()
    text = transcribe(audio)
    if not text:
        return
    print("📝 You said:", text)
    answer = chat_gpt(text)
    print("🤖 GPT says:", answer)
    mp3 = synthesize_voice(answer)
    sound = AudioSegment.from_file(mp3)
    play(sound)

if __name__ == "__main__":
    main()