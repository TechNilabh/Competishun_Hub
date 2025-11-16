# Optional: Command to fetch questions from QuizAPI
import os
import requests
from django.core.management.base import BaseCommand
from api.models import Exam, QuizQuestion

class Command(BaseCommand):
    help = 'Fetch quiz questions from QuizAPI'

    def add_arguments(self, parser):
        parser.add_argument('exam_id', type=str, help='Exam ID to add questions to')
        parser.add_argument('--limit', type=int, default=40, help='Number of questions to fetch')

    def handle(self, *args, **options):
        exam_id = options['exam_id']
        limit = options['limit']
        
        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Exam with ID {exam_id} does not exist'))
            return
        
        api_key = 'JrWbGB8ehB6N3APngfmdeaSZvES0yZHKw3dvf7wh'
        url = f'https://quizapi.io/api/v1/questions?apiKey={api_key}&limit={limit}'
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            questions_data = response.json()
            
            created_count = 0
            for idx, q_data in enumerate(questions_data):
                # Extract answers
                answers = q_data.get('answers', {})
                correct_answers = q_data.get('correct_answers', {})
                
                # Find correct answer
                correct_answer = None
                for key, value in correct_answers.items():
                    if value == 'true':
                        correct_answer = key.replace('_correct', '').upper()
                        break
                
                if not correct_answer:
                    continue
                
                # Create question
                QuizQuestion.objects.create(
                    exam=exam,
                    question_text=q_data.get('question', ''),
                    option_a=answers.get('answer_a', ''),
                    option_b=answers.get('answer_b', ''),
                    option_c=answers.get('answer_c', ''),
                    option_d=answers.get('answer_d', ''),
                    correct_answer=correct_answer[7],  # Get letter from 'answer_a'
                    difficulty=q_data.get('difficulty', 'medium'),
                    category=q_data.get('category', ''),
                    marks=1,
                    order=idx + 1
                )
                created_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} questions for exam {exam.title}')
            )
            
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Failed to fetch questions: {str(e)}'))