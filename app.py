import os
import telebot
from flask import Flask, request, abort

API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise RuntimeError("Ошибка: переменная окружения API_TOKEN не установлена")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Убираем двоеточие из токена в URL пути
clean_token = API_TOKEN.replace(':', '')
WEBHOOK_URL_BASE = 'https://render-webhuk-test.onrender.com'
WEBHOOK_URL_PATH = f"/{clean_token}/"

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
        abort(403)

from telebot import types

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Нажми меня", callback_data="button_click")
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! Я бот на вебхуках!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "button_click")
def callback_button(call):
    bot.answer_callback_query(call.id, "Ты нажал кнопку!")
    bot.send_message(call.message.chat.id, "Спасибо за нажатие!")

if __name__ == '__main__':
    print("Удаляю старый вебхук...")
    bot.remove_webhook()
    print("Устанавливаю новый вебхук...")
    success = bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    if success:
        print("Вебхук успешно установлен.")
    else:
        print("Ошибка при установке вебхука.")
    app.run(host='0.0.0.0', port=8080)