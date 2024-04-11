from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class ByeHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        bye_handler = CommandHandler('bye', cls.callback)
        app.add_handler(bye_handler)

    @staticmethod
    async def callback(cls: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await cls.message.reply_text(f'Прощавай {cls.effective_user.first_name}!')


