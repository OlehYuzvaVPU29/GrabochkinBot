from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class AuthorHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(CommandHandler("author", cls.callback))

    @staticmethod
    async def callback(cls: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=cls.effective_chat.id, text="Мене робив Oleh Yuzva")
