from django.db.models import Prefetch, Subquery, OuterRef
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404

from utils.drf import errors
from utils.drf.exceptions import ValidationError
from .filters import (
    ScheduleFilter,
    StudyMembershipListFilter,
    AttendanceFilter,
)
from .models import (
    StudyCategory,
    StudyIcon,
    Study,
    StudyMembership,
    Schedule,
    Attendance,
    StudyInviteToken,
)
from .serializers import (
    StudyCategorySerializer,
    StudyIconSerializer,
    StudySerializer,
    StudyCreateSerializer,
    StudyDetailSerializer,
    StudyUpdateSerializer,
    StudyMembershipSerializer,
    StudyMembershipCreateSerializer,
    StudyMembershipDetailSerializer,
    StudyMembershipUpdateSerializer,
    ScheduleSerializer,
    ScheduleCreateSerializer,
    ScheduleDetailSerializer,
    ScheduleUpdateSerializer,
    AttendanceSerializer,
    AttendanceCreateSerializer,
    AttendanceDetailSerializer,
    AttendanceUpdateSerializer,
    StudyInviteTokenCreateSerializer,
    StudyMembershipCreateByInviteTokenSerializer,
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
        operation_summary='StudyIcon List',
        operation_description='스터디 아이콘 목록'
    )
)
class StudyIconListAPIView(generics.ListAPIView):
    queryset = StudyIcon.objects.all()
    serializer_class = StudyIconSerializer


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
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Study.objects.user_queryset(user)
        return Study.objects.all()

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
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Study.objects.user_queryset(user)
        return Study.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return StudyUpdateSerializer
        return StudyDetailSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_id='study_read_by_token',
        operation_summary='Study Retrieve (By InviteToken)',
        operation_description='초대 토큰값을 사용한 스터디 정보'
    )
)
class StudyRetrieveByInviteTokenAPIView(generics.RetrieveAPIView):
    queryset = Study.objects.all()
    serializer_class = StudyDetailSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_object(self):
        token_key = self.kwargs.get('token')
        try:
            token = StudyInviteToken.objects.get(key=token_key)
        except StudyInviteToken.DoesNotExist:
            raise ValidationError(errors.STUDY_INVITE_TOKEN_INVALID)
        obj = get_object_or_404(self.queryset, token_set=token)
        return obj


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
            status.HTTP_200_OK: StudyMembershipDetailSerializer(),
        }
    )
)
class StudyMembershipListCreateAPIView(generics.ListCreateAPIView):
    filterset_class = StudyMembershipListFilter

    def get_queryset(self):
        return StudyMembership.objects.select_related(
            'user',
            'study__category',
            'study__author',
        ).prefetch_related(
            'study__member_set',
            'study__schedule_set',
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudyMembershipCreateSerializer
        return StudyMembershipSerializer

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
            status.HTTP_200_OK: StudyMembershipSerializer(),
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
            return StudyMembershipUpdateSerializer
        return StudyMembershipDetailSerializer

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
    filterset_class = ScheduleFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Schedule.objects.user_queryset(user)
        return Schedule.objects.all()

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
        user = self.request.user
        if user:
            return Schedule.objects.user_queryset(user)
        return Schedule.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ScheduleUpdateSerializer
        return ScheduleDetailSerializer

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


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='StudyInviteToken Create',
        operation_description='스터디 초대 토큰 생성(24시간 유효)'
    )
)
class StudyInviteTokenCreateAPIView(generics.CreateAPIView):
    queryset = StudyInviteToken.objects.all()
    serializer_class = StudyInviteTokenCreateSerializer


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='StudyMembership Create (By InviteToken)',
        operation_description='초대 토큰값을 사용한 스터디 멤버십 생성'
    )
)
class StudyMembershipCreateByInviteTokenAPIView(generics.CreateAPIView):
    queryset = StudyMembership.objects.all()
    serializer_class = StudyMembershipCreateByInviteTokenSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
