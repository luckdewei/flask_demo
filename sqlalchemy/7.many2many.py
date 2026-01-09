from sqlalchemy import ForeignKey, Integer, String, create_engine, Table, Column, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, Session

# 多对多（Many-to-Many）关系在实际开发中同样非常常见。例如，一个学生（Student）可以选修多门课程（Course），
# 而一门课程也可以被多个学生选修。多对多关系通常通过“关联表 + relationship()”来实现。

# 在ORM模型设计时，我们需要单独定义一张关联表（不对应ORM类，只是Table对象），
# 通过relationship()和secondary参数表明多对多的中介关系。同时可以通过back_populates让关系双向访问。


class Base(DeclarativeBase):
    pass


# 定义用于实现学生与课程多对多关系的关联表，不需要创建独立模型类
student_course = Table(
    "student_course",
    # 绑定到Base的元数据信息
    Base.metadata,
    # 定义学生id列，外键关联到students表的id，设置为主键
    Column("student_id", Integer, ForeignKey("students.id", primary_key=True)),
    # 定义课程id列，外键关联到courses表的id，设置为主键
    Column("course_id", Integer, ForeignKey("courses.id", primary_key=True)),
)


# 定义学生模型类
class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    # 与Course模型建立多对多关系，通过student_course中间表，反向引用为students
    courses: Mapped[list["Course"]] = relationship(
        "Course", secondary=student_course, back_populates="students"
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}')>"


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    # 与Student模型建立多对多关系，通过student_course中间表，反向引用为courses
    students: Mapped[list["Student"]] = relationship(
        "Student", secondary=student_course, back_populates="courses"
    )

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.name}')>"


# 创建SQLite数据库连接，指定文件名为many2many_example.db，echo=True用于打印SQL日志
engine = create_engine("sqlite:///many2many_example.db", echo=True)
# 创建所有数据库表结构
Base.metadata.create_all(engine)

with Session(engine) as session:
    # # 创建两门课程对象
    # course1 = Course(title="高等数学")
    # course2 = Course(title="计算机基础")
    # # 创建两个学生对象，分别选修不同的课程
    # student1 = Student(name="小明", courses=[course1, course2])
    # student2 = Student(name="小红", courses=[course2])
    # # 将学生对象添加到会话中
    # session.add_all([student1, student2])
    # # 提交事务到数据库
    # session.commit()
    # # 打印操作成功的提示
    # print("创建学生和课程成功")

    # # 查询姓名为“小明”的学生及其所选课程
    # stu = session.scalars(select(Student).where(Student.name == "小明")).first()
    # print(f"\n学生：{stu.name}")
    # # 打印学生所选的所有课程名称
    # print("所选课程：")
    # for c in stu.courses:
    #     print(f"  - {c.title}")

    # 查询课程名称为“计算机基础”的课程及所有选修该课程的学生
    cour = session.scalars(select(Course).where(Course.title == "计算机基础")).first()
    # 打印课程名称
    print(f"\n课程：{cour.title}")
    # 打印所有选修该课程的学生姓名
    print("选修学生：")
    for s in cour.students:
        print(f"  - {s.name}")
