from django.contrib import admin

from .models import (
    StudyCategory,
    StudyIcon,
    Study,
    StudyMembership,
    Schedule,
    Attendance,
)


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1


@admin.register(StudyCategory)
class StudyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')


@admin.register(StudyIcon)
class StudyIconAdmin(admin.ModelAdmin):
    pass


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'author', 'pk')
    list_filter = ('category',)
    inlines = [
        ScheduleInline,
    ]


@admin.register(StudyMembership)
class StudyMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'study', 'role', 'pk')
    list_filter = ('study',)
    search_fields = ('user', 'study')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('study', 'location', 'vote_end_at', 'start_at', 'studying_time', 'pk')
    list_filter = ('study',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'schedule', 'vote', 'att', 'pk')
    list_filter = ('schedule',)
    search_fields = ('user', 'schedule')
