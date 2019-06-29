from django.contrib import admin

from .models import (
    StudyCategory,
    Study,
    StudyMember,
    Schedule,
    Attendance,
)

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1


@admin.register(StudyCategory)
class StudyCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    list_filter = ('category',)
    inlines = [
        ScheduleInline,
    ]


@admin.register(StudyMember)
class StudyMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'study', 'role')
    list_filter = ('study',)
    search_fields = ('user', 'study')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('study', 'location', 'date', 'due_date',)
    list_filter = ('study',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'schedule', 'vote', 'att')
    list_filter = ('schedule',)
    search_fields = ('user', 'schedule')
