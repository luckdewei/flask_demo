from flask import Flask, render_template, g
from datetime import datetime

app = Flask(__name__)

# 在多个模板中都需要使用相同的变量时（如用户信息、网站配置等），如果每个视图函数都传递这些变量会很繁琐。
# Flask提供了`@app.context_processor`装饰器，可以向所有模板的上下文注入全局变量。


def format_date(date):
    return date.strftime("%Y年%m月%d日")


def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "早上好"
    elif hour < 18:
        return "下午好"
    else:
        return "晚上好"


@app.context_processor
def inject_helpers():
    return {"format_date": format_date, "get_greeting": get_greeting}


@app.route("/index")
def index():
    return render_template("index.html", current_date=datetime.now())


app.run(debug=True)
