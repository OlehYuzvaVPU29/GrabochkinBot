from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class HelloHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        hello_handler = CommandHandler('hello', cls.callback)
        app.add_handler(hello_handler)

    @staticmethod
    async def callback(cls: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await cls.message.reply_text(f'Привіт {cls.effective_user.first_name}!')


