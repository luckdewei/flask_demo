# 导入Flask类和jsonify函数
# Flask用于创建Web应用
# jsonify用于将Python字典转换为JSON响应
from flask import Flask, jsonify, redirect, url_for

# 创建Flask应用实例
app = Flask(__name__)

# 模拟用户数据（实际应用中来自数据库）
users = [
    {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
    {"id": 2, "name": "李四", "email": "lisi@example.com"},
    {"id": 3, "name": "王五", "email": "wangwu@example.com"},
]


# 定义获取所有用户的API
# 返回JSON格式的数据
@app.route("/api/users", methods=["GET"])
def get_users():
    # 使用jsonify将Python字典列表转换为JSON响应
    # jsonify会自动设置Content-Type为application/json
    return jsonify(users)


# 定义获取单个用户的API
# <int:user_id>是URL参数，必须是整数
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # 根据ID查找用户
    user = next((u for u in users if u["id"] == user_id), None)

    # 如果用户不存在，返回404错误
    if user is None:
        # jsonify也可以返回错误信息
        return jsonify({"error": "用户未找到"}), 404

    # 返回用户信息
    return jsonify(user)


# 定义创建用户的API
# 使用POST方法创建新资源
@app.route("/api/users", methods=["POST"])
def create_user():
    # 从请求中获取JSON数据
    # request.json包含请求体中的JSON数据
    from flask import request

    data = request.json

    # 简单的验证
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "缺少必填字段"}), 400

    # 创建新用户（实际应用中应该保存到数据库）
    new_user = {"id": len(users) + 1, "name": data["name"], "email": data["email"]}
    users.append(new_user)

    # 返回新创建的用户信息
    return jsonify(new_user), 201  # 201表示资源创建成功
    # return redirect(url_for("get_users"))


# 运行应用
if __name__ == "__main__":
    app.run(debug=True)
