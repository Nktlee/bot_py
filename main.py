import requests
import json
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BOT_TOKEN = ''

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

button = KeyboardButton(text='Rates')
keyboard = ReplyKeyboardMarkup(keyboard=[[button]])

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
            text='Привет!\nЯ бот, который помогает отслеживать курсы валют',
            reply_markup=keyboard
        )
    
def get_exchange_rates(EXCHANGE_API_URL):
    response = requests.get(EXCHANGE_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def conversion(rates, rate):
    rate = rates['rates'].get(rate, 'Нет данных')
    return rate

@dp.message(F.text == 'Rates')
async def process_dog_answer(message: Message):
    rates_USD = get_exchange_rates('https://api.exchangerate-api.com/v4/latest/USD')
    rates_RUB = get_exchange_rates('https://api.exchangerate-api.com/v4/latest/RUB')

    if rates_RUB and rates_USD:
        RUB = conversion(rates_USD, 'RUB')
        KRW = conversion(rates_RUB, 'KRW')

        await message.answer(
            text=f'USD: {RUB}\nKRW: {KRW}',
        )
    else:
        await message.answer(
            text='Не удалось получить данные о курсах валют. Попробуйте позже.',
        )

if __name__ == '__main__':
    dp.run_polling(bot)
