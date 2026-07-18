from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard")],
        [InlineKeyboardButton("⛏️ USDT Mining", callback_data="mining")],
        [
            InlineKeyboardButton("👥 Referrals", callback_data="referrals"),
            InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")
        ],
        [
            InlineKeyboardButton("👛 Wallet", callback_data="wallet"),
            InlineKeyboardButton("🆘 Support", callback_data="support")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def miners_menu():
    keyboard = [
        [InlineKeyboardButton("🥇 USDŦ Miner V1", callback_data="miner_v1")],
        [InlineKeyboardButton("🥈 USDŦ Miner V2", callback_data="miner_v2")],
        [InlineKeyboardButton("🥉 USDŦ Miner V3", callback_data="miner_v3")],
        [InlineKeyboardButton("⬅️ Back", callback_data="home")]
    ]

    return InlineKeyboardMarkup(keyboard)


def buy_menu():
    keyboard = [
        [InlineKeyboardButton("🛒 Buy 1 Miner", callback_data="buy1")],
        [InlineKeyboardButton("🛒 Buy 2 Miners", callback_data="buy2")],
        [InlineKeyboardButton("🛒 Buy 3 Miners", callback_data="buy3")],
        [InlineKeyboardButton("⬅️ Back", callback_data="mining")]
    ]

    return InlineKeyboardMarkup(keyboard)
