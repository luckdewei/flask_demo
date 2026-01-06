from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "<div>欢迎访问首页</div>"


# 动态路由
# <name>是URL参数，URL中的这部分值会被 传递给函数
@app.route("/user/<name>")
def user(name):
    return f"<h1>name:{name}</h1>"


# <int:post_id>表示post_id必须是整数
@app.route("/post/<int:post_id>")
def post(post_id):
    return f"<h1>post:{post_id}</h1>"


# 定义当客户端访问/form的时候由此视图函数进行处理
# methods参数指定允许的方法名
@app.route("/form", methods=["GET", "POST"])
def handle_form():
    if request.method == "POST":
        # 如果是POST请求，获取表单的数据
        # request.form是包含表单数据的字典
        username = request.form.get("username", "")
        return f"<h1>收到表单数据{username}</h1>"
    else:
        return """
        <form method="post">
            <label>用户名</label>
            <input type="text" name="username">
            <button type="submit">提交</button>
        </form>
        """


# 启动开发服务器
# host 主机名为0.0.0.0代表监听所有的网络端口 0.0.0.0 127.0.0.1
# 一个是任意ip可以访问，一个是本地
# 一台电脑上可能有多个网卡，每个网卡都有IP地址，当然 也有一个回环地址
# 无线网卡内网的IP地址 192.168.2.106
# port 监听的端口号
# debug 开启调试模式 当源文件发生变更会更自动重启 reload
app.run(host="127.0.0.1", port=5000, debug=True)
