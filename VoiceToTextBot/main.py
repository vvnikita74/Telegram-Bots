from aiogram import Bot, Dispatcher, types, executor
import os
from pathlib import Path
from vosk import Model
from Recognition import recognition_def

TOKEN_API = "5898347482:AAEqX_E1gQAe5Fe6hPvOHsm8EVnTGts5870"
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)

model = Model('vosk_model')


def start():
    print("Success")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Hello")
    await message.delete()


@dp.message_handler(content_types=['voice'])
async def voice_trigger(message: types.Message):
    global model
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.ogg")
    await bot.download_file(file_path, destination=file_on_disk)
    recognition = await recognition_def(model, file_on_disk)
    os.remove(file_on_disk)
    await bot.send_message(chat_id=message.chat.id,text=recognition)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=start())
