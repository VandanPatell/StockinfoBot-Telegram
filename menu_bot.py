from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    dispatcher,
    Filters
)

from Stock import NseData


METHOD, MARKET, COMPANY = range(3)

UserChoice = {}


def start(update: Update, context: CallbackContext) -> int:
    print(" --> start")
    reply_keyboard = [['Search By Name', 'Search By ScripCode']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Hi! Please choose an option:",
        reply_markup=markup,
    )
    return METHOD


def getCompanyDetailsNSE(company_name: str) -> str:
    company_details = NseData.get_all_details(company_name)
    return company_details


def MarketByName(update: Update, context: CallbackContext) -> int:
    print(" --> MarketByName")
    user_data = context.user_data
    print(user_data)
    reply_keyboard = [['Search Name In NSE', 'Search Name In BSE']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Hi! Please choose an option:",
        reply_markup=markup,
    )
    return MARKET


def MarketByScripCode(update: Update, context: CallbackContext) -> int:
    print(" --> MarketByScripCode")
    reply_keyboard = [['NSE ScripCode', 'BSE ScripCode']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Hi! Please choose an option:",
        reply_markup=markup,
    )
    return MARKET


def searchNameinNSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchNameinNSE")
    pass


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


def reply(update: Update, context: CallbackContext) -> None:
    print(" --> reply")
    user = update.message.from_user
    user_input = update.message.text
    print(user_input)
    if UserChoice[user] == "SearchScripCodeinNSE":
        company_details = getCompanyDetailsNSE(user_input)
        update.message.reply_text(company_details, parse_mode='Markdown')
    elif UserChoice[user] == "SearchScripCodeinBSE":
        pass
    else:
        pass


def searchScripCodeinBSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchScripCodeinBSE")
    pass


def market(update: Update, context: CallbackContext) -> int:
    print(" --> market")
    reply_keyboard = [['Search In NSE', 'Search In BSE']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Hi! Please choose an option:",
        reply_markup=markup,
    )
    return COMPANY


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
                        '^Search By Name$'), MarketByName),
                    MessageHandler(Filters.regex(
                        '^Search By ScripCode$'), MarketByScripCode)
                ],
                MARKET: [
                    MessageHandler(Filters.regex(
                        '^Search Name In NSE$'), searchNameinNSE),
                    MessageHandler(Filters.regex(
                        '^Search Name In BSE$'), searchNameinBSE),
                    MessageHandler(Filters.regex(
                        '^NSE ScripCode$'), searchScripCodeinNSE),
                    MessageHandler(Filters.regex(
                        '^BSE ScripCode$'), searchScripCodeinBSE)
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
