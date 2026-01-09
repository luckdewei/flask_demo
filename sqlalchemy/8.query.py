# 导入SQLAlchemy必要模块和函数
from sqlalchemy import create_engine, String, and_, or_, select
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column

# 在实际业务中，我们经常会遇到需要根据多个条件综合查询的需求，比如“查找年龄大于某个值且城市为某地的用户”，
# 或者“查找满足多个不同条件之一的记录”等。这时可以使用SQLAlchemy中的and_、or_等函数来拼接复杂的查询条件，实现灵活的多条件过滤。例如，可以查询“年龄大于26且城市为北京”，或者“年龄小于30或所在城市为上海”的所有用户。

# 此外，SQLAlchemy还可以方便地与LIKE模糊匹配、IN列表查询等结合，极大地增强了查询数据的能力。
# 这些复杂条件的查询方式与直接书写SQL相比，ORM风格更优雅、更易维护，同时也更安全（能有效防止SQL注入）。


class Base(DeclarativeBase):
    pass


# 定义用户表对应的User类
class User(Base):
    # 指定表名为users
    __tablename__ = "users"
    # id字段，主键，自增长
    id: Mapped[int] = mapped_column(primary_key=True)
    # name字段，最大长度50
    name: Mapped[str] = mapped_column(String(50))
    # age字段
    age: Mapped[int]
    # city字段，最大长度50
    city: Mapped[str] = mapped_column(String(50))

    # 定义User实例的字符串显示格式
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', age={self.age}, city='{self.city}')>"


engine = create_engine("sqlite:///query_example.db", echo=True)
# 根据ORM模型生成数据库表
Base.metadata.create_all(engine)

# 创建会话
with Session(engine) as session:
    # 构建用户数据列表
    users = [
        User(name="张三", age=25, city="北京"),
        User(name="李四", age=30, city="上海"),
        User(name="王五", age=28, city="北京"),
        User(name="赵六", age=35, city="广州"),
    ]
    # 添加所有用户数据到会话
    session.add_all(users)
    # 提交会话到数据库持久化数据
    session.commit()

    # 使用AND条件查询：年龄大于25并且城市为北京的用户
    result1 = session.scalars(
        select(User).where(and_(User.age > 25, User.city == "北京"))
    )
    # 输出查询结果
    print("年龄大于25且城市为北京的用户：")
    for user in result1:
        # 打印用户信息
        print(user)

    # 使用OR条件查询：年龄小于25或者城市为上海的用户
    result2 = session.scalars(
        select(User).where(or_(User.age < 25, User.city == "上海"))
    ).all()
    # 输出查询结果
    print("\n年龄小于25或城市为上海的用户：")
    for user in result2:
        # 打印用户信息
        print(user)

    # 使用LIKE查询：姓名以'张'开头的用户
    result3 = session.scalars(select(User).where(User.name.like("张%"))).all()
    # 输出查询结果
    print("\n姓名以'张'开头的用户：")
    for user in result3:
        # 打印用户信息
        print(user)
    # 使用IN查询：城市为北京或上海的用户
    result4 = session.scalars(select(User).where(User.city.in_(["北京", "上海"]))).all()
    # 输出查询结果
    print("\n城市为北京或上海的用户：")
    for user in result4:
        # 打印用户信息
        print(user)
    # 使用BETWEEN范围查询：年龄在28到32之间的用户（包含28和32）
    result5 = session.scalars(select(User).where(User.age.between(28, 32))).all()
    # 输出查询结果
    print("\n年龄在28到32之间的用户：")
    for user in result5:
        # 打印用户信息
        print(user)
