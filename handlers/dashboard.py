from telegram import Update
from telegram.ext import ContextTypes

import sqlite3


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    conn = sqlite3.connect("coinminners.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            balance,
            total_withdrawn,
            referrals,
            miner,
            hashrate
        FROM users
        WHERE user_id=?
    """, (query.from_user.id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        balance, withdrawn, referrals, miner, hashrate = row
    else:
        balance = 0
        withdrawn = 0
        referrals = 0
        miner = "USDT Miner V0"
        hashrate = 0

    await query.message.reply_text(
        f"""
💵 COIN MINNERS DASHBOARD

👤 Username:
@{query.from_user.username}

💰 Balance:
{balance:.2f} USDT

💸 Total Withdrawn:
{withdrawn:.2f} USDT

👥 Referrals:
{referrals}

⛏ Active Miner:
{miner}

⚡ Hashrate:
{hashrate} TH/s
"""
    )