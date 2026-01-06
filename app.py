# 导入Flask类
from flask import Flask, render_template

# 导入Blueprint
# 从blueprints包中导入auth模块
from blueprints.auth import auth_bp

# 创建Flask应用实例
app = Flask(__name__)

# 注册Blueprint
# register_blueprint()方法将Blueprint注册到应用中
app.register_blueprint(auth_bp)


# 定义首页路由
@app.route("/")
def index():
    # 渲染首页模板
    return render_template("index.html")


# 运行应用
if __name__ == "__main__":
    app.run(debug=True)
