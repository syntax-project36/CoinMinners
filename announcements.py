from telegram.constants import ParseMode
from config import CHANNEL_ID, BOT_USERNAME


async def announce(bot, message):
    text = (
        f"{message}\n\n"
        f'<a href="https://t.me/{BOT_USERNAME}">🚀 Click to start your mining journey</a>'
    )

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
