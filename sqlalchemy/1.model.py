from sqlalchemy import create_engine, String, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


# 定义基础类，用作所有的模型类的基类
class Base(DeclarativeBase):
    pass


# 定义Product类，映射到数据库里products表
class Product(Base):
    # 指定表名为products
    __tablename__ = "products"
    # 定义主键ID列，类型为整数
    id: Mapped[int] = mapped_column(primary_key=True)
    # 定义商品名称列，类型为字符串，最大长度为100字符，不能为空
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # 价格 浮点数
    price: Mapped[float]
    # 布尔值
    is_avaiable: Mapped[bool] = mapped_column(default=True)
    # 创建时间 默认为当前时间
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self):
        return f"<Product(id={self.id},name={self.name},price={self.price})>"


# 创建数据库引擎，使用sqlite数据库，开启SQL语句回显
engine = create_engine("sqlite:///model_example.db", echo=True)
# 创建所有的定义的数据表
Base.metadata.create_all(engine)
print("表创建成功")
