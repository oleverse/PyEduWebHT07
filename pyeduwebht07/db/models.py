from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.functions import concat
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Grade(Base):
    __tablename__ = "grades"
    id = Column("id", Integer, primary_key=True)
    got_at = Column("got_at", DateTime, nullable=False, default=DateTime())
    mark = Column("mark", Integer, nullable=False)
    student_id = Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"))
    subject_id = Column("subject_id", Integer, ForeignKey("subjects.id", ondelete="CASCADE"))


class Group(Base):
    __tablename__ = "groups"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(256), nullable=False, unique=True)
    students = relationship("Student", backref="group")


class Student(Base):
    __tablename__ = "students"
    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String(256), nullable=False)
    last_name = Column("last_name", String(256), nullable=False)
    group_id = Column("group_id", Integer, ForeignKey(Group.id, ondelete="SET NULL"))
    grades = relationship("Grade", backref="student", cascade="all, delete")

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String(256), nullable=False)
    last_name = Column("last_name", String(256), nullable=False)
    subjects = relationship("Subject", backref="teacher")

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name


class Subject(Base):
    __tablename__ = "subjects"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(256), nullable=False)
    teacher_id = Column("teacher_id", Integer, ForeignKey(Teacher.id, ondelete="SET NULL"))
