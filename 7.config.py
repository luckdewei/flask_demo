# 导入Flask类
from flask import Flask

# 创建Flask应用实例
app = Flask(__name__)

# 直接设置配置项
# app.config是一个字典，可以像普通字典一样操作
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config["DATABASE_URI"] = "sqlite:///mydatabase.db"

# 也可以使用update()方法批量设置
app.config.update(
    DEBUG=True,
    SECRET_KEY="your-secret-key-here",
    DATABASE_URI="sqlite:///mydatabase.db",
)

# 访问配置
print(app.config["DEBUG"])  # 输出: True
