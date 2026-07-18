import sqlite3

DB_NAME = "coinminners.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        balance REAL DEFAULT 0,
        total_withdrawn REAL DEFAULT 0,
        referrals INTEGER DEFAULT 0,
        miner TEXT DEFAULT 'USDT Miner V0',
        hashrate INTEGER DEFAULT 0,
        wallet TEXT DEFAULT '',
        withdrawals_unlocked INTEGER DEFAULT 0,
        join_date TEXT,
        miner_expiry TEXT
    )
    """)

    # PURCHASES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        miner TEXT,
        quantity INTEGER,
        amount REAL,
        crypto TEXT,
        wallet_address TEXT,
        txid TEXT,
        status TEXT DEFAULT 'Pending',
        reminder_active INTEGER DEFAULT 1,
        purchase_date TEXT,
        contract_end TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id, username, first_name, join_date):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users
    (user_id, username, first_name, join_date)
    VALUES(?,?,?,?)
    """, (user_id, username, first_name, join_date))

    conn.commit()
    conn.close()


def add_purchase(
    user_id,
    username,
    miner,
    quantity,
    amount,
    crypto,
    wallet_address,
    purchase_date,
    contract_end
):
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
    VALUES(?,?,?,?,?,?,?,?,?)
    """, (
        user_id,
        username,
        miner,
        quantity,
        amount,
        crypto,
        wallet_address,
        purchase_date,
        contract_end
    ))

    conn.commit()
    conn.close()
