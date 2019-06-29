from django.urls import path
from . import apis

app_name = 'study'
urlpatterns = [
    path('category/', apis.StudyCategoryListCreateAPIView.as_view()),
    path('', apis.StudyListCreateAPIView.as_view()),
    path('<int:pk>/', apis.StudyRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:study_pk>/members/', apis.StudyMemberListCreateAPIView.as_view()),
    path('<int:study_pk>/members/<int:pk>/', apis.StudyMemberRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:study_pk>/schedules/', apis.ScheduleListCreateAPIView.as_view()),
    path('<int:study_pk>/schedules/<int:pk>/', apis.ScheduleRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:study_pk>/attendance/', apis.AttendanceListCreateAPIView.as_view()),
    path('<int:study_pk>/attendance/<int:pk>/', apis.AttendanceRetrieveUpdateDestroyAPIView.as_view()),
]
