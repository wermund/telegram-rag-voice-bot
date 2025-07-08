🤖 Telegram Voice RAG Bot

A voice-enabled Telegram bot that:

Accepts voice messages

Transcribes them with local Whisper

Queries Together AI (Mixtral) with a .txt knowledge base (RAG-style)

Replies with both text and voice using ElevenLabs

Replies with text only for text input

🧠 Features

✅ Voice → Whisper → GPT → ElevenLabs✅ .txt RAG support✅ Telegram integration (Python)✅ Simple .env setup✅ Fully local Whisper (no OpenAI needed!)

🗂 Project structure

📁 telegram-rag-bot
├── telegram_rag_bot.py          # main bot logic
├── knowledge.txt                # custom knowledge base for GPT
├── .env                         # contains API keys (not uploaded)
├── README.md
└── Telegram_RAG_Bot_User_Guide.pdf

💬 How it works

🔊 Voice message:

User sends a voice message

Bot transcribes with Whisper

Sends to Together API (Mixtral)

Replies with text + ElevenLabs voice message

💬 Text message:

User sends a text question

Bot replies with GPT answer in text only

📌 How to interact with the bot

Simply start a chat with the bot and:

Option 1: Send a voice message🗣️ Example: (voice) "How long does the approval take?"

✅ Bot transcribes the question

✅ Responds with text and voice

Option 2: Send a text message⌨️ Example: "What documents do I need to apply for a loan?"

✅ Bot replies with a quick text answer

🧪 Suggested example questions:

"How can I check my past transactions?"

"What documents are required for verification?"

"Where do I upload my ID?"

"How fast is the loan approval process?"

"What happens if I miss a payment?"

All answers are based only on the knowledge.txt file (RAG).

🧩 Built with

Python 3.9+

Whisper (local)

Together API (Mixtral)

ElevenLabs TTS

Telegram Bot API

dotenv, requests, pydub, SpeechRecognition

🧠 Use case ideas

Customer support bots (internal docs)

Medical triage bots (HIPAA-safe knowledgebase)

Loan onboarding bots

Multilingual smart assistants

🙌 Author

Made by Viktor Kononenko — AI integrator for real-world automation

