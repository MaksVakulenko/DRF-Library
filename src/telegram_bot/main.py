import telebot
import os
from dotenv import load_dotenv

from user.models import User
from borrowing.models import Borrowing
from .markups import menu_keyboard


load_dotenv()

bot = telebot.TeleBot(os.environ.get("API_KEY"))


def get_user_from_message(message):
    args = message.text.split()

    if len(args) > 1:
        user_pk_str = args[1]
        if not user_pk_str.isdigit():
            return None, "The provided user ID is invalid."
        user = User.objects.filter(pk=int(user_pk_str)).first()
        if not user:
            return None, f"The user with ID {user_pk_str} does not exist."
        if user.chat_id != message.chat.id:
            user.chat_id = message.chat.id
            user.save(update_fields=["chat_id"])
        return user, None
    user = User.objects.filter(chat_id=message.chat.id).first()
    if not user:
        return None, "You are not registered in the system."
    return user, None


@bot.message_handler(commands=["start"])
def send_welcome(message):
    telegram_name = message.from_user.first_name
    user, error = get_user_from_message(message)
    if error:
        return bot.reply_to(message, f"Hello {telegram_name}! {error}")

    bot.reply_to(message, f"Hello {user.first_name}.", reply_markup=menu_keyboard())


@bot.callback_query_handler(func=lambda call: call.data=="my_borrowings")
def my_borrowings_list(call):
    borrowings = Borrowing.objects.filter(user__chat_id=call.from_user.id)
    if not borrowings:
        return bot.send_message(
            call.message.chat.id,
            "You have no active borrowings.",
        )
    borrowing_message = "📚 *Your Active Borrowings:*\n\n"
    for borrowing in borrowings:
        actual_return_date = borrowing.actual_return_date if borrowing.actual_return_date else "Not yet"

        borrowing_message += (
            f"🔹*{borrowing.book.title}*\n"
            f"📅 Borrowed on: {borrowing.borrow_date.strftime('%B %d, %Y')}\n"
            f"📅 Expected return: {borrowing.expected_return_date.strftime('%B %d, %Y')}\n"
            f"🔙 Actual Return: {actual_return_date}\n\n"
        )


    bot.send_message(call.message.chat.id, borrowing_message, parse_mode="Markdown")
