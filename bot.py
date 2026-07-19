from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from database import create_tables
from minerscheduler import run_mining

from handlers.start import start, verify_channel
from handlers.mining import button_handler
from handlers.withdraw import withdraw
from handlers.admin import (
    approve,
    purchases,
    withdrawals,
    approvewithdraw,
    rejectwithdraw,
    addbalance,
)
from handlers.wallet import wallet


def main():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()
    
    app.job_queue.run_repeating(
    run_mining,
    interval=3600,
    first=10,
)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
    CallbackQueryHandler(
        verify_channel,
        pattern="^verify_channel$"
    )
)
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("purchases", purchases))
    app.add_handler(CommandHandler("withdrawals", withdrawals))
    app.add_handler(CommandHandler("approvewithdraw", approvewithdraw))
    app.add_handler(CommandHandler("rejectwithdraw", rejectwithdraw))
    app.add_handler(CommandHandler("addbalance", addbalance))
    app.add_handler(CallbackQueryHandler(withdraw, pattern="^withdraw$"))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wallet))

    print("✅ Coin Minners Pro is running...")

    app.run_polling()


if __name__ == "__main__":
    main()