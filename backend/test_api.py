import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_fetch_exams():
    print('Testing: Fetch Exams')
    response = requests.get(f'{BASE_URL}/exams/')
    print(f'Status: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    print('-' * 50)
    return response.json()

def test_create_session(exam_id):
    print('Testing: Create Exam Session')
    data = {
        'exam': exam_id,
        'is_camera_enabled': True,
        'is_mic_enabled': True,
        'is_screen_shared': False
    }
    response = requests.post(f'{BASE_URL}/exam-sessions/', json=data)
    print(f'Status: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    print('-' * 50)
    return response.json()

def test_get_questions(exam_id):
    print('Testing: Get Exam Questions')
    response = requests.get(f'{BASE_URL}/exams/{exam_id}/questions/')
    print(f'Status: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)[:500]}...')
    print('-' * 50)
    return response.json()

def test_submit_quiz_answer(session_id, question_id):
    print('Testing: Submit Quiz Answer')
    data = {
        'session': session_id,
        'question': question_id,
        'selected_answer': 'B'
    }
    response = requests.post(f'{BASE_URL}/quiz-answers/', json=data)
    print(f'Status: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    print('-' * 50)

def test_code_execution():
    print('Testing: Code Execution via Piston')
    piston_url = 'https://emkc.org/api/v2/piston/execute'
    data = {
        "language": "python",
        "version": "3.10.0",
        "files": [
            {
                "name": "main.py",
                "content": "print('Hello, World!')"
            }
        ],
        "stdin": "",
        "args": []
    }
    response = requests.post(piston_url, json=data)
    print(f'Status: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
    print('-' * 50)

if __name__ == '__main__':
    print('Starting API Tests...\n')
    
    
    exams = test_fetch_exams()
    
    if exams:
        exam_id = exams[0]['id']
        
       
        session = test_create_session(exam_id)
        session_id = session['id']
        
        questions = test_get_questions(exam_id)
        
        if questions.get('quiz_questions'):
            question_id = questions['quiz_questions'][0]['id']
            
            test_submit_quiz_answer(session_id, question_id)
    
    test_code_execution()
    
    print('\nAll tests completed!')