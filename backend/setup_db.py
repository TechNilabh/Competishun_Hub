import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Exam, QuizQuestion, CodingProblem, TestCase

user, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
)
if created:
    user.set_password('admin123')
    user.save()
 
Exam.objects.all().delete()

exam = Exam.objects.create(
    title='Sample Programming Assessment',
    description='A comprehensive assessment covering multiple choice questions and coding challenges',
    duration_minutes=120,
    quiz_duration_minutes=60,
    is_active=True
)

print(f'✅ Exam created: {exam.title}')

quiz_questions_data = [
    {
        'question_text': 'What is the time complexity of binary search in a sorted array?',
        'option_a': 'O(n)',
        'option_b': 'O(log n)',
        'option_c': 'O(n log n)',
        'option_d': 'O(1)',
        'correct_answer': 'B',
        'difficulty': 'easy',
        'category': 'Algorithms',
        'marks': 1,
        'order': 1
    },
    {
        'question_text': 'Which data structure uses LIFO (Last In First Out) principle?',
        'option_a': 'Queue',
        'option_b': 'Stack',
        'option_c': 'Tree',
        'option_d': 'Graph',
        'correct_answer': 'B',
        'difficulty': 'easy',
        'category': 'Data Structures',
        'marks': 1,
        'order': 2
    },
    {
        'question_text': 'What is the worst-case time complexity of Quick Sort?',
        'option_a': 'O(n)',
        'option_b': 'O(n log n)',
        'option_c': 'O(n²)',
        'option_d': 'O(log n)',
        'correct_answer': 'C',
        'difficulty': 'medium',
        'category': 'Algorithms',
        'marks': 2,
        'order': 3
    },
    {
        'question_text': 'In Python, which keyword is used to create a function?',
        'option_a': 'func',
        'option_b': 'def',
        'option_c': 'function',
        'option_d': 'define',
        'correct_answer': 'B',
        'difficulty': 'easy',
        'category': 'Python',
        'marks': 1,
        'order': 4
    },
    {
        'question_text': 'What does SQL stand for?',
        'option_a': 'Structured Query Language',
        'option_b': 'Simple Query Language',
        'option_c': 'System Query Language',
        'option_d': 'Standard Query Language',
        'correct_answer': 'A',
        'difficulty': 'easy',
        'category': 'Databases',
        'marks': 1,
        'order': 5
    },
    {
        'question_text': 'Which of the following is NOT a programming paradigm?',
        'option_a': 'Object-Oriented',
        'option_b': 'Functional',
        'option_c': 'Procedural',
        'option_d': 'Sequential',
        'correct_answer': 'D',
        'difficulty': 'medium',
        'category': 'Programming Concepts',
        'marks': 2,
        'order': 6
    },
    {
        'question_text': 'What is the output of: print(2 ** 3 ** 2) in Python?',
        'option_a': '64',
        'option_b': '512',
        'option_c': '8',
        'option_d': 'Error',
        'correct_answer': 'B',
        'difficulty': 'medium',
        'category': 'Python',
        'marks': 2,
        'order': 7
    },
    {
        'question_text': 'Which sorting algorithm is most efficient for nearly sorted data?',
        'option_a': 'Bubble Sort',
        'option_b': 'Insertion Sort',
        'option_c': 'Quick Sort',
        'option_d': 'Heap Sort',
        'correct_answer': 'B',
        'difficulty': 'medium',
        'category': 'Algorithms',
        'marks': 2,
        'order': 8
    },
    {
        'question_text': 'What is the space complexity of a recursive function with depth n?',
        'option_a': 'O(1)',
        'option_b': 'O(log n)',
        'option_c': 'O(n)',
        'option_d': 'O(n²)',
        'correct_answer': 'C',
        'difficulty': 'hard',
        'category': 'Algorithms',
        'marks': 3,
        'order': 9
    },
    {
        'question_text': 'In a binary tree, what is the maximum number of nodes at level L?',
        'option_a': '2^L',
        'option_b': 'L^2',
        'option_c': '2L',
        'option_d': 'L!',
        'correct_answer': 'A',
        'difficulty': 'hard',
        'category': 'Data Structures',
        'marks': 3,
        'order': 10
    },
]

for q_data in quiz_questions_data:
    QuizQuestion.objects.create(exam=exam, **q_data)

print(f'✅ Created {len(quiz_questions_data)} quiz questions')

problem1 = CodingProblem.objects.create(
    exam=exam,
    title='Two Sum',
    description='Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.',
    input_format='First line contains n (number of elements)\nSecond line contains n space-separated integers\nThird line contains target',
    output_format='Two space-separated integers representing the indices (0-indexed)',
    constraints='• 2 ≤ n ≤ 10⁴\n• -10⁹ ≤ nums[i] ≤ 10⁹\n• -10⁹ ≤ target ≤ 10⁹\n• Only one valid answer exists',
    sample_input='4\n2 7 11 15\n9',
    sample_output='0 1',
    difficulty='easy',
    max_marks=100,
    order=1
)

TestCase.objects.create(
    problem=problem1,
    input_data='4\n2 7 11 15\n9',
    expected_output='0 1',
    is_sample=True,
    is_hidden=False,
    marks=20
)

TestCase.objects.create(
    problem=problem1,
    input_data='3\n3 2 4\n6',
    expected_output='1 2',
    is_sample=False,
    is_hidden=True,
    marks=40
)

TestCase.objects.create(
    problem=problem1,
    input_data='2\n3 3\n6',
    expected_output='0 1',
    is_sample=False,
    is_hidden=True,
    marks=40
)

problem2 = CodingProblem.objects.create(
    exam=exam,
    title='Palindrome Number',
    description='Given an integer x, return true if x is a palindrome, and false otherwise.\n\nAn integer is a palindrome when it reads the same backward as forward.\n\nFor example, 121 is a palindrome while 123 is not.',
    input_format='A single integer x',
    output_format='Print "true" if palindrome, "false" otherwise',
    constraints='• -2³¹ ≤ x ≤ 2³¹ - 1',
    sample_input='121',
    sample_output='true',
    difficulty='easy',
    max_marks=100,
    order=2
)

TestCase.objects.create(
    problem=problem2,
    input_data='121',
    expected_output='true',
    is_sample=True,
    is_hidden=False,
    marks=25
)

TestCase.objects.create(
    problem=problem2,
    input_data='-121',
    expected_output='false',
    is_sample=False,
    is_hidden=True,
    marks=25
)

TestCase.objects.create(
    problem=problem2,
    input_data='10',
    expected_output='false',
    is_sample=False,
    is_hidden=True,
    marks=25
)

TestCase.objects.create(
    problem=problem2,
    input_data='12321',
    expected_output='true',
    is_sample=False,
    is_hidden=True,
    marks=25
)

print('\n' + '='*50)
print('='*50)
print(f'Exam ID: {exam.id}')
print(f'Total Questions: {QuizQuestion.objects.count()}')
print(f'Total Coding Problems: {CodingProblem.objects.count()}')