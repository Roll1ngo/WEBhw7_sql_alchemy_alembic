from random import randint

from sqlalchemy import func, desc, and_
from rich import print


from src.db import session
from src.models import Teacher, Group, Student, Disciplines, Grade


def select_one():
    '''Select_one: Знайти 5 студентів із найбільшим середнім балом\
    з усіх предметів. :return list[tuple]'''

    result = session.query(
        Student.fullname, func.round(func.avg(Grade.grade), 2)
        .label('avg_grade')).select_from(Grade).join(Student)\
        .group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

    return result


def select_two(discipline_id):
    '''Знайти студента із найвищим середнім балом з певного предмета.\
        :return list[tuple]'''

    result = session.query(Disciplines.name,
                           Student.fullname,
                           func.round(func.avg(Grade.grade),
                                      2).label('avg_grade'))\
        .select_from(Grade).join(Student).join(Disciplines)\
        .filter(Disciplines.id == discipline_id)\
        .group_by(Student.id, Disciplines.name)\
        .order_by(desc('avg_grade'))\
        .limit(1).all()

    return result


def select_three(discipline_id: int):
    '''Знайти середній бал у групах з певного предмета.\
        :return list[tuple]'''

    result = session.query(Group.name,
                           Disciplines.name,
                           func.round(func.avg(Grade.grade),
                                      2).label('avg_grade'))\
        .select_from(Grade).join(Student).join(Group).join(Disciplines)\
        .filter(Disciplines.id == discipline_id)\
        .group_by(Group.name, Disciplines.name)\
        .order_by(desc('avg_grade')).all()

    return result


def select_four():
    '''Знайти середній бал на потоці (по всій таблиці оцінок).\
        :return list(tuple)'''

    result = session.query(func.round(func.avg(Grade.grade), 2)
                           .label('avg_grade')).select_from(Grade).all()

    return result


def select_five(teacher_id: str):
    '''Знайти які курси читає певний викладач.\
        :return list(tuple)'''

    result = session.query(Disciplines.name, Teacher.fullname)\
        .select_from(Grade).join(Disciplines).join(Teacher)\
        .filter(Disciplines.teacher_id == teacher_id).limit(1).all()

    return result


def select_six(group_id: int):
    '''Знайти список студентів у певній групі.\
        :return list(tuple)'''

    result = session.query(Group.name, Student.fullname)\
        .select_from(Student).join(Group)\
        .filter(group_id == Student.group_id).all()

    return result


def select_seven(group_id, discipline_id):
    '''Знайти оцінки студентів у окремій групі з певного предмета.\
        :return list(tuple)'''

    result = session.query(Grade.grade, Student.fullname,
                           Group.name, Disciplines.name)\
        .select_from(Grade).join(Disciplines).join(Student).join(Group)\
        .filter(and_(discipline_id == Grade.disciplines_id,
                     group_id == Student.group_id))\
        .group_by(Student.fullname,
                  Grade.grade,
                  Group.name,
                  Disciplines.name).order_by(desc(Grade.grade))\
        .limit(10).all()

    return result


def select_eight(teacher_id):
    '''Знайти середній бал, який ставить певний викладач зі своїх предметів.\
        :return list(tuple)'''

    result = session.query(Teacher.fullname,
                           Disciplines.name,
                           func.round(func.avg(Grade.grade),
                                      2).label('avg_grade')
                           ).select_from(Grade)\
        .join(Disciplines).join(Teacher)\
        .filter(teacher_id == Disciplines.teacher_id)\
        .group_by(Teacher.fullname, Disciplines.name).all()

    return result


def select_nine(student_id: int):
    '''Знайти список курсів, які відвідує певний студент.\
        :return list(tuple)'''

    result = session.query(Student.fullname, Disciplines.name)\
        .select_from(Grade). filter(student_id == Student.id)\
        .group_by(Disciplines.name, Student.fullname).all()

    return result


def select_ten(student_id: int, teacher_id: int):
    '''Список курсів, які певному студенту читає певний викладач.\
        :return list(tuple)'''

    result = session.query(Disciplines.name,
                           Student.fullname,
                           Teacher.fullname)\
        .select_from(Grade).join(Disciplines).join(Teacher)\
        .filter(and_(student_id == Student.id,
                     teacher_id == Teacher.id))\
        .group_by(Student.fullname, Disciplines.name, Teacher.fullname).all()
    return result


def select_eleven(teacher_id: int, student_id: id):
    '''Середній бал, який певний викладач ставить певному студентові.
    :return list(tuple)'''
    result = session.query(Student.fullname,
                           Teacher.fullname,
                           func.round(func.avg(Grade.grade),
                                      2).label('avg_grade'))\
        .select_from(Grade).join(Disciplines).join(Teacher)\
        .filter(and_(teacher_id == Disciplines.teacher_id,
                     Student.id == student_id))\
        .group_by(Student.fullname, Teacher.fullname).all()

    return result


if __name__ == '__main__':
    '''
    # print(select_one)
    # print(select_two(randint(7, 11)))
    # print(select_three(randint(7, 11)))
    # print(f'Average grade for all groups: {select_four()}')
    # print(f'result:{select_five(randint(1, 5))}')
    print(select_six(randint(3, 5)))
    print(select_seven(group_id=randint(3, 5), discipline_id=randint(7, 11)))
    print(select_eight(randint(1, 5)))
    print(select_nine(randint(1,50)))
    print(select_ten(randint(1, 50), randint(1, 5)))
    print(select_eleven(randint(1, 5), randint(1, 50)))'''
    print(select_eleven(randint(1, 5), randint(1, 50)))
