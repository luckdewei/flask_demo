import sqlite3

DATABASE_URL = "example.db"
conn = sqlite3.connect(DATABASE_URL)
cursor = conn.cursor()
cursor.execute(
    """
    create table if not exists users(
        id integer primary key  autoincrement,
        name text not null,
        email text not null unique,
        created_at TIMESTAMPT DEFAULT CURRENT_TIMESTAMP
    )
    """
)

# test_users = [("张三", "zhangsan@qq.com"), ("李四", "lisi@qq.com")]
# for name, email in test_users:
#     cursor.execute("INSERT INTO users(name,email) VALUES(?,?)", (name, email))
# conn.commit()
# conn.close()

cursor = conn.execute("SELECT *  FROM users where id = ?", (1,))
user = cursor.fetchone()
print(user)
