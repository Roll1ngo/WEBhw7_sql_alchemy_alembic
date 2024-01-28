from src.db import engine
from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(250), nullable=False)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(250), nullable=False)
    group_id = Column(ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship('Group', backref='students')


class Disciplines(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship('Teacher', backref='disciplines')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column(Date, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    disciplines_id = Column(Integer, ForeignKey(
        'disciplines.id', ondelete='CASCADE'))
    student = relationship('Student', backref='grades')
    disciplines = relationship('Disciplines', backref='grades')


Base.metadata.create_all(engine)
