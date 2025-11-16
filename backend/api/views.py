from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Submission, Leaderboard
from .ml_scoring import evaluate_submission
from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.shortcuts import get_object_or_404
from django.utils import timezone
import requests
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
# @login_required
def submit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method only"}, status=400)

    file = request.FILES["file"]
    score = evaluate_submission(file)
    # print(score)

    guest_user, _ = User.objects.get_or_create(username="guest", defaults={
        "email": "guest@example.com",
        "password": "test123",  
    })

    Submission.objects.create(user=guest_user, file=file, score=score)

    lb, _ = Leaderboard.objects.get_or_create(user=guest_user)
    if score > lb.best_score:
        lb.best_score = score
        lb.save()

    rank = list(Leaderboard.objects.order_by("-best_score")).index(lb) + 1

    return JsonResponse({"score": score, "rank": rank})


def leaderboard(request):
    data = [
        {
            "user": row.user.username,
            "score": row.best_score
        }
        for row in Leaderboard.objects.order_by("-best_score")
    ]
    return JsonResponse(data, safe=False)


def history(request):
    guest = User.objects.get(username="guest")  
    submissions = Submission.objects.filter(user=guest).order_by("-timestamp")

    data = [
        {
            "score": s.score,
            "file": s.file.name,
            "timestamp": s.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for s in submissions
    ]

    return JsonResponse(data, safe=False)

from .models import (
    Exam, ExamSession, QuizQuestion, QuizAnswer,
    CodingProblem, TestCase, CodingSubmission, ProctoringLog,
    Team, TeamMember, Payment
)
from .serializers import (
    ExamSerializer, ExamSessionSerializer, ExamSessionCreateSerializer,
    QuizQuestionSerializer, QuizAnswerSerializer,
    CodingProblemSerializer, CodingSubmissionSerializer, ProctoringLogSerializer,
    TeamSerializer, TeamMemberSerializer, PaymentSerializer, UserSerializer
)
from django.contrib.auth.models import User

PISTON_API_URL = "https://emkc.org/api/v2/piston"

LANGUAGE_MAPPING = {
    'python': {'name': 'python', 'version': '3.10.0'},
    'c': {'name': 'c', 'version': '10.2.0'},
    'cpp': {'name': 'c++', 'version': '10.2.0'},
    'java': {'name': 'java', 'version': '15.0.2'},
    'javascript': {'name': 'javascript', 'version': '18.15.0'},
}

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        name = (request.data.get('name') or '').strip()
        email = (request.data.get('email') or '').strip().lower()
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email__iexact=email).exists():
            return Response({'error': 'email already in use'}, status=status.HTTP_400_BAD_REQUEST)

        base_username = email.split('@')[0] if '@' in email else email
        username = base_username
        i = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{i}"
            i += 1

        first_name, last_name = '', ''
        if name:
            parts = name.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email_or_username = (request.data.get('email') or '').strip()
        password = request.data.get('password')

        if not email_or_username or not password:
            return Response({'error': 'email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=email_or_username).first()
        if not user:
            user = User.objects.filter(username=email_or_username).first()
        if not user:
            return Response({'error': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        auth_user = authenticate(request, username=user.username, password=password)
        if not auth_user:
            return Response({'error': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=auth_user)
        return Response({'token': token.key, 'user': UserSerializer(auth_user).data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({'status': 'ok'})

class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exam.objects.filter(is_active=True)
    serializer_class = ExamSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        exam = self.get_object()
        quiz_questions = QuizQuestion.objects.filter(exam=exam)
        coding_problems = CodingProblem.objects.filter(exam=exam)
        return Response({
            'quiz_questions': QuizQuestionSerializer(quiz_questions, many=True).data,
            'coding_problems': CodingProblemSerializer(coding_problems, many=True).data,
        })

class ExamSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSessionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ExamSession.objects.all()

    def create(self, request):
        serializer = ExamSessionCreateSerializer(data=request.data)
        if serializer.is_valid():
            user, _ = User.objects.get_or_create(
                username='test_user',
                defaults={'email': 'test@example.com'}
            )
            exam = serializer.validated_data['exam']
            existing_session = ExamSession.objects.filter(
                user=user,
                exam=exam
            ).exclude(status='completed').exclude(status='disqualified').first()
            if existing_session:
                return Response(
                    ExamSessionSerializer(existing_session).data,
                    status=status.HTTP_200_OK
                )
            session = serializer.save(user=user)
            return Response(
                ExamSessionSerializer(session).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        session = self.get_object()
        if session.status != 'not_started':
            return Response(
                {'error': 'Exam already started or completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        session.status = 'in_progress'
        session.started_at = timezone.now()
        session.save()
        return Response(ExamSessionSerializer(session).data)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        session = self.get_object()
        if session.status != 'in_progress':
            return Response(
                {'error': 'Cannot submit exam that is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )
        quiz_answers = QuizAnswer.objects.filter(session=session, is_correct=True)
        session.quiz_score = sum(answer.question.marks for answer in quiz_answers)
        coding_submissions = CodingSubmission.objects.filter(
            session=session,
            status='accepted'
        )
        session.coding_score = sum(sub.score for sub in coding_submissions)
        session.total_score = session.quiz_score + session.coding_score
        session.status = 'completed'
        session.submitted_at = timezone.now()
        session.save()
        return Response(ExamSessionSerializer(session).data)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        session = self.get_object()
        time_remaining = None
        if session.started_at and session.status == 'in_progress':
            elapsed = (timezone.now() - session.started_at).total_seconds()
            total_duration = session.exam.duration_minutes * 60
            time_remaining = max(0, total_duration - elapsed)
        return Response({
            'session': ExamSessionSerializer(session).data,
            'time_remaining': time_remaining,
            'violation_count': session.violation_count,
        })

class QuizAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = QuizAnswerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return QuizAnswer.objects.all()

    def create(self, request):
        session_id = request.data.get('session')
        question_id = request.data.get('question')
        selected_answer = request.data.get('selected_answer')
        session = get_object_or_404(ExamSession, id=session_id)
        question = get_object_or_404(QuizQuestion, id=question_id)
        answer, _ = QuizAnswer.objects.update_or_create(
            session=session,
            question=question,
            defaults={
                'selected_answer': selected_answer,
                'is_correct': selected_answer == question.correct_answer,
            }
        )
        return Response(QuizAnswerSerializer(answer).data)

    @action(detail=False, methods=['get'])
    def session_answers(self, request):
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response(
                {'error': 'session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        answers = QuizAnswer.objects.filter(session_id=session_id)
        return Response(QuizAnswerSerializer(answers, many=True).data)

class CodingSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = CodingSubmissionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CodingSubmission.objects.all()

    def create(self, request):
        serializer = CodingSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save(status='running')
            try:
                result = self.execute_code(submission)
                submission.status = result['status']
                submission.score = result['score']
                submission.test_cases_passed = result['test_cases_passed']
                submission.total_test_cases = result['total_test_cases']
                submission.execution_time_ms = result.get('execution_time_ms', 0)
                submission.memory_used_kb = result.get('memory_used_kb', 0)
                submission.error_message = result.get('error_message', '')
                submission.save()
                session = submission.session
                best_score = CodingSubmission.objects.filter(
                    session=session,
                    problem=submission.problem,
                    status='accepted'
                ).order_by('-score').first()
                if best_score:
                    all_problems_best = {}
                    for sub in CodingSubmission.objects.filter(
                        session=session,
                        status='accepted'
                    ):
                        prob_id = str(sub.problem.id)
                        if prob_id not in all_problems_best or sub.score > all_problems_best[prob_id]:
                            all_problems_best[prob_id] = sub.score
                    session.coding_score = sum(all_problems_best.values())
                    session.save()
                return Response(CodingSubmissionSerializer(submission).data)
            except Exception as e:
                submission.status = 'runtime_error'
                submission.error_message = str(e)
                submission.save()
                return Response(
                    CodingSubmissionSerializer(submission).data,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def execute_code(self, submission):
        problem = submission.problem
        test_cases = TestCase.objects.filter(problem=problem)
        language_config = LANGUAGE_MAPPING.get(submission.language)
        if not language_config:
            raise ValueError(f"Unsupported language: {submission.language}")
        passed_tests = 0
        total_tests = test_cases.count()
        total_time = 0
        total_memory = 0
        for test_case in test_cases:
            try:
                piston_request = {
                    "language": language_config['name'],
                    "version": language_config['version'],
                    "files": [
                        {
                            "name": f"main.{self.get_file_extension(submission.language)}",
                            "content": submission.code
                        }
                    ],
                    "stdin": test_case.input_data,
                    "args": [],
                    "compile_timeout": 10000,
                    "run_timeout": 5000,
                }
                response = requests.post(
                    f"{PISTON_API_URL}/execute",
                    json=piston_request,
                    timeout=10
                )
                if response.status_code != 200:
                    continue
                result = response.json()
                if 'compile' in result and result['compile'].get('code') != 0:
                    return {
                        'status': 'compilation_error',
                        'score': 0,
                        'test_cases_passed': 0,
                        'total_test_cases': total_tests,
                        'error_message': result['compile'].get('stderr', 'Compilation failed')
                    }
                run_result = result.get('run', {})
                if run_result.get('code') != 0:
                    if run_result.get('signal') == 'SIGKILL':
                        return {
                            'status': 'time_limit',
                            'score': 0,
                            'test_cases_passed': passed_tests,
                            'total_test_cases': total_tests,
                            'error_message': 'Time limit exceeded'
                        }
                    else:
                        return {
                            'status': 'runtime_error',
                            'score': 0,
                            'test_cases_passed': passed_tests,
                            'total_test_cases': total_tests,
                            'error_message': run_result.get('stderr', 'Runtime error')
                        }
                output = run_result.get('stdout', '').strip()
                expected = test_case.expected_output.strip()
                if output == expected:
                    passed_tests += 1
                total_time += run_result.get('cpu_time', 0)
                total_memory += run_result.get('memory', 0)
            except requests.Timeout:
                return {
                    'status': 'time_limit',
                    'score': 0,
                    'test_cases_passed': passed_tests,
                    'total_test_cases': total_tests,
                    'error_message': 'Request timeout'
                }
            except Exception:
                continue
        score_percentage = (passed_tests / total_tests) * 100
        score = int((score_percentage / 100) * problem.max_marks)
        status_text = 'accepted' if passed_tests == total_tests else 'wrong_answer'
        return {
            'status': status_text,
            'score': score,
            'test_cases_passed': passed_tests,
            'total_test_cases': total_tests,
            'execution_time_ms': total_time,
            'memory_used_kb': total_memory // 1024,
        }

    def get_file_extension(self, language):
        extensions = {
            'python': 'py',
            'c': 'c',
            'cpp': 'cpp',
            'java': 'java',
            'javascript': 'js',
        }
        return extensions.get(language, 'txt')

    @action(detail=False, methods=['get'])
    def problem_submissions(self, request):
        session_id = request.query_params.get('session_id')
        problem_id = request.query_params.get('problem_id')
        if not session_id or not problem_id:
            return Response(
                {'error': 'session_id and problem_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        submissions = CodingSubmission.objects.filter(
            session_id=session_id,
            problem_id=problem_id
        ).order_by('-submitted_at')
        return Response(CodingSubmissionSerializer(submissions, many=True).data)

class ProctoringLogViewSet(viewsets.ModelViewSet):
    serializer_class = ProctoringLogSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ProctoringLog.objects.all()

    def create(self, request):
        serializer = ProctoringLogSerializer(data=request.data)
        if serializer.is_valid():
            log = serializer.save()
            session = log.session
            session.violation_count += 1
            if session.violation_count >= 3 and session.status == 'in_progress':
                session.status = 'disqualified'
                session.submitted_at = timezone.now()
            session.save()
            return Response({
                'log': ProctoringLogSerializer(log).data,
                'violation_count': session.violation_count,
                'auto_submitted': session.status == 'disqualified',
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Team.objects.all()

    def create(self, request):
        data = request.data
        user = request.user if request.user and request.user.is_authenticated else User.objects.get_or_create(
            username='test_user', defaults={'email': 'test@example.com'}
        )[0]
        team = Team.objects.create(
            name=data['name'],
            description=data['description'],
            max_members=data.get('maxMembers', 4),
            leader=user
        )
        TeamMember.objects.create(
            team=team,
            user=user,
            email=user.email,
            role='leader',
            status='accepted'
        )
        return Response(TeamSerializer(team).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        team = self.get_object()
        email = request.data.get('email')
        if TeamMember.objects.filter(team=team).count() >= team.max_members:
            return Response(
                {'error': 'Team is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
        member, created = TeamMember.objects.get_or_create(
            team=team,
            email=email,
            defaults={'role': 'member', 'status': 'pending'}
        )
        if not created:
            return Response(
                {'error': 'Member already invited'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(TeamMemberSerializer(member).data)

class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create_checkout(self, request):
        team_id = request.data.get('team_id')
        plan = request.data.get('plan')
        team = Team.objects.get(id=team_id)
        user = request.user if request.user and request.user.is_authenticated else User.objects.get_or_create(
            username='test_user', defaults={'email': 'test@example.com'}
        )[0]
        prices = {
            'basic': 49900,
            'standard': 99900,
            'premium': 199900,
        }
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f'{plan.title()} Plan - {team.name}',
                        },
                        'unit_amount': prices.get(plan, 99900),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'{settings.FRONTEND_URL}/team/success?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{settings.FRONTEND_URL}/team/payment?team_id={team_id}',
                metadata={
                    'team_id': str(team.id),
                    'plan': plan,
                }
            )
            Payment.objects.create(
                team=team,
                user=user,
                plan=plan,
                amount=prices.get(plan, 99900) / 100,
                currency='INR',
                stripe_session_id=session.id,
                status='pending'
            )
            return Response({'sessionId': session.id})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def verify(self, request, session_id=None):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment = Payment.objects.get(stripe_session_id=session_id)
            if session.payment_status == 'paid':
                payment.status = 'completed'
                payment.stripe_payment_intent = session.payment_intent
                payment.completed_at = timezone.now()
                payment.save()
                return Response({
                    'status': 'success',
                    'payment': PaymentSerializer(payment).data
                })
            else:
                return Response({'status': 'pending'}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def webhook(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                payment = Payment.objects.get(stripe_session_id=session['id'])
                payment.status = 'completed'
                payment.stripe_payment_intent = session['payment_intent']
                payment.completed_at = timezone.now()
                payment.save()
            return Response({'status': 'success'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )