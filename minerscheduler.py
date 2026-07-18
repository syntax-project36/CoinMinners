from database import connect, update_balance
from datetime import datetime
from miners import MINERS


async def run_mining(context):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id,
               miner,
               hashrate,
               miner_expiry
        FROM users
        WHERE withdrawals_unlocked = 1
    """)

    users = cursor.fetchall()

    for user_id, miner, hashrate, expiry in users:

        if not expiry:
            continue

        if datetime.now() > datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S"):
            continue

        miner_data = None

        for m in MINERS.values():
            if m["name"] == miner:
                miner_data = m
                break

        if miner_data:
            daily = float(miner_data["daily"].split()[0])
            hourly = daily / 24
            update_balance(user_id, hourly)

    conn.close()