import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Берём токен из Render переменных
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def index():
    return "Dosha bot is running!"

# Обработка сообщений в Telegram
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! 👋 Я калькулятор ДОШ по аюрведе. Напиши /test чтобы начать.")

@bot.message_handler(commands=['test'])
def start_test(message):
    bot.reply_to(message, "📝 Здесь скоро будет тест из 24 вопросов для определения ДОШи.")

# Flask endpoint для вебхуков
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.stream.read().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

if name == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)