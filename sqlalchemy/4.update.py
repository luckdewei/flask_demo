from sqlalchemy import (
    create_engine,
    String,
    update,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


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

with Session(engine) as session:
    #  SELECT users.id, users.name, users.age FROM users WHERE users.name = ?
    # user = session.scalars(select(User).where(User.name == "张三")).first()
    # if user:
    #    user.age = 26
    #    # UPDATE users SET age=? WHERE users.id = ?   (26, 1)
    #    session.commit()
    #    print("更新成功", user)
    # else:
    #    print("用户不存在")
    # UPDATE users SET age=? WHERE users.age > ? (30, 20)
    # UPDATE users SET age=30 WHERE users.age > 20
    session.execute(update(User).where(User.age > 20).values(age=30))
    session.commit()
