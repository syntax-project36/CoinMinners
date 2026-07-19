from database import add_user
from keyboards import main_menu
from announcements import announce


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

    text = f"""
👋 Welcome to Coin Minners, {user.first_name}!

Mine cryptocurrency with powerful cloud miners.

Choose an option below to get started.
"""

    await update.message.reply_text(
        text,
        reply_markup=main_menu()
    )