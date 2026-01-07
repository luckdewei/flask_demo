from sqlalchemy import create_engine, String, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from datetime import datetime


# 定义基础类，用作所有的模型类的基类
class Base(DeclarativeBase):
    pass


# 定义User类，映射到数据库里users表
class User(Base):
    __tablename__ = "users"
    # 定义主键ID列，类型为整数 自动增加，唯一的
    id: Mapped[int] = mapped_column(primary_key=True)
    # 定义商品名称列，类型为字符串，最大长度为100字符，不能为空
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    # 年龄 整形
    age: Mapped[int]

    def __repr__(self):
        return f"<User(id={self.id},name={self.name},age={self.age})>"


# 创建数据库引擎，使用sqlite数据库，开启SQL语句回显
engine = create_engine("sqlite:///model_example.db", echo=True)
# 创建所有的定义的数据表
Base.metadata.create_all(engine)
# 使用会话管理器打开数据库会话
with Session(engine) as session:
    # 1.创建模型的实例
    # user1 = User(name="张三", age=18)
    # 2.将user1对象添加到session中，这个时候处于等待添加的状态
    # session.add(user1)
    # 3.提交事务，将user1的信息写入数据库中
    # session.commit()
    # print("添加用户成功")

    users = [
        User(name="李四", age=20),
        User(name="王五", age=22),
        User(name="赵六", age=24),
    ]
    session.add_all(users)
    session.commit()
