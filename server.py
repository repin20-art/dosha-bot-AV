import os
import logging
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Flask для Render
app = Flask(__name__)

# Токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден! Установите его в Render → Environment.")

# Анкета (пример 24 вопросов)
QUESTIONS = [
    "Вопрос 1: Чувствуете ли вы себя энергичным утром?",
    "Вопрос 2: Быстро ли вы устаете в течение дня?",
    "Вопрос 3: У вас часто холодные руки или ноги?",
    "Вопрос 4: Вам трудно переносить жару?",
    "Вопрос 5: Есть ли у вас склонность к сухости кожи?",
    "Вопрос 6: Часто ли вы чувствуете голод?",
    "Вопрос 7: Склонны ли вы к вспыльчивости?",
    "Вопрос 8: Есть ли у вас проблемы с засыпанием?",
    "Вопрос 9: Легко ли вам сохранять концентрацию?",
    "Вопрос 10: Быстро ли вы теряете вес?",
    "Вопрос 11: Легко ли вы набираете вес?",
    "Вопрос 12: Есть ли у вас склонность к отёкам?",
    "Вопрос 13: Вам комфортнее в прохладе, чем в жаре?",
    "Вопрос 14: У вас хороший аппетит?",
    "Вопрос 15: Склонны ли вы к тревожности?",
    "Вопрос 16: Часто ли у вас бывают головные боли?",
    "Вопрос 17: У вас крепкий сон?",
    "Вопрос 18: У вас хорошая память?",
    "Вопрос 19: Вы любите физическую активность?",
    "Вопрос 20: Есть ли у вас склонность к простудам?",
    "Вопрос 21: У вас хорошее пищеварение?",
    "Вопрос 22: Часто ли у вас меняется настроение?",
    "Вопрос 23: Вам трудно переносить холод?",
    "Вопрос 24: Вы считаете себя уравновешенным человеком?"
]

# Состояние пользователей
user_states = {}

# Команда /start
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_states[chat_id] = 0  # начинаем с первого вопроса

    keyboard = [["Старт"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Бот онлайн и готов работать ✅\n\nНажмите 'Старт', чтобы пройти анкету.",
        reply_markup=reply_markup
    )

# Обработка кнопки "Старт" и вопросов
async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text.strip().lower()

    if text == "старт":
        user_states[chat_id] = 0
        await update.message.reply_text(QUESTIONS[0])
    else:
        if chat_id not in user_states:
            await update.message.reply_text("Нажмите 'Старт', чтобы начать.")
            return

        idx = user_states[chat_id]
        if idx < len(QUESTIONS) - 1:
            user_states[chat_id] += 1
            await update.message.reply_text(QUESTIONS[idx + 1])
        else:
            await update.message.reply_text("✅ Спасибо! Вы прошли все 24 вопроса.")
            del user_states[chat_id]

# Flask endpoint для Telegram webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Создание приложения Telegram
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)