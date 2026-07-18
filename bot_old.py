from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
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
from handlers.mining import mining_menu, buy_menu, payment_menu
from miners import MINERS
from wallets import WALLETS


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

⚡ Automated Hourly Rewards
🟢 Instant Payouts 24/7

✳️ Referral Invite: +25 USDT
💎 Premium Invite: +35 USDT

🎁 Your Referral Link

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

        await query.message.reply_text(
            f"""
💵 COIN MINNERS DASHBOARD

👤 Username:
@{query.from_user.username}

💰 Balance:
0.00 USDT

💸 Total Withdrawn:
0.00 USDT

👥 Referrals:
0

⛏ Active Miner:
USDT Miner V0

⚡ Hashrate:
0 TH/s
"""
        )

    elif query.data == "mining":

        await query.edit_message_text(
            """
🛒 COIN MINNERS STORE

Choose your mining package.

⛏ Every miner runs for 30 Days.

🔒 Withdrawals remain locked until you own at least one active miner.
""",
            reply_markup=mining_menu()
        )

    elif query.data in MINERS:

        miner = MINERS[query.data]


        await query.message.reply_photo(
            photo=open(miner["image"], "rb"),
            caption=f"""
{miner["name"]}

⚡ Hashrate:
{miner["hashrate"]}

💰 Daily Earnings:
{miner["daily"]}

💵 Monthly Return:
{miner["monthly"]}

💲 Price:
${miner["price"]}

⏳ Duration:
{miner["duration"]}

━━━━━━━━━━━━━━

🔒 Withdrawal Status

Locked

Purchase at least one active miner to unlock withdrawals.
""",
            reply_markup=buy_menu(query.data)
        )
        elif "_buy_" in query.data:

        miner_id, _, quantity = query.data.rpartition("_buy_")
        miner = MINERS[miner_id]
        total = miner["price"] * int(quantity)

        await query.message.reply_text(
            f"""
💳 SELECT PAYMENT METHOD

Miner:
{miner['name']}

Quantity:
{quantity}

Total:
${total:.2f}

Choose the cryptocurrency you want to use for payment.
""",
            reply_markup=payment_menu()
        )

    elif query.data.startswith("pay_"):

        coin = query.data.replace("pay_", "")
        wallet = WALLETS.get(coin, "Wallet not available")

        await query.message.reply_text(
            f"""
💳 PAYMENT DETAILS

🌐 Network:
{coin}

📥 Wallet Address:

`{wallet}`

📋 Tap and hold the wallet address above to copy it.

⚠️ Send the exact amount to the wallet address above.

After payment, click the button below.
""",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I've Paid", callback_data="paid")]
            ])
        )

    elif query.data == "paid":

        await query.message.reply_text(
            "✅ Thank you!\n\n"
            "Your payment has been submitted for verification.\n"
            "Once confirmed, your miner will be activated."
        )
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ Coin Minners Bot is running...")

app.run_polling()
