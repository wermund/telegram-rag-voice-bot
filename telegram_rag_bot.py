import os
import tempfile
import requests
import whisper
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TOGETHER_KEY = os.getenv("TOGETHER_API_KEY")
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")

# Load Whisper model
model = whisper.load_model("base")

# Load RAG knowledge
with open("knowledge.txt", "r", encoding="utf-8") as f:
    context = f.read()

def transcribe(file_path):
    result = model.transcribe(file_path)
    return result["text"]

def query_gpt(user_input):
    prompt = f"""You are an assistant that only knows the following information:

{context}

Based on this knowledge, answer the following question:

{user_input}"""
    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("GPT Error:", response.status_code, response.text)
        return "Sorry, I couldn't get a response."

def tts_elevenlabs(text):
    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream",
        headers={"xi-api-key": ELEVEN_KEY},
        json={"text": text}
    )
    if response.status_code == 200:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp.write(response.content)
        temp.flush()
        return temp.name
    else:
        print("TTS Error:", response.status_code, response.text)
        return None

def handle_voice(update: Update, context: CallbackContext):
    file = update.message.voice.get_file()
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".ogg").name
    file.download(temp_path)

    # Convert ogg to wav
    wav_path = temp_path.replace(".ogg", ".wav")
    AudioSegment.from_file(temp_path).export(wav_path, format="wav")

    text = transcribe(wav_path)
    update.message.reply_text(f"You said: {text}")

    answer = query_gpt(text)
    update.message.reply_text(answer)

    voice_path = tts_elevenlabs(answer)
    if voice_path:
        with open(voice_path, "rb") as audio:
            update.message.reply_voice(audio)

def handle_text(update: Update, context: CallbackContext):
    user_input = update.message.text
    answer = query_gpt(user_input)
    update.message.reply_text(answer)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()