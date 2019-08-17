from django.urls import path

from . import apis

app_name = 'study'
urlpatterns = [
    path('category/', apis.StudyCategoryListCreateAPIView.as_view()),
    path('icons/', apis.StudyIconListAPIView.as_view()),
    path('', apis.StudyListCreateAPIView.as_view()),
    path('token/<str:token>/', apis.StudyRetrieveByInviteTokenAPIView.as_view()),
    path('<int:pk>/', apis.StudyRetrieveUpdateDestroyAPIView.as_view()),
    path('memberships/', apis.StudyMembershipListCreateAPIView.as_view()),
    path('memberships/<int:pk>/', apis.StudyMembershipRetrieveUpdateDestroyAPIView.as_view()),
    path('schedules/', apis.ScheduleListCreateAPIView.as_view()),
    path('schedules/<int:pk>/', apis.ScheduleRetrieveUpdateDestroyAPIView.as_view()),
    path('attendances/', apis.AttendanceListCreateAPIView.as_view()),
    path('attendances/<int:pk>/', apis.AttendanceRetrieveUpdateDestroyAPIView.as_view()),

    # 초대토큰 생성
    path('invite-token/', apis.StudyInviteTokenCreateAPIView.as_view()),
    # 초대토큰을 사용한 멤버십 생성
    path('memberships/token/', apis.StudyMembershipCreateByInviteTokenAPIView.as_view()),
]
