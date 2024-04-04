import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

TELEGRAM_TOKEN_BOT = os.getenv('TELEGRAM_TOKEN_BOT')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Start {update.effective_user.first_name}')


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Мене робив Diduh Andrian")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.lower()

    last_name = update.effective_user.last_name
    if "привіт" or "ку" in message:
        if last_name:
            await update.message.reply_text(
                f"привіт {update.effective_user.first_name} {update.effective_user.last_name}")
        else:
            await update.message.reply_text(f"привіт {update.effective_user.first_name}")

    elif "прощавай" or "папа" in message:
        if last_name:
            await update.message.reply_text(
                f"прощавай {update.effective_user.first_name} {update.effective_user.last_name}")
        else:
            await update.message.reply_text(f"прощавай {update.effective_user.first_name}")


app = ApplicationBuilder().token(TELEGRAM_TOKEN_BOT).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("author", author))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
