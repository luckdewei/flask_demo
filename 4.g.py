from flask import Flask, render_template, g
import sqlite3

DATABASE_URL = "./example.db"

app = Flask(__name__)


def get_db():
    db = getattr(g, "_xxx", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_URL)
        # 设置返回字典格式的游标 更易用
        db.row_factory = sqlite3.Row
    return db


# 定义在请求结束的时候关闭数据库连接的函数
# teardown_appcontext 装饰器会在请求结束的时候执行
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, "_xxx", None)
    if db is not None:
        db.close()


def get_user_by_id(user_id):
    db = get_db()
    cursor = db.execute("SELECT *  FROM users where id = ?", (user_id,))
    user = cursor.fetchone()
    return dict(user) if user else None


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = get_user_by_id(user_id)
    return f"""
     <h1>用户信息</h1>
     <p>ID:{user['id']}</p>
     <p>姓名:{user['name']}</p>
     <p>邮箱:{user['email']}</p>
    """


app.run(debug=True)
