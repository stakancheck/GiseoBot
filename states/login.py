from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    question6 = State()
    confirm = State()
