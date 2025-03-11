import datetime


def get_message_borrowing_created(borrowing, validated_data):
    return (
        f"✅ New borrowing created!\n"
        f"👤 User: {borrowing.context['request'].user}\n"
        f"📚 Book: {validated_data.get('book')}\n"
        f"⏳ Waiting for payment\n"
        f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
