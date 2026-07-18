from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

from config import ADMIN_ID
from database import (
    connect,
    approve_purchase,
    activate_miner,
    approve_withdrawal,
    reject_withdrawal,
    admin_add_balance,
)
from miners import MINERS


async def purchases(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if str(update.effective_user.id) != str(ADMIN_ID):
        return

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            miner,
            quantity,
            amount,
            crypto,
            purchase_date
        FROM purchases
        WHERE status='Pending'
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("No pending purchases.")
        return

    text = "🛒 Pending Purchases\n\n"

    for row in rows:
        purchase_id, username, miner, quantity, amount, crypto, date = row

        text += (
            f"ID: {purchase_id}\n"
            f"User: @{username}\n"
            f"Miner: {miner}\n"
            f"Quantity: {quantity}\n"
            f"Amount: ${amount:.2f}\n"
            f"Crypto: {crypto}\n"
            f"Date: {date}\n\n"
        )

    text += "Approve with:\n/approve <purchase_id>"

    await update.message.reply_text(text)


async def withdrawals(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if str(update.effective_user.id) != str(ADMIN_ID):
        return

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            amount,
            wallet,
            request_date
        FROM withdrawals
        WHERE status='Pending'
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("No pending withdrawals.")
        return

    text = "💸 Pending Withdrawals\n\n"

    for row in rows:
        withdrawal_id, username, amount, wallet, date = row

        text += (
            f"ID: {withdrawal_id}\n"
            f"User: @{username}\n"
            f"Amount: {amount:.2f} USDT\n"
            f"Wallet: {wallet}\n"
            f"Date: {date}\n\n"
        )

    text += (
        "Approve:\n"
        "/approvewithdraw <id>\n\n"
        "Reject:\n"
        "/rejectwithdraw <id>"
    )

    await update.message.reply_text(text)


async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if str(update.effective_user.id) != str(ADMIN_ID):
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage:\n/approve <purchase_id>"
        )
        return

    try:
        purchase_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Usage:\n/approve <purchase_id>"
        )
        return

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, miner
        FROM purchases
        WHERE id=? AND status='Pending'
    """, (purchase_id,))

    purchase = cursor.fetchone()

    if not purchase:
        await update.message.reply_text("Purchase not found.")
        conn.close()
        return

    user_id, miner_name = purchase

    miner = None
    for m in MINERS.values():
        if m["name"] == miner_name:
            miner = m
            break

    if miner is None:
        await update.message.reply_text("Miner not found.")
        conn.close()
        return

    expiry = (
        datetime.now() + timedelta(days=30)
    ).strftime("%Y-%m-%d %H:%M:%S")

    approve_purchase(purchase_id)

    activate_miner(
        user_id,
        miner["name"],
        miner["hashrate"],
        expiry,
    )

    conn.close()

    await context.bot.send_message(
        user_id,
        f"""
🎉 Payment Confirmed!

Your {miner["name"]} has been activated.

⚡ Hashrate: {miner["hashrate"]}

Mining has started automatically.

Happy mining!
"""
    )

    await update.message.reply_text("✅ Purchase approved.")


async def approvewithdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if str(update.effective_user.id) != str(ADMIN_ID):
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage:\n/approvewithdraw <id>"
        )
        return

    try:
        withdrawal_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Usage:\n/approvewithdraw <id>"
        )
        return

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id
        FROM withdrawals
        WHERE id=? AND status='Pending'
    """, (withdrawal_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        await update.message.reply_text("Withdrawal not found.")
        return

    user_id = row[0]

    approve_withdrawal(withdrawal_id)

    await context.bot.send_message(
        user_id,
        "✅ Your withdrawal has been approved and will be processed shortly."
    )

    await update.message.reply_text(
        "✅ Withdrawal approved."
    )


async def rejectwithdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if str(update.effective_user.id) != str(ADMIN_ID):
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage:\n/rejectwithdraw <id>"
        )
        return

    try:
        withdrawal_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Usage:\n/rejectwithdraw <id>"
        )
        return

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id
        FROM withdrawals
        WHERE id=? AND status='Pending'
    """, (withdrawal_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        await update.message.reply_text("Withdrawal not found.")
        return

    user_id = row[0]

    reject_withdrawal(withdrawal_id)

    await context.bot.send_message(
        user_id,
        "❌ Your withdrawal request was rejected. The funds have been returned to your balance."
    )

    await update.message.reply_text(
        "✅ Withdrawal rejected and refunded."
    )


async def addbalance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if str(update.effective_user.id) != str(ADMIN_ID):
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage:\n/addbalance <user_id> <amount>"
        )
        return

    try:
        user_id = int(context.args[0])
        amount = float(context.args[1])
    except ValueError:
        await update.message.reply_text(
            "Invalid user ID or amount."
        )
        return

    admin_add_balance(user_id, amount)

    try:
        await context.bot.send_message(
            user_id,
            f"""
💰 Bonus Added

{amount:.2f} USDT has been credited to your account.

Current balance has been updated.
"""
        )
    except Exception:
        pass

    await update.message.reply_text(
        f"✅ Added {amount:.2f} USDT to user {user_id}."
    )