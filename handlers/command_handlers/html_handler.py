from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class HTMLHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        html_handler = CommandHandler('html', cls.callback)
        app.add_handler(html_handler)

    @staticmethod
    async def callback(cls: Update, context: ContextTypes.DEFAULT_TYPE):
        message = (
            "Це Параграф\n"
            "<i>Hello Markiyan italic</i>\n"
            "<b>Hello Oleh bold</b>\n"
            "<u>Hello Legenda underline</u>\n"
            "<a href=\'https://vpu29.lviv.ua/\'>Сайт Вищого Професійного Училища 29 </a>"
        )
        await cls.message.reply_text(message, parse_mode=ParseMode.HTML)
