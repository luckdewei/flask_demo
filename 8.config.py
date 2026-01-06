# 导入Flask类和os模块
from flask import Flask
import os
from dotenv import load_dotenv

# 读取当前目录下面的.env文件，把文件中的key value设置到环境变量中，以便 可以通过os.getenv("FLASK_DEBUG", "False") 获取
load_dotenv()

# 创建Flask应用实例
app = Flask(__name__)

# 从环境变量读取配置
# os.getenv()获取环境变量，如果不存在则使用默认值
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "False") == "True"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-secret-key")
app.config["DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///mydatabase.db")

print(f"app.config:{app.config}")
