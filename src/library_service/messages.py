import datetime


def get_message_borrowing_created(borrowing, validated_data):
    return (
        f"✅ New borrowing created!\n"
        f"👤 User: {borrowing.context['request'].user}\n"
        f"📚 Book: {validated_data.get('book')}\n"
        f"⏳ Waiting for payment\n"
        f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )


def get_message_book_returned(borrowing):
    return (
        f"✅ Book successfully returned!\n"
        f"👤 User: {borrowing.user}\n"
        f"📚 Book: {borrowing.book}\n"
        f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

def get_message_payment_successful(payment):
    return (
        f"✅ Payment successful!\n"
        f"👤 User: {payment.borrowing.user}\n"
        f"📚 Book: {payment.borrowing.book}\n"
        f"💸 Amount: {payment.amount_of_money // 100} USD\n"
        f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

def get_message_overdue_borrowings(borrowing):
    return (
        f"📚 Overdue Borrowing Alert!\n\n"
        f"👤 User: {borrowing.user}\n"
        f"🔹 Book: {borrowing.book}\n"
        f"📅 Borrowed on: {borrowing.borrow_date.strftime('%B %d, %Y')}\n"
        f"📅 Expected return: {borrowing.expected_return_date.strftime('%B %d, %Y')}"
    )

def get_email_overdue_message(borrowing, days_expired, fine, frontend_url):
    return (
        f"Hello, {borrowing.user.first_name}!\n\n"
        f"We noticed that the book \"{borrowing.book.title}\" you borrowed on "
        f"{borrowing.borrow_date.strftime('%B %d, %Y')} was due for return on "
        f"{borrowing.expected_return_date.strftime('%B %d, %Y')}.\n\n"
        f"As of today, it is overdue by {days_expired} day(s). Please return the book as soon as possible to avoid further penalties.\n\n"
        f"A fine of ${fine / 100:.2f} has been applied to your account.\n\n"
        f"Use provided link to pay it:"
        f"{frontend_url}/api/borrowings/{borrowing.id}/return/"
        "If you have any questions, feel free to reach out.\n\n"
        "Thank you for your cooperation!\n\n"
        "Best regards,\n"
        "Your Library Team 📚"
    )

def get_borrowing_info_message(borrowing, actual_return_date):
    return (
        f"🔹*{borrowing.book.title}*\n"
        f"📅 Borrowed on: {borrowing.borrow_date.strftime('%B %d, %Y')}\n"
        f"📅 Expected return: {borrowing.expected_return_date.strftime('%B %d, %Y')}\n"
        f"🔙 Actual Return: {actual_return_date}\n\n"
    )
