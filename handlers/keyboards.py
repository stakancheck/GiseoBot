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

import datetime

from aiogram import types

confirm_keyboard = types.InlineKeyboardMarkup()
confirm_keyboard.row(types.InlineKeyboardButton('Не даю согласие', callback_data='no'),
                     types.InlineKeyboardButton('Даю согласие', callback_data='yes'))

back_keyboard = types.InlineKeyboardMarkup()
back_keyboard.row(types.InlineKeyboardButton('🔙', callback_data='back'))

start_keyboard = types.InlineKeyboardMarkup()
start_keyboard.row(types.InlineKeyboardButton('Начать!', callback_data='start'))

date = datetime.date.today().strftime('%d.%m.%Y')

main_menu_keyboard = types.InlineKeyboardMarkup()
main_menu_keyboard.row(types.InlineKeyboardButton(text="Расписание", callback_data=f'schedule: {date}'),
                       types.InlineKeyboardButton(text="Баллы за год", callback_data='year'))
main_menu_keyboard.row(types.InlineKeyboardButton(text="Баллы за четверть", callback_data='quarter'),
                       types.InlineKeyboardButton(text="Итоговые отметки", callback_data='final'))
main_menu_keyboard.row(types.InlineKeyboardButton(text="🔄 Обновить данные 🔄", callback_data='update'))
main_menu_keyboard.row(types.InlineKeyboardButton(text="❗ Информация ❗", callback_data='info'),
                       types.InlineKeyboardButton(text="🗿 Аккаунт 🗿", callback_data='account'))


quarter_select_keyboard = types.InlineKeyboardMarkup()
quarter_select_keyboard.row(types.InlineKeyboardButton('1⃣ четверть', callback_data='select_quarter_1'))
quarter_select_keyboard.row(types.InlineKeyboardButton('2⃣ четверть', callback_data='select_quarter_2'))
quarter_select_keyboard.row(types.InlineKeyboardButton('3⃣ четверть', callback_data='select_quarter_3'))
quarter_select_keyboard.row(types.InlineKeyboardButton('4⃣ четверть', callback_data='select_quarter_4'))
quarter_select_keyboard.row(types.InlineKeyboardButton('🏠', callback_data='back_selected'))

account_keyboard = types.InlineKeyboardMarkup()
account_keyboard.add(types.InlineKeyboardButton('❌  Выйти из аккаунта  ❌', callback_data='logout'))
account_keyboard.add(types.InlineKeyboardButton('✏ Сменить тему ✏', callback_data='change_theme'))
account_keyboard.add(types.InlineKeyboardButton('💎 Pro version 💎', callback_data='vip'))
account_keyboard.add(types.InlineKeyboardButton('🏠', callback_data='back'))

logout_confirm_keyboard = types.InlineKeyboardMarkup()
logout_confirm_keyboard.row(types.InlineKeyboardButton('Да', callback_data='yes'),
                            types.InlineKeyboardButton('Нет', callback_data='no'))

change_theme_keyboard = types.InlineKeyboardMarkup()
change_theme_keyboard.row(types.InlineKeyboardButton('✔', callback_data='theme_1'),
                          types.InlineKeyboardButton('✔', callback_data='theme_2'),
                          types.InlineKeyboardButton('✔', callback_data='theme_3'))
change_theme_keyboard.row(types.InlineKeyboardButton('🔙', callback_data='back'))

info_keyboard = types.InlineKeyboardMarkup()
info_keyboard.row(types.InlineKeyboardButton('💰 Поддержать 💰', callback_data='support'))
info_keyboard.row(types.InlineKeyboardButton('📁 Другие проекты 📁', callback_data='over'))
info_keyboard.row(types.InlineKeyboardButton('✉ Связь с разработчиком ✉', callback_data='connect'))
info_keyboard.add(types.InlineKeyboardButton('🏠', callback_data='back_info'))

admin_keyboard = types.InlineKeyboardMarkup()
admin_keyboard.row(types.InlineKeyboardButton('Рассылка', callback_data='spam'))
admin_keyboard.row(types.InlineKeyboardButton('База данных', callback_data='db'))
admin_keyboard.row(types.InlineKeyboardButton('Отключить бота', callback_data='off'))
admin_keyboard.add(types.InlineKeyboardButton('В стартовое меню', callback_data='back'))
