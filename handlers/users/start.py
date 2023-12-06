from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.default_buttons import main_menu_buttons

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}! Buyruqni tanlang",
                         reply_markup=main_menu_buttons())


