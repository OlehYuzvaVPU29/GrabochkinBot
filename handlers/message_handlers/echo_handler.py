from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler


class EchoHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, cls.callback))

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(update.message.text)
