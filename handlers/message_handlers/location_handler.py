from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler


class LocationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        location_handler = (MessageHandler(filters.LOCATION, cls.callback))
        app.add_handler(location_handler)

    @classmethod
    async def callback(cls: Update, context: ContextTypes.DEFAULT_TYPE):
        lat = cls.message.location.latitude
        lon = cls.message.location.longitude

        await cls.message.reply_text(f'lat = {lat}, lon = {lon}')

