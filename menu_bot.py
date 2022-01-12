from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, user
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    conversationhandler,
    dispatcher,
    Filters
)
import logging
from Stock import NseData
from datetime import datetime

METHOD, COMPANY = range(2)

# To store the unique user choice's
UserChoice = {}


def start(update: Update, context: CallbackContext) -> int:
    # print(" -- start -- ")
    user = update.message.from_user
    print(f" {datetime.now()} - User {user['username']} : /start")
    reply_keyboard = [
        ['Search By Name - NSE'], ['Search By ScripCode - NSE'],
        ['Search By Name - BSE'], ['Search By ScripCode - BSE']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Hi! Please choose an option:",
        reply_markup=markup,
    )
    return METHOD


def getCompanyDetailsNSE(company_name: str) -> str:
    company_details = NseData.get_all_details(company_name)
    return company_details


def searchNameinNSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchNameinNSE")
    user = update.message.from_user
    # user_input = update.message.text
    UserChoice[user] = "SearchNameinNSE"
    update.message.reply_text("Please enter the company name:")
    return COMPANY


def searchNameinBSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchNameinBSE")
    pass


def searchScripCodeinNSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchScripCodeinNSE")
    user = update.message.from_user
    # user_input = update.message.text
    UserChoice[user] = "SearchScripCodeinNSE"
    update.message.reply_text("Please enter the company scripCode:")
    return COMPANY


def searchScripCodeinBSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchScripCodeinBSE")
    pass


def reply(update: Update, context: CallbackContext) -> None:
    print(" --> reply")
    user = update.message.from_user
    user_input = update.message.text
    print(user_input)
    if UserChoice[user] == "SearchScripCodeinNSE":
        company_details = getCompanyDetailsNSE(user_input)
        update.message.reply_text(company_details, parse_mode='Markdown')
        return ConversationHandler.END
    elif UserChoice[user] == "SearchScripCodeinBSE":
        pass
    elif UserChoice[user] == "SearchNameinNSE":
        pass
    else:
        pass


def main() -> None:
    try:
        updater = Updater(
            token='2007518409:AAHrriVMo47AlWm5eBWbAqC6paSy015x_AU')
        dispatcher = updater.dispatcher

        print("-------------- > Bot started < -------------- ")

        convHandler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                METHOD: [
                    MessageHandler(Filters.regex(
                        '^Search By Name - NSE$'), searchNameinNSE),
                    MessageHandler(Filters.regex(
                        '^Search By Name - BSE$'), searchNameinBSE),
                    MessageHandler(Filters.regex(
                        '^Search By ScripCode - NSE$'), searchScripCodeinNSE),
                    MessageHandler(Filters.regex(
                        '^Search By ScripCode - BSE$'), searchScripCodeinBSE)
                ],
                COMPANY: [MessageHandler(Filters.text, reply)]
            },
            fallbacks=[CommandHandler('start', start)]
        )

        dispatcher.add_handler(convHandler)

        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(e)


main()
