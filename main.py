import os
import logging

from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton('/hello'), KeyboardButton('/author')],
        [KeyboardButton('/bye'), KeyboardButton('Share location', request_location=True)],
        [KeyboardButton('Share contact', request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        f'Привіт {update.effective_user.first_name}',
        reply_markup=reply_markup)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привіт {update.effective_user.first_name}!')


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Мене робив Markyian Patsai")


async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Прощавай {update.effective_user.first_name}!')


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.longitude

    await update.message.reply_text(f'lat = {lat}, lon = {lon}')


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.contact.user_id
    first_name = update.message.contact.first_name
    last_name = update.message.contact.last_name
    await update.message.reply_text(
        f"""user_id = {user_id}
        first_name = {first_name}
        last_name = {last_name}
        """)


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("author", author))
app.add_handler(CommandHandler("bye", bye))

location_handler = (MessageHandler(filters.LOCATION, location))
app.add_handler(location_handler)

contact_handler = (MessageHandler(filters.CONTACT, contact))
app.add_handler(contact_handler)

app.run_polling()
