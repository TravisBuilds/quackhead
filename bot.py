from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from quackHeadBill import convo, append_to_convo
import os 
PORT = int(os.environ.get('PORT', '8443'))

TOKEN = os.getenv("TELEGRAM_KEY")

session = {}


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("Hello! Welcome to Highstreet")


def help(update, context):
    update.message.reply_text("""
    Talk to me!
    
    """)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', context)


def about(update, context):
    update.message.reply_text("""
           Talk to me to help Highstreet develop the next generation of NPCs.
        """)


def contact(update, context):
    update.message.reply_text("Developer: FomoDuck \n email: dev@highstreet.market\n")


def handle_message(update, context):
    chat_log = session.get('chat_log')
    answer = convo(update.message.text, chat_log)
    session['chat_log'] = append_to_convo(update.message.text, answer,
                                                         chat_log)
    update.message.reply_text(f"{str(answer)}")


def main():
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    bot = updater.dispatcher

    bot.add_handler(telegram.ext.CommandHandler("start", start))
    bot.add_handler(telegram.ext.CommandHandler("help", help))
    bot.add_handler(telegram.ext.CommandHandler("about", about))
    bot.add_handler(telegram.ext.CommandHandler("contact", contact))
    bot.add_handler(telegram.ext.MessageHandler(
    telegram.ext.Filters.text, handle_message))

    bot.add_error_handler(error)
    updater.start_polling()

    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://quackhead.herokuapp.com/' + TOKEN
    )

    updater.idle()


if __name__ == '__main__':
    main()