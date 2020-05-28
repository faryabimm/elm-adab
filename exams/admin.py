from django.contrib import admin
from django.db.models.fields.reverse_related import ManyToOneRel

from .models import SchoolClass, Student, Exam, ExamSubmission

for model in [
    SchoolClass, Student, Exam, ExamSubmission
]:
    class ModelAdmin(admin.ModelAdmin):
        list_display = [x.name for x in model._meta.get_fields(False, False) if type(x) not in (ManyToOneRel,)]


    admin.site.register(model, ModelAdmin)
