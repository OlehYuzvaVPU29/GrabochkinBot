from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler
from models.user import User

STATE_FIRST_NAME, STATE_LAST_NAME, STATE_PHONE_NUMBER, STATE_EMAIL = range(4)


class UserRegisterConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('user_register', cls.user_register)],
            states={
                STATE_FIRST_NAME: [MessageHandler(filters.TEXT, cls.first_name)],
                STATE_LAST_NAME: [MessageHandler(filters.TEXT, cls.last_name)],
                STATE_PHONE_NUMBER: [
                    MessageHandler(filters.CONTACT, cls.phone_number),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, cls.phone_number)
                ],
                STATE_EMAIL: [MessageHandler(filters.TEXT, cls.email)]
            },
            fallbacks=[CommandHandler('exit_user_register', cls.exit_user_register)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def user_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"Хаю хай {update.effective_user.first_name}. Впиши своє ім'я:")

        return STATE_FIRST_NAME

    @staticmethod
    async def exit_user_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Ви вийшли з розмови.')

        return ConversationHandler.END

    @staticmethod
    async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

        first_name = update.message.text
        context.user_data['first_name'] = first_name

        await update.message.reply_text(f'Дякую. Впиши своє прізвище:')

        return STATE_LAST_NAME

    @staticmethod
    async def last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

        last_name = update.message.text
        context.user_data['last_name'] = last_name

        contact_button = KeyboardButton(text="Поділитись своїм контактом", request_contact=True)
        keyboard = [
            [contact_button],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)

        await update.message.reply_text(f'Ще раз Дякую. Впиши свій номер телефона або поділись контактом:',
                                        reply_markup=reply_markup)

        return STATE_PHONE_NUMBER

    @staticmethod
    async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.contact:
            phone_number = update.message.contact.phone_number
        else:
            phone_number = update.message.text

        context.user_data['phone_number'] = phone_number

        await update.message.reply_text(f'Велике дякую! Надішліть вашу пошту:')

        return STATE_EMAIL

    @classmethod
    async def email(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):

        email = update.message.text
        context.user_data['email'] = email

        first_name = context.user_data['first_name']
        last_name = context.user_data['last_name']
        phone_number = context.user_data['phone_number']
        email = context.user_data['email']

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email
        )
        cls.session.add(new_user)
        cls.session.commit()

        await update.message.reply_text(
            f"Ви зарегестровані!\n"
            f"Вас звати: {context.user_data['first_name']}\n"
            f"Ваше прізвище: {context.user_data['last_name']}\n"
            f"Ваш номер: {context.user_data['phone_number']}\n"
            f"Ваш емейл: {context.user_data['email']}"
        )

        return ConversationHandler.END
