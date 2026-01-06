from flask import Flask, render_template

app = Flask(__name__)


def get_current_user():
    return "Alice"


@app.context_processor
def inject_user():
    current_user = get_current_user()
    site_title = "我的站点"
    return dict(current_user=current_user, site_title=site_title)


@app.route("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name)


@app.route("/users")
def show_users():
    users = ["张三", "李四", "王五"]
    return render_template("users.html", users=users)


app.run(debug=True)
