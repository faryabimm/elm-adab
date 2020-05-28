from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render
from django.utils import timezone

from . import forms
from .models import Exam, ExamSubmission


def handle_valid_submission(request, form):
    print('test')
    in_mem_file = form.cleaned_data['file']
    exam = Exam.objects.get(id=form.cleaned_data['exam_id'])
    extension = in_mem_file.name.split('.')[-1]
    in_mem_file.name = f'/EX_{exam.code}_STD_{request.user.username}.{extension}'

    ExamSubmission(
        student=request.user.student,
        exam=exam,
        time=timezone.now(),
        answer_file=in_mem_file
    ).save()

    return render(request, 'exam/message.html', context={
        'color': 'green',
        'icon': 'clipboard check',
        'header': 'پاسخ ارسال شد',
        'message': f'پاسخ شما به آزمون «اسم آزمون» با موفقیت ارسال شد.',
    })


@login_required
def message(request):
    return render(request, 'exam/message.html', context={
        'color': 'green',
        'icon': 'smile',
        'header': 'پیغام تست',
        'message': 'این پیغام تستی‌ است.',
    })


@login_required
def azmoon(request):
    class_exams = Exam.objects.filter(
        school_class=request.user.student.school_class,
        start_time__gt=timezone.now() - F('duration')
    )

    if len(class_exams) == 0:
        return render(request, 'exam/message.html', context={
            'color': 'green',
            'icon': 'smile',
            'header': 'آزمونی وجود ندارد',
            'message': 'فعلا آزمونی برای شما در سیستم تعریف نشده‌است.',
        })

    if len(class_exams) > 1:
        raise Exception('More than one exam')

    exam = class_exams.get()
    submissions = ExamSubmission.objects.filter(exam=exam, student=request.user.student)

    if len(submissions) > 1:
        raise Exception('More than one submission')

    if len(submissions) == 1:
        return render(request, 'exam/message.html', context={
            'color': 'green',
            'icon': 'clipboard check',
            'header': 'پاسخ دریافت شده',
            'message': f'شما قبلا به آزمون «{exam.name}» پاسخ‌داده‌اید.',
        })

    if exam.start_time > timezone.now():
        delta = exam.start_time - timezone.now()
        return render(request, 'exam/message.html', context={
            'color': 'blue',
            'icon': 'clock outline',
            'header': 'آزمون شروع نشده',
            'message': f'آزمون «{exam.name}» در {str(delta).split(".")[0]} دیگر شروع خواهد شد.',
        })

    if request.method == 'POST':
        form = forms.ExamSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            return handle_valid_submission(request, form)
    else:
        return render(request, 'exam/exam.html', context={
            'form': forms.ExamSubmissionForm(initial={
                'exam_id': exam.id,
            }),
            'exam': exam,
            'server_timestamp': timezone.now().timestamp(),
            'end_timestamp': exam.start_time.timestamp() + exam.duration.seconds,
            'user': request.user,
        })
