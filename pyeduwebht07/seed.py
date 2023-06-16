import datetime
import logging
from db.connection import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import *
import faker.providers
from faker import Faker
from random import randint, choice, choices


# custom providers for Faker
groups_provider = faker.providers.DynamicProvider(
    provider_name="edu_groups_shortcuts",
    elements=[f"{''.join(choices([chr(c) for c in range(ord('К'), ord('Ш'))], k=randint(2,3)))}-"
              f"{choice(range(18, 23))}" for _ in range(3)]
)

subjects_provider = faker.providers.DynamicProvider(
    provider_name="edu_subjects",
    elements=["Вища математика", "Українська мова", "Архітектура",
              "Програмування", "Бази даних", "Філософія",
              "Економіка", "Технології виробництва"]
)


def add_students(fake):
    with Session(engine) as session:
        groups_ids = get_all_ids(Group, session)
        for _ in range(randint(30, 50)):
            student = Student()
            student.first_name = fake.first_name()
            student.last_name = fake.last_name()

            student.group_id = choice(groups_ids)

            session.add(student)

        session.commit()

    logging.info("Students added.")


def add_groups(fake):
    fake.add_provider(groups_provider)

    with Session(engine) as session:
        for _ in range(3):
            group = Group(name=fake.unique.edu_groups_shortcuts())
            session.add(group)

        session.commit()

    logging.info("Groups added.")


def add_teachers(fake):
    with Session(engine) as session:
        for _ in range(randint(3, 5)):
            teacher = Teacher()
            teacher.first_name = fake.first_name()
            teacher.last_name = fake.last_name()

            session.add(teacher)

        session.commit()

    logging.info("Teachers added.")


def get_all_ids(model: Base, session: Session):
    statement = select(model.id)
    ids = [i[0] for i in session.execute(statement).all()]
    return ids


def add_subjects(fake):
    fake.add_provider(subjects_provider)

    with Session(engine) as session:
        teachers_ids = get_all_ids(Teacher, session)
        for _ in range(randint(5, 8)):
            subject = Subject()
            subject.name = fake.unique.edu_subjects()

            subject.teacher_id = choice(teachers_ids)

            session.add(subject)

        session.commit()

    logging.info("Subjects added.")


def add_grades(fake):
    with Session(engine) as session:
        students_ids = get_all_ids(Student, session)
        subjects_ids = get_all_ids(Subject, session)
        date_range = datetime.date(2018, 9, 1), datetime.date(2023, 6, 1)

        for student_id in students_ids:
            for _ in range(randint(15, 20)):
                grade = Grade()
                grade.got_at = fake.date_time_between_dates(*date_range)
                grade.mark = randint(2, 5)
                grade.student_id = student_id
                grade.subject_id = choice(subjects_ids)

                session.add(grade)

        session.commit()

    logging.info("Subjects added.")


def seed_data():
    Faker.seed(0)
    fake = Faker(locale="uk_UA")
    fake.seed_instance(0)
    fake.add_provider(subjects_provider)

    for func in (add_groups, add_students, add_teachers, add_subjects, add_grades):
        func(fake)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_data()
