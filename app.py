import os
import telebot
from flask import Flask, request, abort

API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise RuntimeError("Ошибка: переменная окружения API_TOKEN не установлена")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

WEBHOOK_URL_BASE = 'https://your-render-domain.onrender.com'  # <-- замените на ваш URL
WEBHOOK_URL_PATH = f"/{API_TOKEN}/"

@app.route('/')
def index():
    return "Бот запущен и готов к работе!"

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        abort(403)  # Запретить запросы с другим content-type

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я простой бот с вебхуком на Flask.")

if __name__ == '__main__':
    print("Устанавливаю вебхук...")
    bot.remove_webhook()
    success = bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    if success:
        print("Вебхук успешно установлен.")
    else:
        print("Ошибка при установке вебхука.")
    app.run(host='0.0.0.0', port=8080)
