import random

from aiogram import Bot, Dispatcher, F, types
import asyncio
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from gtts import gTTS # pip install gTTS для озвучивания текста
import os

from googletrans import Translator # pip install googletrans для перевода

from config import TOKEN, weather_api

bot = Bot(token=TOKEN) # https://t.me/aio_bot_my_bot
dp = Dispatcher()

translator = Translator()

@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь мне фото, и я сохраню его."
                         " Или отправь текст, и я переведу его на английский язык.")

@dp.message(F.photo)
async def photo_answer(message: Message):
    await message.answer("я сохраню это фото")
    await bot.download(message.photo[-1], f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(Command("translate"))
async def send_translate_prompt(message: Message):
    await message.reply("Отправь текст, и я переведу его на английский язык")

@dp.message(F.text)
async def translate_text(message: Message):
    # Переводим текст на английский
    translated = translator.translate(message.text, dest='en').text
    # Отправляем переведенный текст обратно пользователю
    await message.reply(translated)
    tts = gTTS(text=translated, lang="en")
    tts.save("translating.ogg")
    audio = FSInputFile('translating.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove('translating.ogg')


async def main():
    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())