from telebot import types


def menu_keyboard():
    markup = types.InlineKeyboardMarkup()
    borrowings = types.InlineKeyboardButton(
        "My borrowings",
        callback_data="my_borrowings"
    )
    markup.add(borrowings)
    return markup
