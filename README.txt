# Dosha Bot Render Deploy

## Шаги для запуска
1. Создай новый проект на Render и выбери Python.
2. Загрузи туда эти файлы (server.py, requirements.txt, Procfile).
3. В настройках Render → Environment добавь переменную:
   BOT_TOKEN = <Твой токен от BotFather>
4. Убедись, что команда запуска:
   gunicorn server:app -w 1 -k sync -b 0.0.0.0:$PORT
5. Сделай Deploy.
6. Установи webhook (замени <ТОКЕН> и <URL>):
   https://api.telegram.org/bot<ТОКЕН>/setWebhook?url=<URL>/webhook
7. Проверь:
   https://api.telegram.org/bot<ТОКЕН>/getWebhookInf