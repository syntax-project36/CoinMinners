
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from database import (
    connect,
    add_withdrawal,
)


async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ---------- SAVE WALLET ----------
    if context.user_data.get("waiting_wallet"):

        address = update.message.text.strip()

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET wallet = ?
            WHERE user_id = ?
        """, (
            address,
            update.effective_user.id,
        ))

        conn.commit()
        conn.close()

        context.user_data["waiting_wallet"] = False

        await update.message.reply_text(
            f"""
✅ Wallet Saved

Your withdrawal wallet has been updated.

👛 Wallet Address

{address}
"""
        )
        return

    # ---------- WITHDRAW ----------
    if context.user_data.get("waiting_withdraw_amount"):
        print("Withdrawal received")

        try:
            amount = float(update.message.text)
        except ValueError:
            await update.message.reply_text(
                "❌ Please enter a valid number."
            )
            return

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT balance, wallet
            FROM users
            WHERE user_id = ?
        """, (update.effective_user.id,))

        user = cursor.fetchone()

        if not user:
            conn.close()
            return

        balance, wallet = user

        if amount < 300:
            conn.close()
            await update.message.reply_text(
                "❌ Minimum withdrawal is 300 USDT."
            )
            return

        if amount > balance:
            conn.close()
            await update.message.reply_text(
                "❌ Insufficient balance."
            )
            return

        cursor.execute("""
            UPDATE users
            SET balance = balance - ?
            WHERE user_id = ?
        """, (
            amount,
            update.effective_user.id,
        ))

        conn.commit()
        conn.close()

        add_withdrawal(
            update.effective_user.id,
            update.effective_user.username or "",
            wallet,
            amount,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        context.user_data["waiting_withdraw_amount"] = False

        await update.message.reply_text(
            f"""
✅ Withdrawal Request Submitted

Amount:
{amount:.2f} USDT

Wallet:
{wallet}

Status:
Pending Approval
"""
        )