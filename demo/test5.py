from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine(f'sqlite:///F:\Python-code\WorldSimplifiedTextVersion\demo\demo1.db')

Session = Session(engine)

Base = declarative_base()


class Person:
    id = Column(Integer, primary_key=True)
    name = Column(String)

    @classmethod
    def get_by_name(cls, name: str) -> "Person":
        return Session.query(cls).filter(cls.name==name).first()


class Student(Person, Base):
    __tablename__ = 'student'

    ss = 1


class Teacher(Person, Base):
    __tablename__ = 'teacher'

    tt = 2


class Worker(Person, Base):
    __tablename__ = 'worker'

    ww = 3


a = Student.get_by_name(name='weeqw')

b = Teacher.get_by_name(name='1')
c = Worker.get_by_name(name='1')

print(a)  # <__main__.Student object at 0x10d1715c0>
print(b)  # <__main__.Teacher object at 0x10d1716a0>
print(c)  # <__main__.Worker object at 0x10d171780>

Base.metadata.create_all(engine)

# 全局设置
engine = create_engine(f'sqlite:///F:\Python-code\WorldSimplifiedTextVersion\demo\demo1.db')
Base.metadata.create_all(engine)

table_classes = [Student, Teacher, Worker]
for cls in table_classes:
    Base.metadata.create_all(engine, [cls.__table__], checkfirst=True)

print(1)
