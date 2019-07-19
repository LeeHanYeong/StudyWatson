from django.urls import path
from . import apis

app_name = 'study'
urlpatterns = [
    path('category/', apis.StudyCategoryListCreateAPIView.as_view()),
    path('', apis.StudyListCreateAPIView.as_view()),
    path('<int:pk>/', apis.StudyRetrieveUpdateDestroyAPIView.as_view()),
    path('memberships/', apis.StudyMembershipListCreateAPIView.as_view()),
    path('memberships/<int:pk>/', apis.StudyMembershipRetrieveUpdateDestroyAPIView.as_view()),
    path('schedules/', apis.ScheduleListCreateAPIView.as_view()),
    path('schedules/<int:pk>/', apis.ScheduleRetrieveUpdateDestroyAPIView.as_view()),
    path('attendances/', apis.AttendanceListCreateAPIView.as_view()),
    path('attendances/<int:pk>/', apis.AttendanceRetrieveUpdateDestroyAPIView.as_view()),
]
