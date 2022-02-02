import os
from datetime import datetime

from loader import bot
from aiogram import types
from .PyGiseo import Parse
from .base_model import *
from decouple import config
from .ImageConstructor import creation_image, plot_image

project_path = config('PATH_P')
params = ["chat_id", "login", "password", "place", "town", "type_school", "school", "theme"]


async def spaming(message: types.Message, text):
    """
    Func of spam.
    :param message: types.Message
    :param text: text to spam
    :return:
    """
    user_data = User.select()
    # with sql.connect(f'{project_path}\\data\\basic\\data.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT * FROM users")
    #     user_data = cur.fetchall()
    #     cur.close()
    for user in user_data:
        await bot.send_message(user.chat_id, text, parse_mode='html')  # chat id of all users
    await message.answer(f"Сообщение отправлено {len(user_data)} пользователям")


async def send_photo(call: types.CallbackQuery, file: str, mode=1, caption=None, reply_markup=None):
    """
    Send photo from bot to user for menu.

    :param call: call (Callback)
    :param file: file name with .png/.jpg
    :param mode: 1 - edit message, else answer (new message)
    :param caption: caption for message
    :param reply_markup: keyboard
    :return:
    """
    if file[:5] == 'parse':
        if os.path.exists(f'{project_path}\\data\\assets\\user_{call.message.chat.id}\\{file}'):
            path_image = f'{project_path}\\data\\assets\\user_{call.message.chat.id}\\{file}'
            await call.message.edit_media(types.InputMediaPhoto(types.InputFile(path_image)))
            return True
        else:
            date = datetime.now().weekday()
            if file == f'parse_schedule_{date}.png':
                await call.answer('Занятий нет')
            else:
                await call.answer('Информации нет на сайте!')
            return False

    else:
        if file == 'theme_change_variants.png':
            path_image = f'{project_path}\\data\\assets\\{file}'
        else:
            user_data = User.select().where(User.chat_id == call.message.chat.id).get()
            # with sql.connect(f'{project_path}\\data\\basic\\data.db') as conn:
            #     cur = conn.cursor()
            #     cur.execute("SELECT * FROM users WHERE chat_id=?",
            #                 (call.message.chat.id,))
            #     user_data = cur.fetchone()
            #     cur.close()
            path_image = f'{project_path}\\data\\assets\\{user_data.theme}\\{file}'  # user theme

        if mode == 1:
            await call.message.edit_media(types.InputMediaPhoto(types.InputFile(path_image)))
        else:
            await call.message.answer_photo(photo=open(path_image, 'rb'), caption=caption, reply_markup=reply_markup)


def change_theme(chat_id: int, theme: str):
    """
    Change theme by chat_id
    :param chat_id: message.chat.id
    :param theme: set theme
    :return:
    """
    data = User.select().where(User.chat_id == chat_id).get()

    # with sql.connect(f'{project_path}\\data\\basic\\data.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    #     user_data = tuple(cur.fetchone())
    #     data = user_data[:-2]
    #     cur.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
    #     conn.commit()

    data.theme = theme  # change theme
    data.save()

    # user_data = (data.chat_id, data.login, data.password, data.place,
    #              data.town, data.type_school, data.school, data.theme)
    update_images(chat_id, theme)


def update_data(chat_id: int):
    """
    Update info about user by chat_id
    :param chat_id: message.chat.id
    :return: list(chat_id, login, password, place, town, type_school, school, theme, date_update)
    """
    # with sql.connect(f'{project_path}\\data\\basic\\data.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    #     user_data = tuple(cur.fetchone())
    #     data = user_data[:-1]
    #     cur.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
    #     conn.commit()
    #     try:
    #         Parse(*data)
    #     except:
    #         user_data = 'error'
    #     cur.close()
    data = User.select().where(User.chat_id == chat_id).get()
    user_data = (data.chat_id, data.login, data.password, data.place,
                 data.town, data.type_school, data.school, data.theme)
    # print(user_data)
    # print(type(user_data))
    try:
        Parse(*user_data)
    except Exception as e:
        user_data = f'error: {e}'
    return user_data


def logout_user(chat_id: int):
    """
    Logout user (delete user from database) by chat_id
    :param chat_id: message.chat.id
    :return: none
    """
    user_data = User.get(User.chat_id == chat_id)
    user_data.delete_instance()
    user_data.save()
    #
    # with sql.connect(f'{project_path}\\data\\basic\\data.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
    #     conn.commit()
    #     cur.close()


def check_user_exists(chat_id: int):
    """
    This func check is the user exists
    :param chat_id: message.chat.id
    :return: true or false
    """
    return User.select().where(User.chat_id == chat_id)


def get_user_data(chat_id: int):
    """
    Get user data by chat_id
    :param chat_id: message.chat.id
    :return: list(chat_id, login, password, place, town, type_school, school, theme, date_update)
    """
    data = User.select().where(User.chat_id == chat_id).get()
    user_data = (data.chat_id, data.login, data.password, data.place,
                 data.town, data.type_school, data.school, data.theme)
    # with sql.connect(f'{project_path}\\data\\basic\\data.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    #     user_data = cur.fetchone()
    #     cur.close()
    return user_data


