#  Copyright 2023. Artem Sukhanov
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  SPDX-License-Identifier: GPL-3.0-or-later

from states import Register, Menu
from aiogram.dispatcher import FSMContext
from loader import dp
import json
from tools import *
from .keyboards import start_keyboard, confirm_keyboard
from decouple import config
from cryptography.fernet import Fernet


cipher_key = config('CIPHER_KEY')


async def start_login(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    with open(f'{project_path}\\data\\basic\\data_registration_giseo.json', 'r') as f:
        DATA = json.load(f)
    for item in DATA.keys():
        keyboard.row(types.KeyboardButton(item))
    await message.answer('Введите городской округ/муниципальный район 🗺', reply_markup=keyboard)
    await Register.question1.set()


@dp.message_handler(state=Register.question1)
async def second(message: types.Message, state: FSMContext):
    answer = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    with open(f'{project_path}\\data\\basic\\data_registration_giseo.json', 'r') as f:
        DATA = json.load(f)
    for item in DATA[answer].keys():
        keyboard.row(types.KeyboardButton(item))
    await state.update_data({
        'id_mess': message.chat.id,
        'place': answer
    })
    await message.answer('Введите город 🏙', reply_markup=keyboard)
    await Register.question2.set()


@dp.message_handler(state=Register.question2)
async def third(message: types.Message, state: FSMContext):
    answer = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    with open(f'{project_path}\\data\\basic\\data_registration_giseo.json', 'r') as f:
        DATA = json.load(f)
    state_data = await state.get_data()
    for item in DATA[state_data['place']][answer].keys():
        keyboard.row(types.KeyboardButton(item))
    await state.update_data({
        'town': answer
    })
    await message.answer('Введите тип ОО 🏢', reply_markup=keyboard)
    await Register.question3.set()


@dp.message_handler(state=Register.question3)
async def fourth(message: types.Message, state: FSMContext):
    answer = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    with open(f'{project_path}\\data\\basic\\data_registration_giseo.json', 'r') as f:
        DATA = json.load(f)
    state_data = await state.get_data()
    for item in DATA[state_data['place']][state_data['town']][answer]:
        keyboard.row(types.KeyboardButton(item))
    await state.update_data({
        'type_school': answer
    })
    await message.answer('Введите название ОО 📋', reply_markup=keyboard)
    await Register.question4.set()


@dp.message_handler(state=Register.question4)
async def fifth(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({
        'school': answer
    })
    await message.answer('Введите логин 🤵‍', reply_markup=types.ReplyKeyboardRemove())
    await Register.question5.set()


@dp.message_handler(state=Register.question5)
async def sixth(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({
        'login': answer
    })
    await message.answer('Введите пароль 🔐')
    await Register.question6.set()


@dp.message_handler(state=Register.question6)
async def confirm(message: types.Message, state: FSMContext):
    answer = message.text.encode()
    cipher = Fernet(cipher_key)
    password = cipher.encrypt(answer).decode()
    await state.update_data({
        'password': password
    })
    path_file = f'{project_path}\\data\\basic\\Согласие на обработку персональных данных.pdf'
    await message.answer_document(types.InputFile(path_file), caption='Согласие на обработку персональных данных',
                                  reply_markup=confirm_keyboard)
    # await message.answer('Согласие на обработку персональных данных', reply_markup=confirm_keyboard)
    await Register.confirm.set()


@dp.callback_query_handler(state=Register.confirm)
async def finish(call: types.CallbackQuery, state: FSMContext):
    answer = call.data
    if answer == 'yes':
        await call.message.answer('Минутку... Связываюсь с Giseo 🌐')
        data = await state.get_data()
        # id_message, login, password, place, town, type_school, school, theme, date_update
        try:
            Parse(data['id_mess'], data['login'], data['password'], data['place'], data['town'], data['type_school'],
                  data['school'], 'theme_1')

        except:
            await call.message.answer('Невозможно подключить к giseo, попробуйте снова!')
            delete_user(call.message.chat.id)
            await state.finish()
            await start_login(call.message)

        else:
            await state.finish()
            await Menu.main_menu.set()
            await call.message.answer(f'Успешная регистрация!', parse_mode='html',
                                      reply_markup=start_keyboard)
            await Menu.main_menu.set()
    else:
        await call.message.answer('Вы не дали согласие!')
        await state.finish()
        await start_login(call.message)
