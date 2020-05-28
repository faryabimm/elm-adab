from django.contrib.auth.models import User
from django.db import models


class SchoolClass(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='کد کلاس')
    name = models.CharField(max_length=50, verbose_name='نام کلاس')

    def __str__(self):
        return f'{self.name}({self.code})'

    class Meta:
        verbose_name = 'کلاس درس'
        verbose_name_plural = 'کلاس‌های درس'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', verbose_name='کاربر')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, verbose_name='کلاس درس')
    # username is national-id
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')

    def __str__(self):
        return f'{self.first_name} {self.last_name}({self.user.username})'

    class Meta:
        verbose_name = 'دانش‌آموز'
        verbose_name_plural = 'دانش‌آموزان'


class Exam(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام آزمون')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, verbose_name='کلاس درس')
    code = models.CharField(max_length=20, unique=True, verbose_name='کد آزمون')
    duration = models.DurationField(verbose_name='مدت زمان آزمون')
    start_time = models.DateTimeField(verbose_name='تاریخ و ساعت شروع')
    valid_submission_extensions = models.CharField(max_length=50, blank=True, verbose_name='فرمت‌های مجاز فایل جواب')
    question_file_path = models.FileField(upload_to='exam_files', verbose_name='فایل صورت آزمون')

    def __str__(self):
        return f'{self.name}({self.code})'

    class Meta:
        verbose_name = 'آزمون'
        verbose_name_plural = 'آزمون‌ها'


class ExamSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='دانش‌آموز')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='آزمون')
    time = models.DateTimeField(verbose_name='تاریخ و زمان ارسال')
    answer_file = models.FileField(upload_to='submission_files', verbose_name='فایل پاسخ')

    class Meta:
        verbose_name = 'پاسخ ارسالی'
        verbose_name_plural = 'پاسخ‌های ارسالی'
