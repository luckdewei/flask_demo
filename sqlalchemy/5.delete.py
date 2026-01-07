from sqlalchemy import (
    create_engine,
    String,
    delete,
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
    # user = session.scalars(select(User).where(User.name == "赵六")).first()
    # if user:
    #    # 删除单个用户
    #    # DELETE FROM users WHERE users.id = 4
    #    session.delete(user)
    #    session.commit()
    #    print("删除成功")
    # else:
    #    print("用户不存在")

    # 删除的话会返回删除成功的条数
    # DELETE FROM users WHERE users.age > ?
    # This result object does not return rows. It has been closed automatically.
    # DELETE FROM users WHERE users.age > 20
    result = session.execute(delete(User).where(User.age > 20))
    print("delete", result.rowcount)
    session.commit()
