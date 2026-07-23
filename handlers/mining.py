  from telegram import (
      Update,
      InlineKeyboardButton,
      InlineKeyboardMarkup,
  )
  from telegram.ext import ContextTypes
  
  from miners import MINERS
  from wallets import WALLETS
  from datetime import datetime, timedelta
  from database import connect
    
  def mining_menu():
        keyboard = [
            [InlineKeyboardButton("🥇 USDŦ Miner V1", callback_data="miner_v1")],
            [InlineKeyboardButton("🥈 USDŦ Miner V2", callback_data="miner_v2")],
            [InlineKeyboardButton("🥉 USDŦ Miner V3", callback_data="miner_v3")],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")],
        ]
    
        return InlineKeyboardMarkup(keyboard)
    
    
  def buy_menu(miner):
        keyboard = [
            [InlineKeyboardButton("🛒 Buy 1 Miner", callback_data=f"{miner}_buy_1")],
            [InlineKeyboardButton("🛒 Buy 2 Miners", callback_data=f"{miner}_buy_2")],
            [InlineKeyboardButton("🛒 Buy 3 Miners", callback_data=f"{miner}_buy_3")],
            [InlineKeyboardButton("⬅️ Back", callback_data="mining")],
        ]
    
        return InlineKeyboardMarkup(keyboard)
    
    
  def payment_menu():
        keyboard = [
            [InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data="pay_BTC")],
            [InlineKeyboardButton("💵 USDT (TRC20)", callback_data="pay_USDT_TRC20")],
            [InlineKeyboardButton("💵 USDT (BEP20)", callback_data="pay_USDT_BEP20")],
            [InlineKeyboardButton("💵 USDT (ERC20)", callback_data="pay_USDT_ERC20")],
            [InlineKeyboardButton("💵 USDT (TON)", callback_data="pay_USDT_TON")],
            [InlineKeyboardButton("⚡ Tron (TRX)", callback_data="pay_TRX")],
            [InlineKeyboardButton("◎ Solana (SOL)", callback_data="pay_SOL")],
            [InlineKeyboardButton("🔷 BNB Smart Chain", callback_data="pay_BNB")],
            [InlineKeyboardButton("⟠ Ethereum", callback_data="pay_ETH")],
            [InlineKeyboardButton("💎 TON", callback_data="pay_TON")],
            [InlineKeyboardButton("🌊 SUI", callback_data="pay_SUI")],
            [InlineKeyboardButton("⬅️ Back", callback_data="mining")],
        ]
    
        return InlineKeyboardMarkup(keyboard)
    
    
  async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
        query = update.callback_query
        await query.answer()
    
        if query.data == "dashboard":
    
    
            conn = connect()
            cursor = conn.cursor()
    
            cursor.execute("""
                SELECT
                    balance,
                    total_earned,
                    total_withdrawn,
                    referrals,
                    referral_earnings,
                    miner,
                    hashrate,
                    miner_expiry
                FROM users
                WHERE user_id = ?
            """, (query.from_user.id,))
    
            user = cursor.fetchone()
            conn.close()
    
            if user:
                (
                    balance,
                    total_earned,
                    withdrawn,
                    referrals,
                    referral_earnings,
                    miner,
                    hashrate,
                    expiry,
                ) = user
            else:
                balance = 0
                total_earned = 0
                withdrawn = 0
                referrals = 0
                referral_earnings = 0
                miner = "USDT Miner V0"
                hashrate = 0
                expiry = "Not Active"
    
            status = "🟢 Active" if miner != "USDT Miner V0" else "🔴 Inactive"
    
            await query.message.reply_text(
                f"""
    💎 COIN MINNERS PRO
    ━━━━━━━━━━━━━━━━━━
    
    👤 Username
    @{query.from_user.username or "No Username"}
    
    🆔 User ID
    {query.from_user.id}
    
    ━━━━━━━━━━━━━━━━━━
    
    ⛏ Active Miner
    {miner}
    
    ⚡ Hashrate
    {hashrate} TH/s
    
    🟢 Status
    {status}
    
    ━━━━━━━━━━━━━━━━━━
    
    💰 Balance
    {balance:.4f} USDT
    
    📈 Total Earned
    {total_earned:.4f} USDT
    
    💸 Total Withdrawn
    {withdrawn:.4f} USDT
    
    ━━━━━━━━━━━━━━━━━━
    
    👥 Referrals
    {referrals}
    
    🎁 Referral Earnings
    {referral_earnings:.4f} USDT
    
    ━━━━━━━━━━━━━━━━━━
    
    📅 Contract Ends
    {expiry}
    """
            )
    
        elif query.data == "earnings":
  
    
            conn = connect()
            cursor = conn.cursor()
    
            cursor.execute("""
                SELECT
                    balance,
                    total_earned,
                    miner,
                    miner_expiry
                FROM users
                WHERE user_id = ?
            """, (query.from_user.id,))
    
            user = cursor.fetchone()
            conn.close()
    
            if user:
                balance, total_earned, miner, expiry = user
            else:
                balance = 0
                total_earned = 0
                miner = "USDT Miner V0"
                expiry = "Not Active"
    
            hourly = 0
            daily = 0
            monthly = 0
    
            for m in MINERS.values():
                if m["name"] == miner:
                    daily = float(m["daily"].split()[0])
                    monthly = float(m["monthly"].split()[0])
                    hourly = daily / 24
                    break
    
            await query.message.reply_text(
                f"""
    📈 MY EARNINGS
    
    ━━━━━━━━━━━━━━━━━━
    
    💰 Current Balance
    {balance:.4f} USDT
    
    📈 Total Earned
    {total_earned:.4f} USDT
    
    ━━━━━━━━━━━━━━━━━━
    
    ⏰ Hourly Earnings
    {hourly:.4f} USDT
    
    📅 Daily Earnings
    {daily:.4f} USDT
    
    🗓 Monthly Earnings
    {monthly:.4f} USDT
    
    ━━━━━━━━━━━━━━━━━━
    
    ⛏ Active Miner
    {miner}
    
    📅 Contract Ends
    {expiry}
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
    
            context.user_data["miner_id"] = miner_id
            context.user_data["quantity"] = int(quantity)
            print(context.user_data)
    
            miner = MINERS[miner_id]
    
            total = miner["price"] * int(quantity)
    
            await query.message.reply_text(
                f"""
    💳 SELECT PAYMENT METHOD
    
    Miner:
    {miner["name"]}
    
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
  
            context.user_data["coin"] = coin
            print(context.user_data)
  
            wallet = WALLETS.get(coin, "Wallet not available")
  
            await query.message.reply_text("TEST PAYMENT")
    
        elif query.data == "paid":
    
            from config import ADMIN_ID
    
            miner_id = context.user_data["miner_id"]
            quantity = context.user_data["quantity"]
            coin = context.user_data["coin"]
    
            miner = MINERS[miner_id]
            amount = miner["price"] * quantity
            wallet = WALLETS[coin]
    
            purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            contract_end = (
                datetime.now() + timedelta(days=30)
            ).strftime("%Y-%m-%d %H:%M:%S")
    
            conn = connect()
            cursor = conn.cursor()
    
            cursor.execute("""
            INSERT INTO purchases
            (
                user_id,
                username,
                miner,
                quantity,
                amount,
                crypto,
                wallet_address,
                purchase_date,
                contract_end
            )
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                query.from_user.id,
                query.from_user.username or "",
                miner["name"],
                quantity,
                amount,
                coin,
                wallet,
                purchase_date,
                contract_end,
            ))
    
            purchase_id = cursor.lastrowid
            conn.commit()
            conn.close()
    
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"""
    🔔 New Miner Purchase
    
    Purchase ID: {purchase_id}
    
    User: @{query.from_user.username or "No Username"}
    User ID: {query.from_user.id}
    
    Miner: {miner["name"]}
    Quantity: {quantity}
    Amount: ${amount:.2f}
    Network: {coin}
    
    Approve with:
    /approve {purchase_id}
    """
            )
    
            await query.message.reply_text(
                f"""
    ✅ Payment Submitted
    
    Your purchase has been recorded.
    
    Status: Pending Verification
    
    Miner: {miner["name"]}
    Quantity: {quantity}
    Amount: ${amount:.2f}
    Network: {coin}
    
    An administrator will verify your payment and activate your miner.
    """
            )
    
    
        elif query.data == "wallet":
    
    
            conn = connect()
            cursor = conn.cursor()
    
            cursor.execute("""
                SELECT wallet
                FROM users
                WHERE user_id = ?
            """, (query.from_user.id,))
    
            result = cursor.fetchone()
            conn.close()
    
            current_wallet = result[0] if result and result[0] else "Not Set"
    
            context.user_data["waiting_wallet"] = True
    
            await query.message.reply_text(
                f"""
    👛 MY WALLET
    
    ━━━━━━━━━━━━━━━━━━
    
    Current Wallet
    
    {current_wallet}
    
    ━━━━━━━━━━━━━━━━━━
    
    Send your USDT wallet address.
    
    Example:
    
    TQ3nxxxxxxxxxxxxxxxxxxxx
    """
            )
    
        elif query.data == "home":
    
            from keyboards import main_menu
    
            await query.message.reply_text(
                """
    🏠 COIN MINNERS
    
    Welcome back!
    
    Choose an option below.
    """,
                reply_markup=main_menu()
            )