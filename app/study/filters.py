from django_filters import rest_framework as filters

from .models import Schedule, StudyMembership, Attendance


class ScheduleFilter(filters.FilterSet):
    class Meta:
        model = Schedule
        fields = (
            'study',
        )


class StudyMembershipListFilter(filters.FilterSet):
    user = filters.NumberFilter(help_text='User의 pk(id)')
    study = filters.NumberFilter(help_text='Study의 pk(id)')

    class Meta:
        model = StudyMembership
        fields = (
            'is_withdraw',
            'user',
            'study',
        )


class AttendanceFilter(filters.FilterSet):
    class Meta:
        model = Attendance
        fields = (
            'user',
            'schedule',
            'vote',
            'att',
        )
