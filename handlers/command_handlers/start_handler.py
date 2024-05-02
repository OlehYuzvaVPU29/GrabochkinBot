from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class StartHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        start_handler = CommandHandler('start', cls.callback)
        app.add_handler(start_handler)

    @staticmethod
    async def callback(cls: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [KeyboardButton('/hello'), KeyboardButton('/author'), KeyboardButton('/bye')],
            [KeyboardButton('/begin'), KeyboardButton('/user_register')],
            [KeyboardButton('Share location', request_location=True),
             KeyboardButton('Share contact', request_contact=True)]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await cls.message.reply_text(
            f'Привіт {cls.effective_user.first_name}',
            reply_markup=reply_markup)
