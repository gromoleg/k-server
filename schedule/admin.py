from django.contrib import admin
from .models import Faculty, Group, Degree, Teacher, Classroom, Class


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'faculty_id', 'degree_id', 'name')


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'middle_name')


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'faculty_id', 'name')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'num', 'week', 'day', 'start', 'end', 'name', 'type')
