from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, permissions

from .filters import (
    ScheduleFilter,
    StudyMembershipListFilter,
    AttendanceFilter)
from .models import (
    StudyCategory,
    Study,
    StudyMembership,
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
    StudyDetailSerializer,
    StudyMemberDetailSerializer,
    AttendanceDetailSerializer,
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
        study = serializer.save(author=self.request.user)
        # Study생성시 해당 유저가 관리자인 StudyMember생성
        StudyMembership.objects.update_or_create(
            user=self.request.user,
            study=study,
            defaults={
                'role': StudyMembership.ROLE_MAIN_MANAGER,
            }
        )

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
        return StudyDetailSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)


STUDY_MEMBER_LIST_DESCRIPTION = '''
스터디멤버십 목록
'''


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='StudyMembership List',
        operation_description=STUDY_MEMBER_LIST_DESCRIPTION,
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='StudyMembership Create',
        operation_description='스터디멤버십 생성',
        responses={
            status.HTTP_200_OK: StudyMemberDetailSerializer(),
        }
    )
)
class StudyMembershipListCreateAPIView(generics.ListCreateAPIView):
    queryset = StudyMembership.objects.all()
    filterset_class = StudyMembershipListFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudyMemberCreateSerializer
        return StudyMemberSerializer

    def perform_create(self, serializer):
        instance = serializer.save()


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='StudyMembership Retrieve',
        operation_description='스터디멤버십 정보'
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_summary='StudyMembership Update',
        operation_description='스터디멤버십 정보 수정',
        responses={
            status.HTTP_200_OK: StudyMemberSerializer(),
        },
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_summary='StudyMembership Withdraw',
        operation_description='스터디멤버십 탈퇴',
    ),
)
class StudyMembershipRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyMembership.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return StudyMemberUpdateSerializer
        return StudyMemberDetailSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.withdraw()


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
    queryset = Schedule.objects.all()
    filterset_class = ScheduleFilter

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
    queryset = Schedule.objects.all()

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
    queryset = Attendance.objects.all()
    filterset_class = AttendanceFilter

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
    queryset = Attendance.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return AttendanceUpdateSerializer
        return AttendanceDetailSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)
