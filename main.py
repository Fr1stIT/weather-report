import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
import json
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from datetime import datetime as DT, timezone, timedelta, time

# from key import TOKEN


logging.basicConfig(level=logging.INFO)

PROXY_URL = "http://proxy.server:3128"

API_WEATHER = 'e9a41244a9bc9a4c3d168e3005a0b3d9'
API = '3d9de74844d28377e81415151cbe6a66'
# bot = Bot(token =  , proxy=PROXY_URL)
bot = Bot(token='6094525906:AAE2kPj_VGToVD0ZUNvk_hOZePgskRmwo3c')
dp = Dispatcher(bot=bot)


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Привет! Этот бот умеет передавать информацию о погоде! Если что-то не понятно, напишите команду /help')


@dp.message_handler(commands='help')
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Напишите нужный город чтобы узнать погоду. ПО вопросам и предложениям пишите @Fr1st')


@dp.message_handler(content_types=['text'])
async def weather(message: types.Message):
    city = message.text
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric&lang=ru')
    data = json.loads(res.text)

    if res.status_code == 200:
        tz = timezone(+timedelta(hours=3))

        sun_up = DT.fromtimestamp(data["sys"]["sunrise"], tz)
        sun_up_del = sun_up.strftime('%H:%M')
        DUN = data["sys"]["sunset"]
        sun_down = DT.fromtimestamp(data["sys"]["sunset"], tz)
        sun_down_del = sun_down.strftime('%H:%M')

        sky = data["weather"][0]["description"]
        skyread = sky.title()
        skystick = ''
        print(skyread)
        # print(res.json())
        temp = data["main"]["temp"]
        stiker = ''
        if temp >= 30:
            stiker = '♨️'
        elif temp >= 15:
            stiker = '☀️'
        elif temp >= 5:
            stiker = '⛅'
        elif temp < -10:
            stiker = '🥶'
        elif temp < 0:
            stiker = '❄️'
        else:
            stiker = '️'

        if skyread == 'Ясно':
            skystick = '☀️'

        elif skyread == 'Пасмурно':
            skystick = '🌥️'


        elif skyread == 'Переменная Облачность':
            skystick = '⛅'

        elif skyread == 'Облачно С Прояснениями':
            skystick = '🌤️'

        elif skyread == 'Облачно':
            skystick = '☁️'

        elif skyread == 'Туман':
            skystick = '🌫️'

        elif skyread == 'Дождь':
            skystick = '🌧️'

        elif skyread == 'Небольшой Дождь':
            skystick = '🌦️'

        else:
            skystick = ''
        WEATHER_TEXT = f'''

Текущая погода: В городе {city.title()} {skyread} {skystick}
Температура: {temp}°C {stiker}
Скорость ветра: {data["wind"]["speed"]} м/с
Время восхода: {sun_up_del}
Время заката: {sun_down_del}
Хорошего дня!
        
        '''

        await bot.send_message(chat_id=message.from_user.id, text=WEATHER_TEXT)

    else:
        await bot.send_message(chat_id=message.from_user.id, text=f'Ошибка! Указаны некорректные данные!')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)