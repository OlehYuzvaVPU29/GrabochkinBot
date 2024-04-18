from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler

from handlers.base_handler import BaseHandler

GENDER, PHOTO, AGE = range(3)


class FirstConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('begin', cls.begin)],
            states={
                GENDER: [MessageHandler(filters.Regex('^(Boy|Girl)$'), cls.gender)],
                PHOTO: [MessageHandler(filters.PHOTO, cls.photo)],
                AGE: [CallbackQueryHandler(cls.age)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Boy'), KeyboardButton('Girl')],
            [KeyboardButton('/exit'), KeyboardButton('/begin')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            f'Привіт {update.effective_user.first_name}! Ти Boy чи Girl?',
            reply_markup=reply_markup)

        return GENDER

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Ви вийшли з розмови.')

        return ConversationHandler.END

    @staticmethod
    async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):

        gender = update.message.text
        context.user_data['gender'] = gender

        await update.message.reply_text(f'Ти {gender}. Поділіться своїм фото, будь ласка!')

        return PHOTO

    @staticmethod
    async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Дякуємо за ваше фото! Скільки вам років?")

        keyboard = []
        number = 1

        for i in range(50):
            row = []

            for j in range(8):
                row.append(InlineKeyboardButton(f"{number}", callback_data=f"{number}"))
                number += 1

            keyboard.append(row)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Вибери свій вік:", reply_markup=reply_markup)

        return AGE

    @staticmethod
    async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        age = query.data

        context.user_data['age'] = age
        await query.answer()

        await query.edit_message_text(text=f"Вітаю ви {context.user_data['gender']}!"
                                           f" А ще вам {context.user_data['age']} years!")

        return ConversationHandler.END
