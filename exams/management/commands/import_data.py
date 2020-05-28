import pandas as pd
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from exams.models import SchoolClass, Student


class Command(BaseCommand):
    help = "Imports student and class data from a .xlsx file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs=1, type=str)

    def handle(self, *args, **options):
        file_path = options['file_path'][0]

        def define_base_number(name):
            if name == 'هفتم':
                return '7'
            if name == 'هشتم':
                return '8'
            if name == 'نهم':
                return '9'
            return '0'

        df = pd.read_excel(file_path,
                           names=['base', 'branch', 'class', 'first_name', 'last_name', 'father_name', 'national_code'])
        df['base_code'] = df['base'].apply(define_base_number)
        df['class'] = df['class'].apply(str)
        df['class_code'] = df['base_code'] + '0' + df['class']

        classes = df.copy().drop_duplicates(subset=['class_code'])

        self.stdout.write('delete all previous data')
        SchoolClass.objects.all().delete()
        Student.objects.all().delete()

        self.stdout.write('add all new data')
        for clazz in classes.iterrows():
            clazz = clazz[1]
            school_class = SchoolClass(
                code=clazz['class_code'],
                name=f'{clazz["base"]} {clazz["class"]}',
            )
            school_class.save()
            class_students = df[df['class_code'] == clazz['class_code']].copy()
            for student in class_students.iterrows():
                student = student[1]
                user = User(
                    username=student['national_code'],
                    password=student['national_code'],
                )
                user.save()

                student = Student(
                    user=user,
                    school_class=school_class,
                    first_name=student['first_name'],
                    last_name=student['last_name'],
                )
                student.save()

        self.stdout.write('done')
