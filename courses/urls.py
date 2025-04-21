from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListCreateView.as_view()),  # No extra 'courses/' here
    path('<int:pk>/', views.CourseRetrieveView.as_view()),
    path('<int:course_id>/enroll/', views.EnrollView.as_view()),
    path('../lessons/<int:lesson_id>/submit-quiz/', views.SubmitQuizView.as_view()),
    path('../lessons/<int:lesson_id>/progress/', views.UserLessonProgressView.as_view()),
]
# The above code defines the URL patterns for the courses app. It includes paths for listing and creating courses, retrieving a specific course, enrolling in a course, submitting a quiz, and checking user lesson progress. Each path is associated with a corresponding view class that handles the request and response logic.