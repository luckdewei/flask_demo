# 导入Flask类和request对象
from flask import Flask, request, jsonify

# 创建Flask应用实例
app = Flask(__name__)


# 定义处理表单的路由
# methods=['GET', 'POST']表示支持GET和POST两种请求方法
@app.route("/login", methods=["GET", "POST"])
def login():
    # 判断请求方法
    if request.method == "POST":
        # 获取表单数据
        print(f"request:{request}")
        # request.form是包含表单数据的字典
        if request.is_json:
            data = request.get_json()
            print(f"data:{data}")
            return jsonify({"message": "JSON data received", "data": data})
        else:
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            # 简单的验证逻辑（实际应用中应该连接数据库）
            if username == "admin" and password == "123456":
                return f"<h1>登录成功！</h1><p>欢迎，{username}！</p>"
            else:
                return "<h1>登录失败</h1><p>用户名或密码错误</p>"
    else:
        # GET请求，显示登录表单
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>登录</title>
        </head>
        <body>
            <h1>用户登录</h1>
            <form method="post">
                <label>用户名：</label><br>
                <input type="text" name="username" required><br><br>
                <label>密码：</label><br>
                <input type="password" name="password" required><br><br>
                <button type="submit">登录</button>
            </form>
        </body>
        </html>
        """


# 定义获取URL参数的路由
# 访问 /search?q=Flask 时，q='Flask'
@app.route("/search")
def search():
    # 获取URL参数
    # request.args是包含URL参数的字典
    query = request.args.get("q", "")
    if query:
        return f"<h1>搜索结果</h1><p>搜索关键词：{query}</p>"
    else:
        return "<h1>请输入搜索关键词</h1>"


# 运行应用
if __name__ == "__main__":
    app.run(debug=True)
