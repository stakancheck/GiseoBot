from aiogram import types
from loader import dp


# reply on incorrect command
@dp.message_handler(state='*')
async def answer(message: types.Message):
    await message.answer('Команда не работает или не распознана')
