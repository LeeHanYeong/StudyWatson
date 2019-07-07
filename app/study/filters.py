from django_filters import rest_framework as filters
from .models import StudyMember


class StudyMemberListFilter(filters.FilterSet):
    user = filters.NumberFilter(help_text='User의 pk(id)')
    study = filters.NumberFilter(help_text='Study의 pk(id)')

    class Meta:
        model = StudyMember
        fields = (
            'user',
            'study',
        )
