from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class PythonHelloHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        pythonhello_handler = CommandHandler('pythonhello', cls.callback)
        app.add_handler(pythonhello_handler)

    @staticmethod
    async def callback(cls: Update, context: ContextTypes.DEFAULT_TYPE):
        message = (
            f"```python\nprint('Привіт {cls.effective_user.first_name} {cls.effective_user.last_name}')\n```"
        )
        await cls.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
