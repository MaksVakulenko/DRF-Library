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