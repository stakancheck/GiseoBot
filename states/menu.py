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
