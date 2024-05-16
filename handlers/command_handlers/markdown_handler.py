from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class MarkdownHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(CommandHandler('markdown', cls.callback))

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = (
            "*bold text* \n"
            "_italic text_ \n"
            "__underline__ \n"
            "~strikethrough~ \n"
            "||spoiler|| \n"
            "*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold* \n"
            "[inline URL](http://www.example.com/) \n"
            "[inline mention of a user](tg://user?id=6570732383) \n"
            "![👍](tg://emoji?id=5368324170671202286) \n"
            "`inline fixed-width code` \n"
            "``` \n"
            "pre-formatted fixed-width code block \n"
            "``` \n"
            "```python \n"
            "# pre-formatted fixed-width code block written in the Python programming language \n"
            "print('Hello, world!') \n"
            "``` \n"
            ">Block quotation started \n"
            ">Block quotation continued \n"
            ">The last line of the block quotation \n\n"
            ">The second block quotation started right after the previous \n"
            ">The third block quotation started right after the previous"
        )
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
