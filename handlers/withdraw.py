from telegram import Update
from telegram.ext import ContextTypes
from database import connect


async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            balance,
            wallet,
            withdrawals_unlocked
        FROM users
        WHERE user_id = ?
    """, (query.from_user.id,))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return

    balance, wallet, unlocked = user

    if not unlocked:
        await query.message.reply_text(
            """
❌ Withdrawals Locked

Purchase at least one active miner to unlock withdrawals.
"""
        )
        return

    if not wallet:
        await query.message.reply_text(
            """
👛 No Wallet Found

Please save your withdrawal wallet first.

Go to:

👛 Wallet
"""
        )
        return

    if balance < 300:
        await query.message.reply_text(
            f"""
❌ Minimum Withdrawal

Current Balance:
{balance:.4f} USDT

Minimum Withdrawal:
300 USDT
"""
        )
        return

    context.user_data["waiting_withdraw_amount"] = True

    await query.message.reply_text(
        f"""
💸 Withdraw Funds

Available Balance

{balance:.4f} USDT

Wallet

{wallet}

━━━━━━━━━━━━━━━━━━

Reply with the amount you want to withdraw.
"""
    )