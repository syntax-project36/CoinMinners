from telegram import Update
from telegram.ext import ContextTypes

from datetime import datetime

from database import add_user
from keyboards import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.username or "",
        user.first_name or "",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    text = f"""
👋 Welcome to Coin Minners, {user.first_name}!

Mine cryptocurrency with powerful cloud miners.

Choose an option below to get started.
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )