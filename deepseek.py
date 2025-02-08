import os
import re
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties


load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

TGBOT_TOKEN = os.getenv("TGBOT_TOKEN")
bot = Bot(token=TGBOT_TOKEN, default=DefaultBotProperties(parse_mode="MarkdownV2"))
dp = Dispatcher()


# Функция для экранирования символов MarkdownV2
def escape_markdown_v2(text: str) -> str:
    special_chars = r"[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(special_chars)}])", r"\\\1", text)


@dp.message(Command("ai"))
async def handle_ai_request(message: Message):
    """Обрабатывает команду /ai и отправляет запрос в DeepSeek."""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Представь что ты агрессивный пользователь двач или форчан. Очень злобный, негативно отвечаешь на сообщения и вопросы. Посылаешь на три буквы. Ответь на следующий вопрос"},
            {"role": "user", "content": message.text},
        ],
        stream=False
    )
    
    reply_text = escape_markdown_v2(response.choices[0].message.content)
    await message.answer(reply_text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
