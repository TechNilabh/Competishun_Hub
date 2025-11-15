from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet,
    ExamViewSet, ExamSessionViewSet, QuizAnswerViewSet,
    CodingSubmissionViewSet, ProctoringLogViewSet,
    TeamViewSet, PaymentViewSet
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'exam-sessions', ExamSessionViewSet, basename='exam-session')
router.register(r'quiz-answers', QuizAnswerViewSet, basename='quiz-answer')
router.register(r'coding-submissions', CodingSubmissionViewSet, basename='coding-submission')
router.register(r'proctoring-logs', ProctoringLogViewSet, basename='proctoring-log')
router.register(r'teams', TeamViewSet, basename='team')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/create-checkout/', PaymentViewSet.as_view({'post': 'create_checkout'})),
    path('payments/verify/<str:session_id>/', PaymentViewSet.as_view({'get': 'verify'})),
    path('payments/webhook/', PaymentViewSet.as_view({'post': 'webhook'})),
]