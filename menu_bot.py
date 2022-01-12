from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, user
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    commandhandler,
    conversationhandler,
    dispatcher,
    Filters
)
import sys
import os
from Stock import NseData
from Stock import bse
from datetime import datetime

METHOD, COMPANY, NAME, DETAILS = range(4)

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


def getCompanyDetailsBSECode(company_name: str) -> str:
    company_details = bse.get_all_details_by_scripCode(company_name)
    return company_details


def searchNameinNSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchNameinNSE")
    user = update.message.from_user
    # user_input = update.message.text
    UserChoice[user] = "SearchNameinNSE"
    update.message.reply_text("Please enter the company name:")
    return NAME


def get_all_company_names_nse(update: Update, context: CallbackContext) -> int:
    print(" --> get_all_company_names_nse")
    # user = update.message.from_user
    # user_input = update.message.text
    # if NseData.search_company:
    #     for i in NseData.search_company(user_input):
    # reply_keyboard = [
    #     ['Search By Name - NSE'], ['Search By ScripCode - NSE'],
    #     ['Search By Name - BSE'], ['Search By ScripCode - BSE']
    # ]
    # markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # update.message.reply_text(
    #     "Hi! Please choose an option:",
    #     reply_markup=markup,
    # )
    return NAME


def searchNameinBSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchNameinBSE")
    user = update.message.from_user
    # user_input = update.message.text
    UserChoice[user] = "SearchNameinNSE"
    update.message.reply_text("Please enter the company name:")
    return NAME


def searchScripCodeinNSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchScripCodeinNSE")
    user = update.message.from_user
    # user_input = update.message.text
    UserChoice[user] = "SearchScripCodeinNSE"
    update.message.reply_text("Please enter the company scripCode:")
    return COMPANY


def searchScripCodeinBSE(update: Update, context: CallbackContext) -> int:
    print(" --> searchScripCodeinBSE")
    user = update.message.from_user
    UserChoice[user] = "SearchScripCodeinBSE"
    update.message.reply_text("Please enter the company scripCode:")
    return COMPANY


def reply(update: Update, context: CallbackContext) -> int:
    print(" --> reply")
    user = update.message.from_user
    user_input = update.message.text
    print(user_input)
    if UserChoice[user] == "SearchScripCodeinNSE":
        company_details = getCompanyDetailsNSE(user_input)
        update.message.reply_text(company_details, parse_mode='Markdown')
        return ConversationHandler.END
    elif UserChoice[user] == "SearchScripCodeinBSE":
        company_details = getCompanyDetailsBSECode(user_input)
        update.message.reply_text(company_details, parse_mode='Markdown')
        return ConversationHandler.END
    elif UserChoice[user] == "SearchNameinNSE":
        return NAME
    elif UserChoice[user] == "SearchNameinBSE":
        return NAME
    else:
        pass


def searchByName(update: Update, context: CallbackContext) -> int:
    print(" --> searchByName")
    user = update.message.from_user
    user_input = update.message.text
    print(user_input)
    if UserChoice[user] == "SearchNameinNSE":
        list_l = []
        for i in NseData.search_company(user_input):
            # update.message.reply_text(i)
            l = []
            l.append(i)
            list_l.append(l)
        # print(list_l)
        reply_keyboard = list_l
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Hi! Please choose The Company Name:",
            reply_markup=markup,
        )
        return DETAILS
    elif UserChoice[user] == "SearchNameinBSE":
        list_l = []
        for i in bse.search_companies_by_name(user_input):
            # update.message.reply_text(i)
            l = []
            l.append(i)
            list_l.append(l)
        reply_keyboard = list_l
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Please Choose the company name: ", reply_markup=markup)
        return DETAILS
    else:
        pass
    return ConversationHandler.END


def returnDetailsByName(update: Update, context: CallbackContext) -> None:
    print(" --> returnDteailsByName")
    user = update.message.from_user
    user_input = update.message.text
    print(user_input)
    if UserChoice[user] == "SearchNameinNSE":
        company_details = NseData.get_details_by_name(user_input)
        update.message.reply_text(company_details, parse_mode='Markdown')
    if UserChoice[user] == "SearchNameinBSE":
        company_details = bse.get_details_by_name(user_input)
        update.message.reply_text(company_details, parse_mode='Markdown')
    return ConversationHandler.END


def company_NAMES(update: Update, context: CallbackContext) -> None:
    print(" --> company_NAMES")
    user = update.message.from_user
    user_input = update.message.text
    print(user_input)

    # company_details = NseData.(user_input)
    # update.message.reply_text(company_details, parse_mode='Markdown')
    return ConversationHandler.END


def main() -> None:
    try:
        updater = Updater('2007518409:AAHrriVMo47AlWm5eBWbAqC6paSy015x_AU')
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
                COMPANY: [MessageHandler(Filters.text, reply)],
                NAME: [MessageHandler(Filters.text, searchByName)],
                DETAILS: [MessageHandler(Filters.text, returnDetailsByName)]
            },
            fallbacks=[CommandHandler('start', start)]
        )
        dispatcher.add_handler(convHandler)
        dispatcher.add_handler(CommandHandler('search', start))

        updater.start_polling()
        updater.idle()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e, exc_tb.tb_lineno)


main()
