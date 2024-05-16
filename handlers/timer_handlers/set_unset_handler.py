from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from handlers.base_handler import BaseHandler


class SetUnsetHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(CommandHandler("timer", cls.timer))
        app.add_handler(CommandHandler("set", cls.set_timer))
        app.add_handler(CommandHandler("unset", cls.unset))

    @staticmethod
    async def timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Привіт! Використовуйте /set <seconds>, щоб встановити таймер")

    @staticmethod
    async def alarm(context: ContextTypes.DEFAULT_TYPE):
        job = context.job
        await context.bot.send_message(job.chat_id, text=f"Біп! {job.data} секунд закінчено!")

    @staticmethod
    def remove_job_if_exists(name, context: ContextTypes.DEFAULT_TYPE):
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    @classmethod
    async def set_timer(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        try:
            due = float(context.args[0])
            if due < 0:
                await update.effective_message.reply_text("Вибачте, ми не можемо повернутися в майбутнє!")
                return

            job_removed = cls.remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_once(cls.alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

            text = "Таймер успішно встановлено!"
            if job_removed:
                text += " Старий таймер видалений."
            await update.effective_message.reply_text(text)

        except (IndexError, ValueError):
            await update.effective_message.reply_text("Використовуйте: /set <секунди>")

    @classmethod
    async def unset(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        job_removed = cls.remove_job_if_exists(str(chat_id), context)
        text = "Таймер успішно скасовано!" if job_removed else "У вас немає активного таймера."
        await update.message.reply_text(text)
