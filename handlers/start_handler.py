from loader import dp
from states import Menu
from tools import *
from .keyboards import start_keyboard
from .login_handler import start_login
from decouple import config

admin = config('ADMIN_ID')


# хендлер ловит команду "старт"
@dp.message_handler(state='*', commands='start')
async def start(message: types.Message):

    if message.chat.id == int(admin):
        # Если есть запись о пользователе отправляем на главную
        if check_user_exists(message.chat.id):
            await message.answer(f'С возвращением, <b>{message.chat.username}</b>!', parse_mode='html',
                                 reply_markup=start_keyboard)
            await Menu.main_menu.set()

        # Если записи нет, то запускаем регистрацию пользователя
        else:
            path_image = f'{project_path}/data/assets/theme_1/start_page.png'
            await message.answer_photo(types.InputFile(path_image),
                                       caption=f'Привет, {message.chat.username}!\n'
                                               f'Я <b>Giseo бот</b>, помогу Вам следить за <u>успеваемостью</u> '
                                               f'в школе и <u>расписанием</u> занятий, чтобы начать работать '
                                               f'необходимо зарегистрироваться.', parse_mode='html')

            await start_login(message)
    else:
        await message.answer('Во время проведения защиты проекта работа бота для обычных пользователей приостановлена! Благодарим за понимание...')
