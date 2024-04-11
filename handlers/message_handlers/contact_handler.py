from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler


class ContactHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        contact_handler = (MessageHandler(filters.CONTACT, cls.callback))
        app.add_handler(contact_handler)

    @classmethod
    async def callback(cls: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = cls.message.contact.user_id
        first_name = cls.message.contact.first_name
        last_name = cls.message.contact.last_name
        await cls.message.reply_text(
            f"""user_id = {user_id}
            first_name = {first_name}
            last_name = {last_name}
            """)


