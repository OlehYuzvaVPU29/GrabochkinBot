import logging
import inspect

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram.ext import ApplicationBuilder

from config.config import TELEGRAM_TOKEN_BOT, DATABASE_URL
import handlers
from models.base import Base
from models.user import User

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    engine = create_engine(DATABASE_URL, echo=True)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN_BOT).build()

    for name, obj in inspect.getmembers(handlers):
        if inspect.isclass(obj) and issubclass(obj, handlers.BaseHandler):
            obj.register(app, )
            obj.set_session(session)

    app.run_polling()
