from dotenv import load_dotenv
import openai 
import os
from aiogram import Bot, Dispatcher, types, executor
import sys

load_dotenv()
openai.api_key  = os.getenv("OPENAI_API_KEY")
Telegram_bot_token = os.getenv("Telegram_BOT_TOKEN")


class Reference:

    def __init__(self) -> None:
        self.response = ""




reference = Reference()
model_name  = "gpt-3.5-turbo"


#initializing bot and dispatcher
bot = Bot(token=Telegram_bot_token)
dispatcher = Dispatcher(bot)


def clear_past():
    """
    This function clears the past conversation and context."
    """
    reference.response = " "

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    This handler clear the past conversation and context.
    """
    clear_past()
    await message.reply("I have cleared the past conversation and context.")

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with '/start' command
    """
    await message.reply("Hi.. I am a Telebot!\n Created by SaiDeepak")


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    This handler receives messages with '/help' command
    """
    help_command = """
    Hi There, I'm ChatGPT Telegram Bot! Created by SaiDeepak.Follow these commands -
    /start - To start the bot
    /help - To get help
    /clear - To clear the past conversation and context.
    I hope you Enjoy
    """
    await message.reply(help_command)



@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    This handler receives messages from the user and sends it to the OpenAI API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "assistant", "content": reference.response}, #role assistant
            {"role": "user", "content": message.text}
        ]
    )

    reference.response = response['choices'][0]['message']['content']
    print(f">>> ChatGPT: \n{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)

 

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)