from decouple import config
import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 👋\n\n"
        "Welcome to the bot! Here are the available commands:\n"
        "/start - Show this welcome message\n"
        "/test - Show a message with URL button"
    )


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with URL button when the command /test is issued."""
    keyboard = [
        [
            InlineKeyboardButton(
                "Visit Python-Telegram-Bot", url="https://python-telegram-bot.org"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click the button below to visit the documentation:", reply_markup=reply_markup
    )


async def handle_greetings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle various greeting messages."""
    user = update.effective_user
    await update.message.reply_text(f"Hey {user.first_name}! pie lur? 😊")


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("test", test))

    # Add greeting message handler - compile pattern first
    greeting_pattern = re.compile(r"^(hi|hai|halo|hallo)$", re.IGNORECASE)
    application.add_handler(
        MessageHandler(filters.Regex(greeting_pattern), handle_greetings)
    )

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
