from random import randint
from rich import print

from sqlalchemy import func, desc, and_

from src.db import session
from src.models import Teacher, Group, Student, Disciplines, Grade


def select_one():
    """Select_one: Знайти 5 студентів із найбільшим середнім балом\
    з усіх предметів. :return list[tuple]"""

    result = session.query(
        Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student) \
        .group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

    return result


def select_two(discipline_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета.\
        :return list[tuple]"""

    result = session.query(Disciplines.name, Student.fullname,
                           func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).join(Disciplines) \
        .filter(Disciplines.id == discipline_id) \
        .group_by(Student.id, Disciplines.name) \
        .order_by(desc('avg_grade')).limit(1).all()
    return result


def select_three(discipline_id: int):
    """Знайти середній бал у групах з певного предмета.\
        :return list[tuple]"""

    result = session.query(Group.name,
                           Disciplines.name,
                           func.round(func.avg(Grade.grade),
                                      2).label('avg_grade')) \
        .select_from(Grade).join(Student).join(Group).join(Disciplines) \
        .filter(Disciplines.id == discipline_id) \
        .group_by(Group.name, Disciplines.name) \
        .order_by(desc('avg_grade')).all()

    return result


def select_four():
    """Знайти середній бал на потоці (по всій таблиці оцінок).\
        :return list(tuple)"""

    result = session.query(func.round(func.avg(Grade.grade), 2)
                           .label('avg_grade')).select_from(Grade).all()

    return result


def select_five(teacher_id: int):
    """ВідЗнайти які курси читає певний викладач.\
        :return list(tuple)"""

    result = session.query(Disciplines.name, Teacher.fullname) \
        .select_from(Grade).join(Disciplines).join(Teacher) \
        .filter(Disciplines.teacher_id == teacher_id).limit(1).all()

    return result


def select_six(group_id: int):
    """Знайти список студентів у певній групі.\
        :return list(tuple)"""

    result = session.query(Group.name, Student.fullname) \
        .select_from(Student).join(Group) \
        .filter(group_id == Student.group_id).all()

    return result


def select_seven(group_id: int, discipline_id: int):
    """Знайти оцінки студентів у окремій групі з певного предмета.\
        :return list(tuple)"""

    result = session.query(Grade.grade, Student.fullname,
                           Group.name, Disciplines.name) \
        .select_from(Grade).join(Disciplines).join(Student).join(Group) \
        .filter(and_(discipline_id == Grade.disciplines_id,
                     group_id == Student.group_id)) \
        .group_by(Student.fullname,
                  Grade.grade,
                  Group.name,
                  Disciplines.name).order_by(desc(Student.fullname)) \
        .limit(10).all()

    return result


def select_eight(teacher_id: int):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів.\
        :return list(tuple)"""

    result = session.query(Teacher.fullname,
                           Disciplines.name,
                           func.round(func.avg(Grade.grade),
                                      2).label('avg_grade')
                           ).select_from(Grade) \
        .join(Disciplines).join(Teacher) \
        .filter(teacher_id == Disciplines.teacher_id) \
        .group_by(Teacher.fullname, Disciplines.name).all()

    return result


def select_nine(student_id: int):
    """Знайти список курсів, які відвідує певний студент.\
        :return list(tuple)"""

    result = session.query(Student.fullname, Disciplines.name) \
        .select_from(Grade).join(Disciplines) \
        .join(Student).filter(student_id == Grade.student_id) \
        .group_by(Student.fullname, Disciplines.name).all()

    return result


def select_ten(student_id: int, teacher_id: int):
    """Список курсів, які певному студенту читає певний викладач.\
        :return list(tuple)"""

    result = session.query(Disciplines.name,
                           Student.fullname,
                           Teacher.fullname) \
        .select_from(Grade).join(Disciplines).join(Teacher).join(Student) \
        .filter(and_(student_id == Grade.student_id,
                     teacher_id == Disciplines.teacher_id)) \
        .group_by(Student.fullname, Disciplines.name, Teacher.fullname).all()
    return result


def select_eleven(teacher_id: int, student_id: id):
    """Середній бал, який певний викладач ставить певному студентові.
    :return list(tuple)"""
    result = session.query(Student.fullname,
                           Teacher.fullname,
                           func.round(func.avg(Grade.grade),
                                      2).label('avg_grade')) \
        .select_from(Grade).join(Disciplines).join(Teacher).join(Student) \
        .filter(and_(teacher_id == Disciplines.teacher_id,
                     Grade.student_id == student_id)) \
        .group_by(Student.fullname, Teacher.fullname).all()

    return result


def select_twelve(group_id: int, discipline_id: int):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""

    date_of_last_lesson_row = session.query(Grade.date_of).select_from(Grade) \
        .join(Disciplines).join(Student).join(Group) \
        .filter(and_(Grade.disciplines_id == discipline_id, Student.group_id == group_id)) \
        .group_by(Grade.date_of, Disciplines.id).order_by(desc(Grade.date_of)).first()

    for d in date_of_last_lesson_row:
        date_of_last_lesson = d

    result = session.query(Student.fullname, Group.name, Disciplines.name, Grade.date_of) \
        .select_from(Grade).join(Disciplines).join(Student).join(Group) \
        .filter(and_(Grade.disciplines_id == discipline_id,
                     Student.group_id == group_id, Grade.date_of == date_of_last_lesson)) \
        .group_by(Student.fullname, Group.name, Disciplines.name, Grade.date_of).order_by(desc(Grade.date_of)).all()

    return result


if __name__ == '__main__':
    print(select_one())
    print(select_two(randint(1, 5)))
    print(select_three(randint(1, 5)))
    print(f'Average grade for all groups: {select_four()}')
    print(f'result:{select_five(randint(1, 5))}')
    print(select_six(randint(1, 3)))
    print(select_seven(group_id=randint(1, 3), discipline_id=randint(1, 5)))
    print(select_eight(randint(1, 5)))
    print(select_nine(randint(1, 50)))
    print(select_ten(randint(1, 50), randint(1, 5)))
    print(select_eleven(randint(1, 5), randint(1, 50)))
    print(select_twelve(randint(1, 3), randint(1, 5)))
