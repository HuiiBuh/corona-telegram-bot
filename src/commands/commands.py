from asyncio import sleep

from aiogram import types, md
from aiogram.dispatcher import FSMContext


async def send_welcome(message: types.Message):
    response = """
    Commands: 
      - /subscriptions See your current subscriptions
      - /subscribe Subscribe to a district
    """

    await message.reply(response)


async def subscribe_to(message: types.Message, state: FSMContext):
    print(message.from_user)

    current_state = await state.get_state()

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Other")

    new_message = await message.answer("test")
    await sleep(1)
    await new_message.edit_text("Hello world")


async def subscriptions(message: types.Message):
    await message.reply(md.text(
        md.bold('Info about your language:'),
        md.text("asdf")
    ))
