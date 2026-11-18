import sqlite3

conn = sqlite3.connect("rakuten.db")

conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    role TEXT NOT NULL
    )

""")



conn.execute(
    """
    INSERT OR IGNORE INTO users (user_id, username, role)
    VALUES(?, ?, ?)
    """,
    ("USER_A", "H", "admin")
)

conn.execute(
    """
    INSERT OR IGNORE INTO users (user_id, username, role)
    VALUES(?,?,?)
    """,
    ("USER_B", "V", "user")
)
cursor = conn.execute("SELECT * FROM users")


conn.commit()

print(cursor.fetchall())
conn.close()
