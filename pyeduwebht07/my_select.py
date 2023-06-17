import builtins
from sqlalchemy import func, desc, label, select, distinct
from sqlalchemy.sql.sqltypes import Date
from db.connection import session
from db.models import *


skip = "(Ctrl+C to terminate.): "


def input(prompt):
    return builtins.input(f"{prompt.rstrip()[:-1]} {skip}")


def select_1():
    """01. Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""

    result = session.query(
        label('student_id', Student.id),
        label('student', Student.full_name),
        label('group', Group.name),
        label('avg_mark', func.round(func.avg(Grade.mark), 2))
    ).\
        select_from(Grade).join(Student).join(Group).\
        group_by(Student.id, Group.name).\
        order_by(desc('avg_mark')).\
        limit(5)

    return [cd["name"] for cd in result.column_descriptions], result.all()


def select_2():
    """02. Знайти студента із найвищим середнім балом з певного предмету."""

    subquery_a = select(
        Student.id,
        label('student', Student.full_name),
        label('group', Group.name),
        label('subject', Subject.name),
        label('subject_id', Subject.id),
        label('avg_mark', func.round(func.avg(Grade.mark), 2))
    ).\
        select_from(Grade).join(Student).join(Subject).join(Group).\
        group_by(Student.id, Subject.id, Group.name).subquery()

    subquery_b = select(
        subquery_a.c.subject_id,
        label('max_avg', func.max(subquery_a.c.avg_mark))
    ).\
        select_from(subquery_a).\
        group_by(subquery_a.c.subject_id).subquery()

    result = session.query(
        label('student_id', subquery_a.c.id),
        subquery_a.c.student,
        subquery_a.c.group,
        subquery_a.c.subject,
        subquery_a.c.avg_mark
    ).\
        select_from(subquery_a).\
        join(subquery_b, (subquery_a.c.subject_id == subquery_b.c.subject_id)
             & (subquery_a.c.avg_mark == subquery_b.c.max_avg)).\
        order_by(subquery_a.c.subject_id, 'student_id')

    return [cd["name"] for cd in result.column_descriptions], result.all()


def select_3():
    """03. Знайти середній бал у групах з певного предмета."""

    result = session.query(
        label('group', Group.name),
        label('subject', Subject.name),
        label('avg_mark', func.round(func.avg(Grade.mark), 2))
    ).\
        select_from(Grade).join(Student).join(Subject).join(Group).\
        group_by(Group.id, Subject.id).\
        order_by(Group.name, Subject.name)

    return [cd["name"] for cd in result.column_descriptions], result.all()


def select_4():
    """04. Знайти середній бал на потоці (по всій таблиці оцінок)."""

    result = session.query(
        label('avg_mark', func.round(func.avg(Grade.mark), 2))
    ). \
        select_from(Grade)

    return [cd["name"] for cd in result.column_descriptions], result.all()


def select_5():
    """05. Знайти, які курси читає певний викладач."""

    teachers = session.query(Teacher.id, Teacher.full_name).all()
    print("List of teachers:")
    for teacher in teachers:
        print(f'{teacher[0]}:', teacher[1])

    try:
        t_id = int(input("Enter id of a teacher: "))
    except ValueError:
        print("Bad id!")
    except (KeyboardInterrupt, EOFError):
        print("\nSkipped!")
    else:
        result = session.query(
            label('teacher_id', Teacher.id),
            label('teacher', Teacher.full_name),
            label('subjects', func.string_agg(Subject.name, ', ')),
        ).\
            select_from(Teacher).join(Subject).\
            where(Teacher.id == t_id).\
            group_by(Teacher.id)

        return [cd["name"] for cd in result.column_descriptions], result.all()


def select_6():
    """06. Знайти список студентів у певній групі."""

    groups = session.query(Group.id, Group.name).all()
    print("List of groups:")
    for group in groups:
        print(f'{group[0]}:', group[1])

    try:
        g_id = int(input("Enter id of a group: "))
    except ValueError:
        print("Bad id!")
    except (KeyboardInterrupt, EOFError):
        print("\nSkipped!")
    else:
        result = session.query(
            label('group', Group.name),
            label('student', Student.full_name),
        ). \
            select_from(Student).join(Group). \
            where(Group.id == g_id)

        return [cd["name"] for cd in result.column_descriptions], result.all()


def select_7():
    """07. Знайти оцінки студентів в окремій групі з певного предмета."""

    groups = session.query(Group.id, Group.name).all()
    subjects = session.query(Subject.id, Subject.name).all()

    print("List of groups:")
    for group in groups:
        print(f'{group[0]}:', group[1])

    print("List of subjects:")
    for subject in subjects:
        print(f'{subject[0]}:', subject[1])

    try:
        g_id = int(input("Enter id of a group: "))
        sbj_id = int(input("Enter id of a subject: "))
    except ValueError:
        print("Bad id!")
    except (KeyboardInterrupt, EOFError):
        print("\nSkipped!")
    else:
        result = session.query(
            label('student', Student.full_name),
            label('group', Group.name),
            label('subject', Subject.name),
            Grade.mark,
            label('date', Grade.got_at)
        ). \
            select_from(Grade).join(Student).join(Subject).join(Group). \
            where((Group.id == g_id) & (Subject.id == sbj_id))

        return [cd["name"] for cd in result.column_descriptions], result.all()


def select_8():
    """08. Знайти середній бал, який ставить певний викладач зі своїх предметів."""

    teachers = session.query(Teacher.id, Teacher.full_name).all()
    print("List of teachers:")
    for teacher in teachers:
        print(f'{teacher[0]}:', teacher[1])

    try:
        t_id = int(input("Enter id of a teacher: "))
    except ValueError:
        print("Bad id!")
    except (KeyboardInterrupt, EOFError):
        print("\nSkipped!")
    else:
        result = session.query(
            label('teacher', Teacher.full_name),
            label('subject', Subject.name),
            label('avg_mark', func.round(func.avg(Grade.mark), 2))
        ). \
            select_from(Grade).join(Subject).join(Teacher). \
            where(Teacher.id == t_id). \
            group_by(Subject.id, Teacher.id)

        return [cd["name"] for cd in result.column_descriptions], result.all()


def select_9():
    """09. Знайти список курсів, які відвідує студент."""

    result = session.query(
        label('student_id', Student.id),
        label('student', Student.full_name),
        label('subjects', func.string_agg(distinct(Subject.name), ', ')),
    ). \
        select_from(Student).join(Grade).join(Subject). \
        group_by(Student.id)

    return [cd["name"] for cd in result.column_descriptions], result.all()


def select_10():
    """10. Список курсів, які певному студенту читає певний викладач."""

    students = session.query(Student.id, Student.full_name).all()
    teachers = session.query(Teacher.id, Teacher.full_name).all()

    print("List of students:")
    for student in students:
        print(f'{student[0]}:', student[1])

    print("List of teachers:")
    for teacher in teachers:
        print(f'{teacher[0]}:', teacher[1])

    try:
        st_id = int(input("Enter id of a student: "))
        t_id = int(input("Enter id of a teacher: "))
    except ValueError:
        print("Bad id!")
    except (KeyboardInterrupt, EOFError):
        print("\nSkipped!")
    else:
        result = session.query(
            label('student', Student.full_name),
            label('teacher', Teacher.full_name),
            label('subjects', func.string_agg(distinct(Subject.name), ', ')),
        ). \
            select_from(Student).join(Grade).join(Subject).join(Teacher). \
            where((Student.id == st_id) & (Teacher.id == t_id)).\
            group_by(Student.id, Teacher.id)

        return [cd["name"] for cd in result.column_descriptions], result.all()


def select_11():
    """11(*). Середній бал, який певний викладач ставить певному студентові."""

    students = session.query(Student.id, Student.full_name).all()
    teachers = session.query(Teacher.id, Teacher.full_name).all()

    print("List of students:")
    for student in students:
        print(f'{student[0]}:', student[1])

    print("List of teachers:")
    for teacher in teachers:
        print(f'{teacher[0]}:', teacher[1])

    try:
        st_id = int(input("Enter id of a student: "))
        t_id = int(input("Enter id of a teacher: "))
    except ValueError:
        print("Bad id!")
    except (KeyboardInterrupt, EOFError):
        print("\nSkipped!")
    else:
        result = session.query(
            label('teacher', Teacher.full_name),
            label('student', Student.full_name),
            label('subjects', func.round(func.avg(Grade.mark), 2)),
        ). \
            select_from(Grade).join(Student).join(Subject).join(Teacher). \
            where((Student.id == st_id) & (Teacher.id == t_id)). \
            group_by(Student.id, Teacher.id)

        return [cd["name"] for cd in result.column_descriptions], result.all()


def select_12():
    """12(*). Оцінки студентів у певній групі з певного предмета на останньому занятті."""

    groups = session.query(Group.id, Group.name).all()
    subjects = session.query(Subject.id, Subject.name).all()

    print("List of groups:")
    for group in groups:
        print(f'{group[0]}:', group[1])

    print("List of subjects:")
    for subject in subjects:
        print(f'{subject[0]}:', subject[1])

    try:
        gr_id = int(input("Enter id of a group: "))
        sbj_id = int(input("Enter id of a subject: "))
    except ValueError:
        print("Bad id!")
    except (KeyboardInterrupt, EOFError):
        print("\nSkipped!")
    else:
        subquery = select(func.max(Grade.got_at).cast(Date)).\
            select_from(Grade).\
            where(Grade.subject_id == sbj_id).scalar_subquery()

        result = session.query(
            label('group', Group.name),
            label('student', Student.full_name),
            Grade.mark,
            Grade.got_at
        ). \
            select_from(Grade).join(Student).join(Group).join(Subject). \
            where((Subject.id == sbj_id) & (Group.id == gr_id)
                  & (Grade.got_at.cast(Date) == subquery)). \
            group_by(Group.id, Grade.id, Student.id)

        return [cd["name"] for cd in result.column_descriptions], result.all()
