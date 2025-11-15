from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Exam,
    ExamSession,
    QuizQuestion,
    QuizAnswer,
    CodingProblem,
    TestCase,
    CodingSubmission,
    ProctoringLog,
    Team,
    TeamMember,
    Payment,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        exclude = ['correct_answer']  # Don't send correct answer to frontend


class QuizQuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = '__all__'


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = '__all__'


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'input_data', 'expected_output', 'is_sample', 'marks']


class TestCaseHiddenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'is_sample', 'marks']  # Don't show actual test case data


class CodingProblemSerializer(serializers.ModelSerializer):
    test_cases = serializers.SerializerMethodField()

    class Meta:
        model = CodingProblem
        fields = '__all__'

    def get_test_cases(self, obj):
        # Only return sample test cases
        sample_cases = obj.test_cases.filter(is_sample=True)
        return TestCaseSerializer(sample_cases, many=True).data


class CodingSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingSubmission
        fields = '__all__'
        read_only_fields = [
            'status',
            'score',
            'test_cases_passed',
            'total_test_cases',
            'execution_time_ms',
            'memory_used_kb',
            'error_message',
        ]


class ProctoringLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProctoringLog
        fields = '__all__'


class ExamSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    exam = ExamSerializer(read_only=True)

    class Meta:
        model = ExamSession
        fields = '__all__'


class ExamSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSession
        fields = ['exam', 'is_camera_enabled', 'is_mic_enabled', 'is_screen_shared']


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)
    leader_name = serializers.CharField(source='leader.username', read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['stripe_session_id', 'stripe_payment_intent', 'status']