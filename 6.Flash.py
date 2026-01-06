# 导入Flask类和flash、get_flashed_messages函数
# flash用于存储消息
# get_flashed_messages用于获取消息
from flask import Flask, flash, redirect, url_for, render_template, request, session

# 创建Flask应用实例
app = Flask(__name__)

# 设置密钥（Flash Messages需要session支持，session需要密钥）
# session 存储是后端存储
app.config["SECRET_KEY"] = "your-secret-key-here"

# 模拟用户数据（实际应用中来自数据库）
users = {"admin": "123456", "user1": "password123"}


# 定义登录路由
@app.route("/login", methods=["GET", "POST"])
def login():
    # 判断请求方法
    if request.method == "POST":
        # 获取表单数据
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # 验证用户名和密码
        if username in users and users[username] == password:
            # 登录成功，存储用户信息到session
            session["username"] = username
            # 使用flash()存储成功消息
            # 第一个参数是消息内容，第二个参数是消息类别（可选）
            flash("登录成功！欢迎回来。", "success")
            # 重定向到首页
            return redirect(url_for("index"))
        else:
            # 登录失败，存储错误消息
            flash("用户名或密码错误，请重试。", "error")
            # 重新显示登录页面
            return redirect(url_for("login"))
    else:
        # GET请求，显示登录表单
        return render_template("login.html")


# 定义登出路由
@app.route("/logout")
def logout():
    # 清除session中的用户信息
    session.pop("username", None)
    # 存储登出成功消息
    flash("您已成功登出。", "info")
    # 重定向到首页
    return redirect(url_for("index"))


# 定义首页路由
@app.route("/")
def index():
    # 渲染首页模板（Flash Messages会自动在模板中显示）
    return render_template("index2.html")


# 运行应用
if __name__ == "__main__":
    app.run(debug=True)
