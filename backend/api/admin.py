from django.contrib import admin
from .models import (
    Exam, ExamSession, QuizQuestion, QuizAnswer,
    CodingProblem, TestCase, CodingSubmission, ProctoringLog
)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration_minutes', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']

@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'status', 'total_score', 'violation_count', 'started_at']
    list_filter = ['status', 'started_at']
    search_fields = ['user__username', 'exam__title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'exam', 'correct_answer', 'marks', 'difficulty', 'order']
    list_filter = ['exam', 'difficulty']
    search_fields = ['question_text']
    ordering = ['exam', 'order']

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['session', 'question', 'selected_answer', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']
    search_fields = ['session__user__username']

@admin.register(CodingProblem)
class CodingProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam', 'difficulty', 'max_marks', 'order']
    list_filter = ['exam', 'difficulty']
    search_fields = ['title', 'description']

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['problem', 'is_sample', 'is_hidden', 'marks']
    list_filter = ['is_sample', 'is_hidden', 'problem']

@admin.register(CodingSubmission)
class CodingSubmissionAdmin(admin.ModelAdmin):
    list_display = ['session', 'problem', 'language', 'status', 'score', 'submitted_at']
    list_filter = ['status', 'language', 'submitted_at']
    search_fields = ['session__user__username', 'problem__title']
    readonly_fields = ['submitted_at']

@admin.register(ProctoringLog)
class ProctoringLogAdmin(admin.ModelAdmin):
    list_display = ['session', 'violation_type', 'severity', 'timestamp']
    list_filter = ['violation_type', 'severity', 'timestamp']
    search_fields = ['session__user__username']
    readonly_fields = ['timestamp']
from .models import Submission, Leaderboard

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'timestamp')
    list_filter = ('user',)
    ordering = ('-score',)

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'best_score')
    ordering = ('-best_score',)
