import telebot
from telebot import types
from config import TOKEN
from anime import get_anime,search_anime
from admin import open_admin_panel
bot = telebot.TeleBot(TOKEN)
ADMIN_USERNAME = "Nothing_035"
searching = set()
adding_episode = {}
ADMIN = "@Nothing_035"

@bot.message_handler(commands=['start'])
def start(message):


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("🎬 Anime qidirish")
    markup.row("🔥 Top Anime", "🆕 Yangi Anime")
    markup.row("📺 Kanal", "ℹ️ Yordam")

    bot.send_message(
        message.chat.id,
        "🎌 Animelar | Uzbek tilida\n\nKerakli bo'limni tanlang.",
        reply_markup=markup
    )
@bot.message_handler(func=lambda message: message.chat.id in searching)
def anime_search(message):

    name = message.text

    anime = search_anime(name)

    searching.remove(message.chat.id)


    if anime:
        markup = types.InlineKeyboardMarkup()

        watch = types.InlineKeyboardButton(
            "▶️ Tomosha qilish",
            callback_data=f"watch_{anime[0]}"
        )

        markup.add(watch)

        bot.send_photo(
            message.chat.id,
            anime[2],
            caption=(
                f"🎬 {anime[1]}\n\n"
                f"⭐ Reyting: {anime[5]}\n"
                f"📺 Qismlar: {anime[6]}\n"
                f"🎭 Janr: {anime[4]}"
            ),
            reply_markup=markup
        )


    else:
        bot.send_message(
            message.chat.id,
            "❌ Anime topilmadi."
        )
@bot.message_handler(func=lambda message: True, content_types=['text'])
def menu(message):


    if message.text == "🏠 Chiqish":
        start(message)
        return


    if message.text == "🎬 Anime qidirish":
        searching.add(message.chat.id)
        bot.send_message(message.chat.id, "Anime nomini yuboring.")


    elif message.text == "🔥 Top Anime":
        bot.send_message(message.chat.id, "Tez orada qo'shiladi.")


    elif message.text == "🆕 Yangi Anime":
        bot.send_message(message.chat.id, "Tez orada qo'shiladi.")


    elif message.text == "📺 Kanal":
        bot.send_message(
            message.chat.id,
            "📺 Bizning kanal:\n\nhttps://t.me/Animelar_UzN1"
        )


    elif message.text == "ℹ️ Yordam":
        bot.send_message(
            message.chat.id,
            "ℹ️ Yordam\n\n"
            "Muammo yoki taklif bo‘lsa admin bilan bog‘laning:\n\n"
            "👤 @Nothing_035"
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("watch_"))
def watch_anime(call):
    anime_id = int(call.data.split("_")[1])

    import sqlite3


    conn = sqlite3.connect("database/anime.db")
    cursor = conn.cursor()


    cursor.execute(
        "SELECT episode_number, video_id FROM episodes WHERE anime_id=? ORDER BY episode_number",
        (anime_id,)
    )


    episodes = cursor.fetchall()

    conn.close()


    if episodes:
        for ep in episodes:
            bot.send_message(
                call.message.chat.id,
                f"🎬 {ep[0]}-qism"
            )
            bot.send_video(
                call.message.chat.id,
                ep[1]
            )


    else:
        bot.send_message(
            call.message.chat.id,
            "❌ Hozircha qismlar qo‘shilmagan."
        )


@bot.message_handler(content_types=['photo'])
def get_photo_id(message):


    if message.from_user.username == ADMIN.replace("@", ""):
        file_id = message.photo[-1].file_id

        bot.send_message(
            message.chat.id,
            f"Poster file_id:\n\n{file_id}"
        )
@bot.message_handler(commands=['add_episode'])
def add_episode(message):

    print("USERNAME:", message.from_user.username)

    if message.from_user.username != ADMIN_USERNAME:
        bot.send_message(
            message.chat.id,
            "⛔ Sizda ruxsat yo‘q."
        )
        return

    adding_episode[message.chat.id] = {
        "step": "anime_id"
    }

    bot.send_message(
        message.chat.id,
        "🎬 Anime ID yuboring:"
    )


@bot.message_handler(func=lambda message: message.chat.id in adding_episode)
def episode_process(message):

    data = adding_episode[message.chat.id]


    if data["step"] == "anime_id":
        data["anime_id"] = int(message.text)
        data["step"] = "episode_number"

        bot.send_message(
            message.chat.id,
            "🎞 Qism raqamini yuboring:"
        )


    elif data["step"] == "episode_number":
        data["episode_number"] = int(message.text)
        data["step"] = "video"

        bot.send_message(
            message.chat.id,
            "📹 Endi videoni yuboring:"
        )


    elif data["step"] == "video":
        if message.content_type == "video":

            file_id = message.video.file_id

            import sqlite3

            conn = sqlite3.connect("database/anime.db")
            cursor = conn.cursor()

            cursor.execute(
    "INSERT INTO episodes (anime_id, episode_number, video_id) VALUES (?, ?, ?)",
    (
        1,
        12,
        file_id
    )
)

            conn.commit()
            conn.close()

            del adding_episode[message.chat.id]

            bot.send_message(
                message.chat.id,
                "✅ Qism saqlandi."
            )
@bot.message_handler(content_types=['video'])
def save_video(message):
    file_id = message.video.file_id

    import sqlite3

    conn = sqlite3.connect("database/anime.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO episodes (anime_id, episode_number, video_id) VALUES (?, ?, ?)",
        (
            1,
            12,
            file_id
        )
    )

    conn.commit()
    conn.close()

    bot.send_message(
        message.chat.id,
        "✅ Solo Leveling 12-qism saqlandi."
    )
@bot.message_handler(commands=['admin'])
def admin_command(message):
    open_admin_panel(bot, message)

print("Bot ishga tushdi...")
bot.infinity_polling()
	
