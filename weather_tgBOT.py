import telebot
import config
import requests
from dotenv import load_doenv
import os

load_doenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Бот на связи) Напиши название любого города, например Москва или Лондон: ")

@bot.message_handler(content_types=['text'])
def send_weather(message):
    city = message.text

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            humidity = data['main']['humidity']

            answer = (f"Погода в городе: {city.capitalize()}\n"
                     f"Температура: {temp}°C\n"
                     f"На улицу: {desc}\n"
                     f"Влажность: {humidity}%\n")
            bot.send_message(message.chat.id, answer)
        else:
            print(response.status_code)
            bot.send_message(message.chat.id, "Проверьте правильность написания")
    except Exception as e:
        print(response.status_code)
        bot.send_message(message.chat.id, "Что-то пошло не так при запросе к серверу погоды")

if __name__ == '__main__':
    bot.polling(non_stop=True)

