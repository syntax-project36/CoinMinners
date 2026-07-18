from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from config import BOT_TOKEN
from database import create_tables, add_user
from datetime import datetime
from keyboards import main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
    user.id,
    user.username,
    user.first_name,
    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)
    referral_link = f"https://t.me/Coinminnersbot?start={user.id}"

    text = f"""
☺️ COIN MINNERS BOT ☺️

⚡️ Automated Hourly Rewards, Instant Payouts 24/7

✳️ Referral Invite: +25 USDT
💎 Premium Invite: +35 USDT

🟢 Automatic Payouts to your USDT Wallet

🎁 Share & Earn Referral Bonus 👇

{referral_link}
"""

    await update.message.reply_text(
    text,
    reply_markup=main_menu()
)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "dashboard":
        await query.edit_message_text(
            "💵 COIN MINNERS USER DASHBOARD\n\n"
            "👤 Account ID: @" + query.from_user.username + "\n"
            "💰 Current Balance: 0.00 USDT\n"
            "💸 Total Withdrawn: 0.00 USDT\n"
            "👥 Referrals: 0 Users\n\n"
            "⛏ Miner: USDT Miner V0\n"
            "⚡ Hashrate: 0 TH/s\n\n"
            "💡 Start your mining here:\n"
            "/usdtmining"
        )

    elif query.data == "mining":
        await query.edit_message_text(
            "⛏️ Choose your USDT Miner.\n\n"
            "🥇 Miner V1 - $4\n"
            "🥈 Miner V2 - $6\n"
            "🥉 Miner V3 - $8"
        )

    elif query.data == "wallet":
        await query.edit_message_text("👛 Wallet feature coming next...")

    elif query.data == "withdraw":
        await query.edit_message_text(
            "💸 Minimum withdrawal is 300 USDT."
        )

    elif query.data == "referrals":
        await query.edit_message_text(
            "👥 Invite friends and earn rewards!"
        )

    elif query.data == "support":
        await query.edit_message_text(
            "🆘 Support will be added soon."
        )
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ Coin Minners Bot is running...")

app.run_polling()
