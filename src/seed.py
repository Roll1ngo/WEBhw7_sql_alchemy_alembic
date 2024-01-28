from datetime import date, datetime, timedelta
from random import randint, choice

from faker import Faker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from db import session
from models import Disciplines, Teacher, Student, Grade, Group

fake = Faker('Uk-ua')

number_of_teachers = 5
number_of_students = 50
groups = ['G1', 'G2', 'G3']
dicsiplines = ['Креслення',
               'Вища математика',
               'Теорія ймовірності',
               'Філософія',
               'Інформатика'
               ]



def seed_teachers():
    for _ in range(number_of_teachers):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)


def seed_groups():
    for group in groups:
        cr_gr = Group(name=group)
        session.add(cr_gr)


def seed_students():
    select_groups = session.query(Group).all()
    for _ in range(number_of_students):
        student = Student(fullname=fake.name(),
                          group_id=choice(select_groups).id)
        session.add(student)


def seed_disciplines():
    select_teachers = list(session.query(Teacher.id).all())
    teach_id_list = [id for id_ in select_teachers for id in id_]

    for d in dicsiplines:
        random_teacher_id = choice(teach_id_list)
        dicsipline = Disciplines(name=d, teacher_id=random_teacher_id)
        teach_id_list.remove(random_teacher_id)
        session.add(dicsipline)


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(days=1)
    return result


def seed_grades():
    start_curs = datetime.strptime('2023-05-15', '%Y-%m-%d')
    finish_curs = datetime.strptime('2024-04-12', '%Y-%m-%d')
    date_r = date_range(start_curs, finish_curs)
    dicsipline_ids_taple = session.execute(select(Disciplines.id)).all()
    dicsipline_ids = [dic for dic_ in dicsipline_ids_taple for dic in dic_]
    student_ids_taple = session.execute(select(Student.id)).all()
    student_ids = [st for st_ in student_ids_taple for st in st_]

    for d in date_r:
        random_dicsiplines_id = choice(dicsipline_ids)
        random_ids_student = [choice(student_ids) for _ in range(5)]

        for st_id in random_ids_student:
            grade_ = Grade(
                grade=randint(4, 12),
                date_of=d.date(),
                student_id=st_id,
                disciplines_id=random_dicsiplines_id
            )
            session.add(grade_)


if __name__ == '__main__':
    try:
        seed_teachers()
        seed_groups()
        seed_students()
        seed_disciplines()
        seed_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
