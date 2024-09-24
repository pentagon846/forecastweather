import os
import telebot
import data
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
api_key = os.getenv('API_KEY')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello, do you want to know the weather? \nPlease, type your location!")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()

        name = weather_data["name"]
        lon = weather_data["coord"]["lon"]
        lat = weather_data["coord"]["lat"]

        url2 = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        forecast_response = requests.get(url2)
        print(forecast_response)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            forecast_message = f"Weather forecast for {name}:\n"

            forecast_list = forecast_data["list"]
            for forecast in forecast_list:
                dt_txt = forecast["dt_txt"]
                main = forecast["main"]
                description = forecast["weather"][0]["description"]
                forecast_message += f"Date and Time: {dt_txt}\n"
                forecast_message += f"Temperature: {main['temp']}°C\n"
                forecast_message += f"Description: {description}\n"
                forecast_message += "---\n"

            bot.send_message(message.chat.id, forecast_message)

        else:
            bot.send_message(message.chat.id, f"Sorry, I can't find weather for {city}.")
    else:
        bot.send_message(message.chat.id, f"Sorry, I can't find weather for {city}.")

    bot.send_message(message.chat.id, "Please enter your location!")


if __name__ == '__main__':
    bot.polling(non_stop=True)
