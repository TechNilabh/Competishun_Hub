from django.db import models
from django.contrib.auth.models import User
import uuid


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_minutes = models.IntegerField(default=120)
    quiz_duration_minutes = models.IntegerField(default=60)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ExamSession(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('disqualified', 'Disqualified'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    started_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    quiz_score = models.IntegerField(default=0)
    coding_score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    violation_count = models.IntegerField(default=0)
    is_camera_enabled = models.BooleanField(default=False)
    is_mic_enabled = models.BooleanField(default=False)
    is_screen_shared = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'exam'], name='unique_user_exam_session'),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}"


class QuizQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='quiz_questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500, blank=True, null=True)
    option_d = models.CharField(max_length=500, blank=True, null=True)
    correct_answer = models.CharField(max_length=1)
    marks = models.IntegerField(default=1)
    difficulty = models.CharField(max_length=20, default='medium')
    category = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}"


class QuizAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='quiz_answers')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    time_taken_seconds = models.IntegerField(default=0)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'question'], name='unique_session_question'),
        ]

    def __str__(self):
        return f"{self.session.user.username} - Q{self.question.order}"


class CodingProblem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='coding_problems')
    title = models.CharField(max_length=200)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    constraints = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    difficulty = models.CharField(max_length=20, default='medium')
    max_marks = models.IntegerField(default=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class TestCase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=True)
    marks = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.problem.title} - TestCase {self.id}"


class CodingSubmission(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('c', 'C'),
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('accepted', 'Accepted'),
        ('wrong_answer', 'Wrong Answer'),
        ('runtime_error', 'Runtime Error'),
        ('time_limit', 'Time Limit Exceeded'),
        ('compilation_error', 'Compilation Error'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='coding_submissions')
    problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    score = models.IntegerField(default=0)
    test_cases_passed = models.IntegerField(default=0)
    total_test_cases = models.IntegerField(default=0)
    execution_time_ms = models.IntegerField(default=0)
    memory_used_kb = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.session.user.username} - {self.problem.title} - {self.status}"


class ProctoringLog(models.Model):
    VIOLATION_TYPES = [
        ('no_face', 'No Face Detected'),
        ('multiple_faces', 'Multiple Faces'),
        ('looking_away', 'Looking Away'),
        ('tab_switch', 'Tab Switch'),
        ('audio_detected', 'Audio Detected'),
        ('mobile_detected', 'Mobile Phone Detected'),
        ('suspicious_object', 'Suspicious Object'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='proctoring_logs')
    violation_type = models.CharField(max_length=30, choices=VIOLATION_TYPES)
    severity = models.CharField(max_length=10, default='medium')
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    snapshot_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.session.user.username} - {self.violation_type} - {self.timestamp}"


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_teams')
    max_members = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('leader', 'Leader'),
        ('member', 'Member'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    invited_at = models.DateTimeField(auto_now_add=True)
    joined_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'email'], name='unique_team_email'),
        ]

    def __str__(self):
        return f"{self.email} - {self.team.name}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    stripe_session_id = models.CharField(max_length=255, unique=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.team.name} - {self.amount} {self.currency}"
from django.contrib.auth.models import User

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="submissions/")
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    best_score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.best_score}"
