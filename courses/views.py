from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Course, Lesson, Enrollment, Quiz, UserLessonProgress
from .serializers import CourseSerializer, LessonSerializer, EnrollmentSerializer, QuizSerializer, UserLessonProgressSerializer

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

class CourseRetrieveView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class EnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)
        Enrollment.objects.get_or_create(user=request.user, course=course)
        return Response({"message": "Enrolled successfully."})

class SubmitQuizView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        answers = request.data.get('answers', {})
        total_score = 0
        for quiz in lesson.quizzes.all():
            if str(quiz.id) in answers:
                if quiz.correct_answer.lower().strip() == answers[str(quiz.id)].lower().strip():
                    total_score += 1
        progress, _ = UserLessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
        progress.completed = True
        progress.quiz_score = total_score
        progress.save()
        return Response({"message": "Quiz submitted", "score": total_score})

class UserLessonProgressView(generics.RetrieveAPIView):
    serializer_class = UserLessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        lesson_id = self.kwargs['lesson_id']
        return UserLessonProgress.objects.get(user=self.request.user, lesson_id=lesson_id)
