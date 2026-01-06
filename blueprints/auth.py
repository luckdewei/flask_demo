from flask import Blueprint, render_template, request, redirect, url_for

# 创建Blueprint实例
# 第1个参数auth指的是BluePrint名称
# 第2个参数__name__用于确定BluePrint根路径
# url_prefix="/auth" 表示所有的路由都会自动添加/auth的前缀
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    return render_template("auth/register.html")
