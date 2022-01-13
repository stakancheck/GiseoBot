# start project
if __name__ == "__main__":
    from handlers import dp
    from aiogram import executor
    from tools.base_model import User
    User.create_table()
    executor.start_polling(dp)
