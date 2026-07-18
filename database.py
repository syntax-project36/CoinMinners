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
        total_earned REAL DEFAULT 0,
        total_withdrawn REAL DEFAULT 0,
        referrals INTEGER DEFAULT 0,
        referral_earnings REAL DEFAULT 0,
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

    # WITHDRAWALS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS withdrawals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        wallet TEXT,
        amount REAL,
        status TEXT DEFAULT 'Pending',
        request_date TEXT
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
    
    
def update_balance(user_id, amount):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET
            balance = balance + ?,
            total_earned = total_earned + ?
        WHERE user_id = ?
    """, (
        amount,
        amount,
        user_id
    ))

    conn.commit()
    conn.close()


def approve_purchase(purchase_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE purchases
        SET status = 'Approved'
        WHERE id = ?
    """, (purchase_id,))

    conn.commit()
    conn.close()


def activate_miner(user_id, miner, hashrate, expiry):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET
            miner = ?,
            hashrate = ?,
            withdrawals_unlocked = 1,
            miner_expiry = ?
        WHERE user_id = ?
    """, (
        miner,
        hashrate,
        expiry,
        user_id
    ))

    conn.commit()
    conn.close()


def add_withdrawal(user_id, username, wallet, amount, request_date):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO withdrawals(
            user_id,
            username,
            wallet,
            amount,
            request_date
        )
        VALUES(?,?,?,?,?)
    """, (
        user_id,
        username,
        wallet,
        amount,
        request_date
    ))

    conn.commit()
    conn.close()


def approve_withdrawal(withdrawal_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE withdrawals
        SET status = 'Approved'
        WHERE id = ?
    """, (withdrawal_id,))

    conn.commit()
    conn.close()


def reject_withdrawal(withdrawal_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, amount
        FROM withdrawals
        WHERE id = ?
    """, (withdrawal_id,))

    row = cursor.fetchone()

    if row:
        user_id, amount = row

        cursor.execute("""
            UPDATE users
            SET balance = balance + ?
            WHERE user_id = ?
        """, (amount, user_id))

        cursor.execute("""
            UPDATE withdrawals
            SET status = 'Rejected'
            WHERE id = ?
        """, (withdrawal_id,))

    conn.commit()
    conn.close()


def admin_add_balance(user_id, amount):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET
            balance = balance + ?,
            total_earned = total_earned + ?
        WHERE user_id = ?
    """, (
        amount,
        amount,
        user_id,
    ))

    conn.commit()
    conn.close()