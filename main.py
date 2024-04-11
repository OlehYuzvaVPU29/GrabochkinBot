import logging
import inspect

from telegram.ext import ApplicationBuilder

from config.config import TELEGRAM_TOKEN_BOT
import handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN_BOT).build()

    for name, obj in inspect.getmembers(handlers):
        if inspect.isclass(obj) and issubclass(obj, handlers.BaseHandler):
            obj.register(app)

    app.run_polling()
