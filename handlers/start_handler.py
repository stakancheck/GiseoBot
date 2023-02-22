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

from loader import dp
from states import Menu
from tools import *
from .keyboards import start_keyboard
from .login_handler import start_login


# хендлер ловит команду "старт"
@dp.message_handler(state='*', commands='start')
async def start(message: types.Message):

    # Если есть запись о пользователе отправляем на главную
    if check_user_exists(message.chat.id):
        await message.answer(f'С возвращением, <b>{message.chat.username}</b>!', parse_mode='html',
                             reply_markup=start_keyboard)
        await Menu.main_menu.set()

    # Если записи нет, то запускаем регистрацию пользователя
    else:
        path_image = f'{project_path}\\data\\assets\\theme_1\\start_page.png'
        await message.answer_photo(types.InputFile(path_image),
                                   caption=f'Привет, {message.chat.username}!\n'
                                           f'Я <b>Giseo бот</b>, помогу Вам следить за <u>успеваемостью</u> '
                                           f'в школе и <u>расписанием</u> занятий, чтобы начать работать '
                                           f'необходимо зарегистрироваться.', parse_mode='html')

        await start_login(message)
