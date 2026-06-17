import sqlite3
import telebot

TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
OWNER_ID = 1704806696
BOT_USERNAME = "Imanroterz_bot"

bot = telebot.TeleBot(TOKEN)

db = sqlite3.connect("data.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS messages(
internal_id TEXT,
user_id INTEGER
)
""")
db.commit()

counter = 1000

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "📩 پیام ناشناس خود را ارسال کنید.")

@bot.message_handler(func=lambda m: m.chat.id != OWNER_ID, content_types=['text'])
def receive(message):
    global counter
    counter += 1
    code = f"MSG{counter}"

    cur.execute("INSERT INTO messages VALUES (?,?)", (code, message.chat.id))
    db.commit()

    bot.send_message(
        OWNER_ID,
        f"📨 پیام ناشناس جدید\n\nکد: {code}\n\n{message.text}"
    )

    bot.reply_to(message, "✅ پیام شما ارسال شد.")

@bot.message_handler(func=lambda m: m.chat.id == OWNER_ID and m.reply_to_message)
def reply_owner(message):
    text = message.reply_to_message.text or ""
    if "کد:" not in text:
        return

    code = text.split("کد:")[1].split("\n")[0].strip()

    cur.execute("SELECT user_id FROM messages WHERE internal_id=?", (code,))
    row = cur.fetchone()

    if row:
        bot.send_message(row[0], message.text)

bot.infinity_polling(skip_pending=True)
