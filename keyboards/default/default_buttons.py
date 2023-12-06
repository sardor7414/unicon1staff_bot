from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = ["📝Vazifa qo'shish", "📊Mening ishlarim"]
    for btn in buttons:
        markup.insert(KeyboardButton(text=btn))
    return markup

def button_send_location():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Joylashuvni yuborish", request_location=True)
    markup.add(button)
    return markup