def delete_user(chat_id: int):
    """
    Delete user form db by chat_id
    :param chat_id: message.chat.id
    :return: none
    """
    user_data = User.get(User.chat_id == chat_id)
    user_data.delete_instance()
    user_data.save()

    # with sql.connect(f'{project_path}\\data\\basic\\data.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    #     user_data = tuple(cur.fetchone())
    #     cur.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
    #     cur.close()


def get_photo(chat_id: int, file_name: str, mode=1):
    """
    Open file for user by chat id and name of file

    Types of files:
    > final_marks
    > middle_marks_period_{number}
    > middle_marks_year
    > schedule

    :param file_name: name of file
    :param chat_id: message.chat.id
    :param mode: mode 1 or 2, 1 as default
    :return: file, which has be opened by "open" func
    """
    if mode == 1:
        photo = open(
            f'{project_path}\\data\\assets\\user_{chat_id}\\parse_{file_name}.png', 'rb')
    else:
        photo = open(f'{project_path}\\data\\assets\\{file_name}.png', 'rb')
    return photo


def get_homework_text(chat_id, day):
    schedule = Schedule.select().where(Schedule.chat_id == chat_id)
    text = ''
    for item in schedule:
        if len(item.homework) > 3 and item.day == day:
            text += f'<b>{item.subject}:</b>\n{item.homework}\n\n'
    return text


def get_duty_text(chat_id):
    duty = Duty.select().where(Duty.chat_id == chat_id)
    text = ''
    for item in duty:
        text += f'<b>{item.subject}:\n<i>{item.date}</i></b> - {item.task}\n'
    return text


def plot_constructor(chat_id, theme):
    final_marks = FinalMarks.select().where(FinalMarks.chat_id == chat_id)
    quarter_1 = 0
    quarter_2 = 0
    quarter_3 = 0
    quarter_4 = 0

    quarter_1_div = 0
    quarter_2_div = 0
    quarter_3_div = 0
    quarter_4_div = 0

    for item in final_marks:
        if item.quarter_1:
            quarter_1_div += 1
            quarter_1 += item.quarter_1
        if item.quarter_2:
            quarter_2_div += 1
            quarter_2 += item.quarter_2
        if item.quarter_3:
            quarter_3_div += 1
            quarter_3 += item.quarter_3
        if item.quarter_4:
            quarter_4_div += 1
            quarter_4 += item.quarter_4

    data_marks = []

    data_marks.append(quarter_1/quarter_1_div) if quarter_1_div else data_marks.append(0)
    data_marks.append(quarter_2/quarter_2_div) if quarter_2_div else data_marks.append(0)
    data_marks.append(quarter_3/quarter_3_div) if quarter_3_div else data_marks.append(0)
    data_marks.append(quarter_4/quarter_4_div) if quarter_4_div else data_marks.append(0)

    plot_image(data_marks, theme, chat_id, 'plot_marks.png')


def update_images(chat_id, theme):
    # get schedule
    schedule = Schedule.select().where(Schedule.chat_id == chat_id)
    data_schedule = {
        '0': [],
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
    }

    for item in schedule:
        # schedule
        mass = data_schedule[str(item.day)]
        mass.append([item.time, item.subject])
        data_schedule[str(item.day)] = mass

    # print(schedule)

    # get final marks
    final_marks = FinalMarks.select().where(FinalMarks.chat_id == chat_id)
    final_marks = [[item.subject, item.quarter_1, item.quarter_2,
                    item.quarter_3, item.quarter_4, item.final_mark] for item in final_marks]
    for i in range(len(final_marks)):
        for b in range(1, 4):
            if final_marks[i][b] == 0:
                final_marks[i][b] = ''
    # print(final_marks)

    # get middle marks year
    middle_marks_year = MiddleMarksYear.select().where(MiddleMarksYear.chat_id == chat_id)
    middle_marks_year = [[item.subject, item.marks] for item in middle_marks_year]
    # print(middle_marks_year)

    # get middle marks period
    middle_marks_period = MiddleMarksPeriod.select().where(MiddleMarksPeriod.chat_id == chat_id)
    middle_marks_period = [[item.subject, item.marks, item.period] for item in middle_marks_period]
    # print(middle_marks_period)

    # create images
    for key in data_schedule.keys():
        if data_schedule[key]: creation_image(data_schedule[key], ('Время', 'Урок'), theme, chat_id,
                                              f'parse_schedule_{key}.png')
    if final_marks: creation_image(final_marks, ('Предмет', ' 1 ', ' 2 ', ' 3 ', ' 4 ', 'Итог'),
                                   theme, chat_id, 'parse_final_marks.png')
    if middle_marks_year: creation_image(middle_marks_year, ('Предмет', 'Балл'), theme, chat_id,
                                         'parse_middle_marks_year.png')
    for i in range(1, 5):
        data = [[item[0], item[1]] for item in middle_marks_period if item[2] == i]
        if data: creation_image(data, ('Предмет', 'Балл'), theme, chat_id, f'parse_middle_marks_period_{i}.png')
