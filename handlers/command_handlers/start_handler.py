from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from handlers.base_handler import BaseHandler


class StartHandler(BaseHandler):
    start_count = {}

    @classmethod
    def register(cls, app):
        start_handler = CommandHandler('start', cls.callback)
        app.add_handler(start_handler)

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_user.id
        StartHandler.start_count[user_id] = StartHandler.start_count.get(user_id, 0) + 1

        if StartHandler.start_count[user_id] >= 2:
            await update.message.reply_text(
                f'Привіт {update.effective_user.first_name}, це вже {StartHandler.start_count[user_id]}'
                f'-й раз, коли ви почали цього бота!',
                reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True)
            )
        else:
            keyboard = [
                [KeyboardButton('/hello'), KeyboardButton('/author')],
                [KeyboardButton('/bye'), KeyboardButton('/begin'), KeyboardButton('/poll_favourite_subject')],
                [KeyboardButton('Share location', request_location=True),
                 KeyboardButton('Share contact', request_contact=True)]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            first_start_message = "||Правда, це після останнього його запуску\.||"

            await update.message.reply_text(
                f"Привіт {update.effective_user.first_name},"
                f" ви почали цього бота в 1\-ий раз\!\n{first_start_message}",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN_V2
            )
