from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404

from .models import (
    StudyCategory,
    Study,
    StudyMember,
    Schedule,
    Attendance,
)
from .serializers import (
    StudyCategorySerializer,
    StudySerializer,
    StudyCreateSerializer,
    StudyUpdateSerializer,
    StudyMemberSerializer,
    StudyMemberCreateSerializer,
    StudyMemberUpdateSerializer,
    ScheduleSerializer,
    ScheduleCreateSerializer,
    ScheduleUpdateSerializer,
    AttendanceSerializer,
    AttendanceCreateSerializer,
    AttendanceUpdateSerializer,
)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='StudyCategory List',
        operation_description='스터디 카테고리 목록'
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='StudyCategory Create',
        operation_description='스터디 카테고리 생성',
        responses={
            status.HTTP_200_OK: StudyCategorySerializer(),
        }
    )
)
class StudyCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = StudyCategory.objects.all()
    serializer_class = StudyCategorySerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Study List',
        operation_description='스터디 목록'
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='Study Create',
        operation_description='스터디 생성',
        responses={
            status.HTTP_200_OK: StudyCategorySerializer(),
        }
    )
)
class StudyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Study.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudyCreateSerializer
        return StudySerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Study Retrieve',
        operation_description='스터디 정보'
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_summary='Study Update',
        operation_description='스터디 정보 수정',
        responses={
            status.HTTP_200_OK: StudySerializer(),
        },
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_summary='Study Delete',
        operation_description='스터디 삭제',
    ),
)
class StudyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Study.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return StudyUpdateSerializer
        return StudySerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='StudyMember List',
        operation_description='스터디멤버 목록'
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='StudyMember Create',
        operation_description='스터디멤버 생성',
        responses={
            status.HTTP_200_OK: StudyMemberSerializer(),
        }
    )
)
class StudyMemberListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        study = get_object_or_404(Study, pk=self.kwargs.get('study_pk'))
        return StudyMember.objects.filter(study=study)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudyMemberCreateSerializer
        return StudyMemberSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='StudyMember Retrieve',
        operation_description='스터디멤버 정보'
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_summary='StudyMember Update',
        operation_description='스터디멤버 정보 수정',
        responses={
            status.HTTP_200_OK: StudyMemberSerializer(),
        },
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_summary='StudyMember Delete',
        operation_description='스터디멤버 삭제',
    ),
)
class StudyMemberRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        study = get_object_or_404(Study, pk=self.kwargs.get('study_pk'))
        return StudyMember.objects.filter(study=study)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return StudyMemberUpdateSerializer
        return StudySerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Schedule List',
        operation_description='스터디 일정 목록'
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='Schedule Create',
        operation_description='스터디 일정 생성',
        responses={
            status.HTTP_200_OK: ScheduleSerializer(),
        }
    )
)
class ScheduleListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        study = get_object_or_404(Study, pk=self.kwargs.get('study_pk'))
        return Schedule.objects.filter(study=study)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ScheduleCreateSerializer
        return ScheduleSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Schedule Retrieve',
        operation_description='스터디 일정 정보'
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_summary='Schedule Update',
        operation_description='스터디 일정 수정',
        responses={
            status.HTTP_200_OK: ScheduleSerializer(),
        },
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_summary='Schedule Delete',
        operation_description='스터디 일정 삭제',
    ),
)
class ScheduleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        study = get_object_or_404(Study, pk=self.kwargs.get('study_pk'))
        return Schedule.objects.filter(study=study)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ScheduleUpdateSerializer
        return ScheduleSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Attendance List',
        operation_description='스터디 참여내역 목록'
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='Attendance Create',
        operation_description='스터디 참여내역 생성',
        responses={
            status.HTTP_200_OK: AttendanceSerializer(),
        }
    )
)
class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        study = get_object_or_404(Study, pk=self.kwargs.get('study_pk'))
        return Attendance.objects.filter(study=study)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AttendanceCreateSerializer
        return AttendanceSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Attendance Retrieve',
        operation_description='스터디 참여내역 정보'
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_summary='Attendance Update',
        operation_description='스터디 참여내역 수정',
        responses={
            status.HTTP_200_OK: AttendanceSerializer(),
        },
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_summary='Attendance Delete',
        operation_description='스터디 참여내역 삭제',
    ),
)
class AttendanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        study = get_object_or_404(Study, pk=self.kwargs.get('study_pk'))
        return Attendance.objects.filter(study=study)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return AttendanceUpdateSerializer
        return AttendanceSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)
