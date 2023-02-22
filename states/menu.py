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

from aiogram.dispatcher.filters.state import StatesGroup, State


class Menu(StatesGroup):
    main_menu = State()
    func = State()
    quarter_select = State()
    account_menu = State()
    logout_confirm = State()
    theme_change = State()
    info_menu = State()
    admin = State()
    spam = State()
    off_confirm = State()
