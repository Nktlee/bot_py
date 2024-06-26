from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tg_bot: TgBot

env: Env = Env()

# Добавляем в переменные окружения данные, прочитанные из файла .env 
env.read_env()

# Создаем экземпляр класса Config и наполняем его данными из переменных окружения
config = Config(
    tg_bot=TgBot(
        token=env('BOT_TOKEN')
    )
)
