from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# ВСТАВЬ сюда свой токен
TOKEN = "8363642763:AAH05iIxIAsbpGLhtOLIyV9id0C73Zfyelg"

app = Flask(__name__)

# Команда /start
def start(update: Update, context: CallbackContext):
    keyboard = [[ "Старт" ]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Бот онлайн и готов работать ✅", reply_markup=reply_markup)

# Эхо-ответ
def echo(update: Update, context: CallbackContext):
    update.message.reply_text(f"Эхо: {update.message.text}")

# Основной запуск бота
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

# Flask для Render
@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    main()