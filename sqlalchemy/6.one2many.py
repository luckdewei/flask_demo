"""
sqlalchemy.6.one2many 的 Docstring
一对多
"""

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
    update,
    delete,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from datetime import datetime
import time


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
    # User 类通过 addresses 属性（类型为列表）和 relationship() 实现对多个 Address 的管理
    # 并设置了 back_populates 以支持双向访问。
    addresses: Mapped[list["Address"]] = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id},name={self.name},age={self.age})>"


class Address(Base):
    __tablename__ = "addresses"
    # 定义主键ID列，类型为整数 自动增加，唯一的
    id: Mapped[int] = mapped_column(primary_key=True)
    # 定义外键user_id,关联到users表的id字段
    # Address 类则用 user_id 字段作为外键指定所属用户
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # 定义email列，类型为字符串，最大长度为100字符，不能为空
    email: Mapped[str] = mapped_column(String(100))
    # 定义与User表的多对一的关系
    # Address 类同时也通过 relationship() 实现对 User 的访问，并通过 back_populates 关联上述关系。
    user: Mapped[User] = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(id={self.id},email={self.email}>"


# 创建数据库引擎，使用sqlite数据库，开启SQL语句回显
engine = create_engine("sqlite:///model_example.db", echo=True)
# 创建所有的定义的数据表
Base.metadata.create_all(engine)

with Session(engine) as session:
    # user = User(
    #    name="李四",
    #    age=30,
    #    addresses=[
    #        Address(email="李四家里的地址@qq.com"),
    #        Address(email="李四公司的地址@qq.com"),
    #    ],
    # )
    # session.add(user)
    # session.commit()
    # print("添加用户成功", user)
    # SELECT users.id, users.name, users.age FROM users WHERE users.name = ? id=2
    # SELECT addresses.id AS addresses_id, addresses.user_id AS addresses_user_id, addresses.email AS addresses_email
    # FROM addresses WHERE 2 = addresses.user_id
    # user = session.scalars(select(User).where(User.name == "李四")).first()
    # print(f"用户:{user.name}")
    # for address in user.addresses:
    #    print(f"地址:{address.email}")
    #  SELECT addresses.id, addresses.user_id, addresses.email FROM addresses WHERE addresses.email =  "李四家里的地址@qq.com"
    # ELECT users.id AS users_id, users.name AS users_name, users.age AS users_age
    # FROM users WHERE users.id = 2

    # address = session.scalars(
    #    select(Address).where(Address.email == "李四家里的地址@qq.com")
    # ).first()
    # print(f"地址:{address.email}")
    ## 里面是懒加载的，如果读取user属性才会属性，不读不查询
    # print(f"用户:{address.user.name}")

    # SELECT users.id, users.name, users.age FROM users WHERE users.name = "李四"
    # users.id = 2
    # SELECT addresses.id AS addresses_id, addresses.user_id AS addresses_user_id, addresses.email AS addresses_email
    # FROM addresses WHERE 2 = addresses.user_id
    # addresses.id [1,2]
    # DELETE FROM addresses WHERE addresses.id = 1
    # DELETE FROM addresses WHERE addresses.id = 2
    # DELETE FROM users WHERE users.id = 2
    user = session.scalars(select(User).where(User.name == "李四")).first()
    session.delete(user)
    session.commit()


# cascade什么是cascade
# 数据库层面的级联操作： 当父表记录发生变化时，自动对子表进行相应的操作
# ORM层面的级联操作 当父对象发生变化的时候，自动对子对象进行相关操作
# cascade="all, delete-orphan"
# all包括了以下操作
#   save-update 将新的对象添加到会话时，也添加相关的对象
#   merge 合并会话时，也合并相关对象
#   expunge 从会话删除时，也清除相关的对象
#   delete 删除对象时，也删除相关的对象
#   delete-orphan 删除变成孤立对象 的相关对象
#   refresh-expire 刷新对象时，也刷新相关的对象 查询一个用户信息，过一段时间想获取此用户的最新信息的话，可以使用refresh刷新此对象的属性为最新的数据库信息
#     delete-orphan 当子对象从父对象的集合被 移除的时候，会自动删除子对象，注意是仅当子对象不再与任何父对象关联明才会删除


# 插入的时候 先插主表再插子表
# 删除的时候 先删除子表再删除主表
# 在真正生产环境中，我们一般是不会真正删除数据，会执行逻辑删除。每个表加一个字段dr=0表示正常，dr=1表示逻辑删除
