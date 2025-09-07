from flask import Flask, request
import telebot

# вставь свой токен сюда
TOKEN = "8363642763:AAH05iIxIAsbpGLhtOLIyV9id0C73Zfyelg"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Корневая страница для проверки
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

# Обработка вебхука
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Пример обработки команды /start
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.reply_to(message, "Привет! Бот запущен и работает через вебхук 🚀")

if name == "__main__":
    # Render автоматически подставляет PORT
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)