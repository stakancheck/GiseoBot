from aiogram import types
from loader import dp, bot
from tools import spaming
from decouple import config
from states import Menu
from .keyboards import admin_keyboard, logout_confirm_keyboard
from .start_handler import start
from aiogram.dispatcher.filters import IDFilter
import sys


admin_chat = config('ADMIN_ID')
project_path = config('PATH_P')


@dp.message_handler(IDFilter(chat_id=admin_chat), state='*', commands='admin')
async def admin(message: types.Message):
    await Menu.admin.set()
    await message.answer('Выберите пункт меню.', reply_markup=admin_keyboard)


@dp.callback_query_handler(state=Menu.admin)
async def admin_menu(call: types.CallbackQuery):
    if call.data == 'spam':
        await call.message.answer('Ввведите текст, напишите "отмена", если передумали.')
        await Menu.spam.set()
    if call.data == 'db':
        await bot.send_document(call.message.chat.id, types.InputFile(f"{project_path}/data/basic/data.db"))
    if call.data == 'off':
        await call.message.edit_text('Хозяин, ты уверен???', reply_markup=logout_confirm_keyboard)
        await Menu.off_confirm.set()
    if call.data == 'back':
        await call.message.delete()
        await start(call.message)


@dp.callback_query_handler(state=Menu.off_confirm)
async def off(call: types.CallbackQuery):
    if call.data == 'yes':
        await call.message.answer('ПОКА)')
        sys.exit()
    if call.data == 'no':
        await call.message.delete()
        await start(call.message)


@dp.message_handler(state=Menu.spam)
async def spam(message: types.Message):
    if message.text != 'отмена':
        await spaming(message, message.text)
    await admin(message)
