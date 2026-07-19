from database import add_user
from keyboards import main_menu
from announcements import announce
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus
from datetime import datetime

from config import CHANNEL_USERNAME

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    is_new = add_user(
        user.id,
        user.username or "",
        user.first_name or "",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    if is_new:

        username = f"@{user.username}" if user.username else "No username"

        await announce(
            context.bot,
            f"""🎉 <b>NEW MINER JOINED</b>

👤 <b>{user.first_name}</b>
🔹 {username}

Welcome to the CoinMinners community! 🚀"""
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "📢 Join Official Channel",
                    url=f"https://t.me/{CHANNEL_USERNAME}"
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ I've Joined",
                    callback_data="verify_channel"
                )
            ]
        ]

        await update.message.reply_text(
            f"""👋 Welcome to Coin Minners, {user.first_name}!

Before you begin mining, please join our official announcements channel.

You'll receive:
• 💸 Withdrawal proofs
• 🎁 Bonuses
• 🚀 New miner releases
• 📢 Important updates

After joining, tap "✅ I've Joined" below.""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        await update.message.reply_text(
            f"""👋 Welcome back, {user.first_name}!""",
            reply_markup=main_menu()
        )

async def verify_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    member = await context.bot.get_chat_member(
        chat_id=f"@{CHANNEL_USERNAME}",
        user_id=user_id
    )

    if member.status in (
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ):
        await query.edit_message_text(
            "✅ Verification successful!\n\nWelcome to CoinMinners."
        )

        await context.bot.send_message(
            chat_id=user_id,
            text="Choose an option below to get started.",
            reply_markup=main_menu()
        )

    else:
        await query.answer(
            "❌ Please join our official channel first.",
            show_alert=True
        )