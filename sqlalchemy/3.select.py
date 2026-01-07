from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    select,
    desc,
    func,
)
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

with Session(engine) as session:
    # 构造查询（select）： 使用 select(Model) 来指定要查询的数据表和模型。
    # stmt = select(User)
    # all_users = session.scalars(stmt).all()
    # print("所有的用户")
    # for user in all_users:
    #    print(user)
    ## 查询第1个用户
    # first_user = session.scalars(stmt).first()
    # print("第1个用户", first_user)
    ## 按主键查询id为1的用户
    # user_by_id = session.get(User, 1)
    # print("user_by_id", user_by_id)

    # 构造查询（select）： 使用 select(Model) 来指定要查询的数据表和模型。
    stmt = select(User)
    # 添加条件（where）： 可通过 .where() 添加筛选条件，实现类似 SQL 的 WHERE 子句。
    zhang_user = session.scalars(stmt.where(User.name == "张三")).first()
    print("zhang_user", zhang_user)

    young_users = session.scalars(stmt.where(User.age < 20)).all()
    print("young_users", young_users)
    # 排序（order_by）： 使用 .order_by() 进行排序，可升序（默认）或降序（desc）。
    sorted_users = session.scalars(stmt.order_by(desc(User.age))).all()
    print("sorted_users", sorted_users)
    # 限制、分页（limit/offset）： 可通过 .limit() 限制结果数量，.offset() 跳过指定行数，常用于分页查询。
    top2_users = session.scalars(
        stmt.where(User.age < 50).order_by(desc(User.age)).offset(2).limit(2)
    ).all()
    print("top2_users", top2_users)

    # 查询用户的总数量
    # SELECT count(users.id) AS count_1 FROM users
    user_count = session.execute(select(func.count(User.id))).scalar_one()
    print("user_count", user_count)
    # print("user_count", list(user_count)[0][0])
