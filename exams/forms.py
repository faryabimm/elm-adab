from django import forms


class ExamSubmissionForm(forms.Form):
    file = forms.FileField(label='فایل پاسخ', required=True)
    exam_id = forms.IntegerField(widget=forms.HiddenInput, required=True)
