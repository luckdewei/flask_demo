# 导入SQLAlchemy必要模块和函数
from sqlalchemy import create_engine, String, and_, or_, select, func
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column

# 在实际数据库开发中，我们经常需要对数据进行统计和汇总分析，这就是“聚合查询”。
# 聚合操作可以快速返回某些字段的统计值，比如总数(count)、平均值(avg)、最大值(max)、最小值(min)、总和(sum)等。
# SQLAlchemy通过func模块调用这些数据库原生聚合函数，非常简单直观。


# 定义ORM模型基类
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


# 创建sqlite引擎，echo=True用于打印生成的SQL
engine = create_engine("sqlite:///query_example.db", echo=True)
# 根据ORM模型生成数据库表
Base.metadata.create_all(engine)


# 创建数据库会话，并在会话范围内进行数据操作
with Session(engine) as session:
    # 查询所有用户的平均年龄
    # avg_age = session.execute(select(func.avg(User.age))).scalar_one()
    avg_age = session.scalars(select(func.avg(User.age))).first()
    # 打印平均年龄，保留两位小数
    print(f"平均年龄：{avg_age:.2f}")

    # 查询所有用户中的最大年龄
    max_age = session.execute(select(func.max(User.age))).scalar_one()
    # 打印最大年龄
    print(f"最大年龄：{max_age}")

    # 查询所有用户中的最小年龄
    min_age = session.execute(select(func.min(User.age))).scalar_one()
    # 打印最小年龄
    print(f"最小年龄：{min_age}")

    # 查询所有用户年龄总和
    total_age = session.execute(select(func.sum(User.age))).scalar_one()
    # 打印年龄总和
    print(f"年龄总和：{total_age}")

    # 查询所有用户的数量
    user_count = session.execute(select(func.count(User.id))).scalar_one()
    # 打印用户总数
    print(f"用户总数：{user_count}")

    # 按城市对用户进行分组统计，每个城市对应用户数量和平均年龄
    city_stats = session.execute(
        select(
            User.city,
            func.count(User.id).label("count"),
            func.avg(User.age).label("avg_age"),
        ).group_by(User.city)
    ).all()
    # 打印分组统计结果
    print("\n按城市分组统计：")
    # 遍历每个城市的分组统计结果，依次输出
    for city, count, avg_age in city_stats:
        print(f"  {city}: {count}人, 平均年龄{avg_age:.2f}")
