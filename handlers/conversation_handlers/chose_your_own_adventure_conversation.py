from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler

BRAWLER_PICK, SHOWDOWN_OR_BRAWLBALL, SHOWDOWN, BUSH, POWERCUBE, BRAWLBALL, QUESTION, DEFEAT = range(8)


class AdventureHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('startgame', cls.startgame)],
            states={
                BRAWLER_PICK: [MessageHandler(filters.Regex('^(8-Bit|Fang)$'), cls.brawler_pick)],
                SHOWDOWN_OR_BRAWLBALL: [MessageHandler(filters.Regex('^(Showdown|BrawlBall)$'),
                                                       cls.showdown_or_brawlball)],
                SHOWDOWN: [MessageHandler(filters.Regex('^(Bush|Powercube)$'), cls.showdown)],
                BRAWLBALL: [MessageHandler(filters.Regex('^(PassToGoal|PassTeamBro)$'), cls.brawlball)],
                DEFEAT: [MessageHandler(filters.Regex('^(Yes|No)$'), cls.defeat)],
                QUESTION: [MessageHandler(filters.Regex('^(Yes|No)$'), cls.question)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('8-Bit'), KeyboardButton('Fang')],
            [KeyboardButton('/exit'), KeyboardButton('/startgame')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            f'Привіт {update.effective_user.first_name}! Якого персонажа ти вибереш?',
            reply_markup=reply_markup)

        return BRAWLER_PICK

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Ви вийшли з розмови.')

        return ConversationHandler.END

    @staticmethod
    async def brawler_pick(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Showdown'), KeyboardButton('BrawlBall')],
            [KeyboardButton('/exit'), KeyboardButton('/startgame')]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            f'Який режим вибирете?',
            reply_markup=reply_markup)

        brawler_pick = update.message.text
        context.user_data['brawler_pick'] = brawler_pick

        return SHOWDOWN_OR_BRAWLBALL

    @staticmethod
    async def showdown_or_brawlball(update: Update, context: ContextTypes.DEFAULT_TYPE):

        showdown_or_brawlball = update.message.text
        context.user_data['showdown_or_brawlball'] = showdown_or_brawlball

        if update.message.text == 'Showdown':
            keyboard = [
                [KeyboardButton('Bush'), KeyboardButton('Powercube')],
                [KeyboardButton('/exit'), KeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(text=f"Вітаю {update.effective_user.first_name}!"
                                                 f" Ви вибрали {context.user_data['showdown_or_brawlball']}!"
                                                 f" І йдете туда за {context.user_data['brawler_pick']}",
                                                 reply_markup=reply_markup)

            showdown_or_brawlball = update.message.text
            context.user_data['showdown_or_brawlball'] = showdown_or_brawlball

            return SHOWDOWN

        else:
            keyboard = [
                [KeyboardButton('PassToGoal'), KeyboardButton('PassTeamBro')],
                [KeyboardButton('/exit'), KeyboardButton('/startgame')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(text=f"Вітаю мамкин футболіст!"
                                                 f" Ти вибрав {context.user_data['showdown_or_brawlball']}!"
                                                 f" І ідеш туда за {context.user_data['brawler_pick']}",
                                                 reply_markup=reply_markup)

            showdown_or_brawlball = update.message.text
            context.user_data['showdown_or_brawlball'] = showdown_or_brawlball

            return BRAWLBALL

    @staticmethod
    async def showdown(update: Update, context: ContextTypes.DEFAULT_TYPE):

        if update.message.text == 'Bush':
            keyboard = [
                [KeyboardButton('Yes'), KeyboardButton('No')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f'Ех блін {update.effective_user.first_name}!:( Ви вирішили просидіти у кущах всю ігру.'
                f' Під кінець ігри у вас не було КубівСили і вас вбили.'
                f' Почати спочатку?',
                reply_markup=reply_markup)

            return QUESTION

        else:
            keyboard = [
                [KeyboardButton('Yes'), KeyboardButton('No')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f'Це погано. Ви вирішили получити КубикиСили но вас вбила Amber яка була у сусідніх кущах. '
                f'Почати спочатку?',
                reply_markup=reply_markup)

            return DEFEAT

    @staticmethod
    async def brawlball(update: Update, context: ContextTypes.DEFAULT_TYPE):

        if update.message.text == 'PassToGoal':
            keyboard = [
                [KeyboardButton('Yes'), KeyboardButton('No')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f' Ви вирішили самі вдарити у ворота і ви забили гол!'
                f' Всі на своєму екрані бачуть надпис: {context.user_data["brawler_pick"]} забиває гол!'
                f' Почати спочатку?',
                reply_markup=reply_markup)

            return QUESTION

        else:
            keyboard = [
                [KeyboardButton('Yes'), KeyboardButton('No')]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f'Ви вирішили дати пас тімейту і він промахнувся по пустим воротам,'
                f' противники відібрали мяч і забили у ваші ворота. Ви програли з рахунком 2:0 в їхню користь.'
                f' Почати спочатку?',
                reply_markup=reply_markup)

            return DEFEAT

    @staticmethod
    async def defeat(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Yes':
            keyboard = [
                [InlineKeyboardButton('Yes', callback_data='Yes')],
                [InlineKeyboardButton('No', callback_data='No')]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"Ви виграли, чи бажаєте почати з початку?", reply_markup=reply_markup)
            return BRAWLER_PICK
        elif answer == 'No':
            await update.message.reply_text(
                f'Кінець ігри.')
            return ConversationHandler.END

    @staticmethod
    async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Yes':
            await update.message.reply_text(
                f'Це погано. Ви вирішили получити КубикиСили но вас вбила Amber яка була у сусідніх кущах.')
            keyboard = [
                [InlineKeyboardButton('Yes', callback_data='Yes')],
                [InlineKeyboardButton('No', callback_data='No')]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"Ви виграли, чи бажаєте почати з початку?", reply_markup=reply_markup)
            return BRAWLER_PICK
        elif answer == 'No':
            await update.message.reply_text(
                f'Кінець ігри.')
            return ConversationHandler.END
