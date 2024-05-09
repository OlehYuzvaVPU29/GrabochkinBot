from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, PollAnswerHandler

from handlers.base_handler import BaseHandler

TOTAL_VOTER_COUNT = 3


class FavouriteSubjectHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(
            CommandHandler("poll_favourite_subject", cls.command_handler_callback)
        )
        app.add_handler(
            PollAnswerHandler(cls.poll_answer_handler_callback)
        )

    @staticmethod
    async def command_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        questions = [
            "Основи програмування",
            "Алгоритми і структури даних",
            "Бази даних",
            "Операційні системи",
            "Основи тестування"]

        message = await context.bot.send_poll(
            update.effective_chat.id,
            "Який твій улюбленний спец. предмет?",
            questions,
            is_anonymous=False,
            allows_multiple_answers=True,
        )
        payload = {
            message.poll.id: {
                "questions": questions,
                "message_id": message.message_id,
                "chat_id": update.effective_chat.id,
                "answers": 0,
            }
        }
        context.bot_data.update(payload)

    async def poll_answer_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = update.poll_answer
        answered_poll = context.bot_data[answer.poll_id]
        try:
            questions = answered_poll["questions"]
        except KeyError:
            return
        selected_options = answer.option_ids
        answer_string = ""
        for question_id in selected_options:
            if question_id != selected_options[-1]:
                answer_string += questions[question_id] + " і "
            else:
                answer_string += questions[question_id]
        await context.bot.send_message(
            answered_poll["chat_id"],
            f"{update.effective_user.mention_html()} відповів {answer_string}!",
            parse_mode=ParseMode.HTML,
        )
        answered_poll["answers"] += 1
        if answered_poll["answers"] == TOTAL_VOTER_COUNT:
            await context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])
