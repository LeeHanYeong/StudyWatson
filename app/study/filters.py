from django_filters import rest_framework as filters
from .models import Schedule, StudyMember


class ScheduleFilter(filters.FilterSet):
    class Meta:
        model = Schedule
        fields = (
            'study',
        )


class StudyMemberListFilter(filters.FilterSet):
    user = filters.NumberFilter(help_text='User의 pk(id)')
    study = filters.NumberFilter(help_text='Study의 pk(id)')

    class Meta:
        model = StudyMember
        fields = (
            'user',
            'study',
        )
