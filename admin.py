from telebot import types

ADMIN_USERNAME = "Nothing_035"


def open_admin_panel(bot, message):
    if message.from_user.username != ADMIN_USERNAME:
        bot.send_message(
            message.chat.id,
            "⛔ Sizda admin huquqi mavjud emas."
        )
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("➕ Anime qo'shish")
    markup.row("🎞 Qism qo'shish")
    markup.row("✏️ Anime tahrirlash", "🗑 Anime o'chirish")
    markup.row("📢 Anime e'lon qilish")
    markup.row("📊 Statistika")
    markup.row("🏠 Chiqish")

    bot.send_message(
        message.chat.id,
        "🛠 Admin panel",
        reply_markup=markup
    )
