from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from backend.models import db, User, Quiz, Question, Score, Chapter, Subject

import jwt
import redis
import json
from functools import wraps

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'RADHAKRISHNA'  # Use environment variable in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY'  # Use environment variable in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db.init_app(app)
app.app_context().push()


# Redis configuration
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()  # Test connection
except redis.ConnectionError:
    redis_client = None
    print("Redis not available, caching disabled")


# Utility functions
def cache_get(key):
    """Get data from Redis cache"""
    if not redis_client:
        return None
    try:
        data = redis_client.get(key)
        return json.loads(data) if data else None
    except:
        return None

def cache_set(key, data, expire=300):
    """Set data in Redis cache with expiration (default 5 minutes)"""
    if not redis_client:
        return
    try:
        redis_client.setex(key, expire, json.dumps(data, default=str))
    except:
        pass

def cache_delete(key):
    """Delete data from Redis cache"""
    if not redis_client:
        return
    try:
        redis_client.delete(key)
    except:
        pass

def generate_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'is_admin': user.is_admin,
        'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

def token_required(admin_required=False):
    """Decorator for token authentication"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            # print(request.headers)
            if 'Authorization' in request.headers:
                # print(request.headers['Authorization'])
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]  # Bearer <token>
                except IndexError:
                    return jsonify({'message': 'Token format invalid'}), 401
            
            if not token:
                return jsonify({'message': 'Token is missing'}), 401
            
            try:
                data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                current_user = User.query.get(data['user_id'])
                if not current_user:
                    return jsonify({'message': 'Invalid token'}), 401
                
                if admin_required and not current_user.is_admin:
                    return jsonify({'message': 'Admin access required'}), 403
                    
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Token is invalid'}), 401
            
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

def create_admin():
    if not User.query.filter_by(is_admin=True).first():
        admin = User(
            username='admin',
            password=generate_password_hash('0000'),
            full_name='Admin',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

def load_seed_data():
    seed_path = os.path.join(os.path.dirname(__file__), 'backend', 'seed_data.json')
    if not os.path.exists(seed_path):
        print("Seed data not found, skipping default content.")
        return None
    with open(seed_path, 'r', encoding='utf-8') as seed_file:
        return json.load(seed_file)

def seed_default_content():
    data = load_seed_data()
    if not data or not data.get('subjects'):
        return

    for subject_data in data['subjects']:
        subject = Subject(
            name=subject_data['name'],
            description=subject_data.get('description', '')
        )
        db.session.add(subject)
        db.session.flush()

        for chapter_data in subject_data.get('chapters', []):
            chapter = Chapter(
                name=chapter_data['name'],
                description=chapter_data.get('description', ''),
                subject_id=subject.id
            )
            db.session.add(chapter)
            db.session.flush()

            for quiz_data in chapter_data.get('quizzes', []):
                quiz = Quiz(
                    title=quiz_data['title'],
                    date_of_quiz=quiz_data.get('date_of_quiz', ''),
                    time_duration=quiz_data.get('time_duration', ''),
                    remarks=quiz_data.get('remarks', ''),
                    chapter_id=chapter.id
                )
                db.session.add(quiz)
                db.session.flush()

                for question_data in quiz_data.get('questions', []):
                    question = Question(
                        question_statement=question_data['question_statement'],
                        option1=question_data['option1'],
                        option2=question_data['option2'],
                        option3=question_data.get('option3', ''),
                        option4=question_data.get('option4', ''),
                        correct_option=int(question_data['correct_option']),
                        quiz_id=quiz.id
                    )
                    db.session.add(question)

    db.session.commit()
    print("Default subjects, chapters, quizzes, and questions seeded.")

# API Endpoints

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    new_user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        full_name=data.get('full_name', ''),
        qualification=data.get('qualification', ''),
        dob=data.get('dob', '')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    # print(data)
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        token = generate_token(user)
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/subjects', methods=['GET'])
@token_required()
def get_subjects(current_user):
    cache_key = 'subjects_all'
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return jsonify(cached_data), 200
    
    subjects = Subject.query.all()
    data = [subject.to_dict() for subject in subjects]
    
    cache_set(cache_key, data)
    return jsonify(data), 200

@app.route('/api/subjects', methods=['POST'])
@token_required(admin_required=True)
def create_subject(current_user):
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'message': 'Subject name is required'}), 400
    
    new_subject = Subject(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(new_subject)
    db.session.commit()
    
    # Clear cache
    cache_delete('subjects_all')
    
    return jsonify({
        'message': 'Subject created successfully',
        'subject': new_subject.to_dict()
    }), 201

@app.route('/api/subjects/<int:subject_id>', methods=['GET'])
@token_required()
def get_subject(current_user, subject_id):
    cache_key = f'subject_{subject_id}'
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return jsonify(cached_data), 200
    
    subject = Subject.query.get_or_404(subject_id)
    data = subject.to_dict()
    
    cache_set(cache_key, data)
    return jsonify(data), 200

@app.route('/api/subjects/<int:subject_id>', methods=['PUT'])
@token_required(admin_required=True)
def update_subject(current_user, subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    subject.name = data.get('name', subject.name)
    subject.description = data.get('description', subject.description)
    
    db.session.commit()
    
    # Clear cache
    cache_delete('subjects_all')
    cache_delete(f'subject_{subject_id}')
    
    return jsonify({
        'message': 'Subject updated successfully',
        'subject': subject.to_dict()
    }), 200

@app.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
@token_required(admin_required=True)
def delete_subject(current_user, subject_id):
    subject = Subject.query.get_or_404(subject_id)
    
    db.session.delete(subject)
    db.session.commit()
    
    # Clear cache
    cache_delete('subjects_all')
    cache_delete(f'subject_{subject_id}')
    
    return jsonify({'message': 'Subject deleted successfully'}), 200

# Chapter APIs
@app.route('/api/subjects/<int:subject_id>/chapters', methods=['POST'])
@token_required(admin_required=True)
def create_chapter(current_user, subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'message': 'Chapter name is required'}), 400
    
    new_chapter = Chapter(
        name=data['name'],
        description=data.get('description', ''),
        subject_id=subject_id
    )
    
    db.session.add(new_chapter)
    db.session.commit()
    
    # Clear cache
    cache_delete('subjects_all')
    cache_delete(f'subject_{subject_id}')
    
    return jsonify({
        'message': 'Chapter created successfully',
        'chapter': new_chapter.to_dict()
    }), 201

@app.route('/api/chapters/<int:chapter_id>', methods=['GET'])
@token_required()
def get_chapter(current_user, chapter_id):
    cache_key = f'chapter_{chapter_id}'
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return jsonify(cached_data), 200
    
    chapter = Chapter.query.get_or_404(chapter_id)
    data = chapter.to_dict()
    
    cache_set(cache_key, data)
    return jsonify(data), 200

@app.route('/api/chapters/<int:chapter_id>', methods=['PUT'])
@token_required(admin_required=True)
def update_chapter(current_user, chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    chapter.name = data.get('name', chapter.name)
    chapter.description = data.get('description', chapter.description)
    
    db.session.commit()
    
    # Clear cache
    cache_delete('subjects_all')
    cache_delete(f'subject_{chapter.subject_id}')
    cache_delete(f'chapter_{chapter_id}')
    
    return jsonify({
        'message': 'Chapter updated successfully',
        'chapter': chapter.to_dict()
    }), 200

@app.route('/api/chapters/<int:chapter_id>', methods=['DELETE'])
@token_required(admin_required=True)
def delete_chapter(current_user, chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id
    
    db.session.delete(chapter)
    db.session.commit()
    
    # Clear cache
    cache_delete('subjects_all')
    cache_delete(f'subject_{subject_id}')
    cache_delete(f'chapter_{chapter_id}')
    
    return jsonify({'message': 'Chapter deleted successfully'}), 200

# Quiz APIs
@app.route('/api/chapters/<int:chapter_id>/quizzes', methods=['POST'])
@token_required(admin_required=True)
def create_quiz(current_user, chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'message': 'Quiz title is required'}), 400
    
    new_quiz = Quiz(
        title=data['title'],
        date_of_quiz=data.get('date_of_quiz', ''),
        time_duration=data.get('time_duration', ''),
        remarks=data.get('remarks', ''),
        chapter_id=chapter_id
    )
    
    db.session.add(new_quiz)
    db.session.commit()
    
    # Clear cache
    cache_delete(f'chapter_{chapter_id}')
    
    return jsonify({
        'message': 'Quiz created successfully',
        'quiz': new_quiz.to_dict()
    }), 201

@app.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
@token_required()
def get_quiz(current_user, quiz_id):
    cache_key = f'quiz_{quiz_id}_user_{current_user.id}'
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return jsonify(cached_data), 200
    
    quiz = Quiz.query.get_or_404(quiz_id)
    data = quiz.to_dict()
    
    # Don't include correct answers for regular users taking the quiz
    if not current_user.is_admin:
        for question in data['questions']:
            question.pop('correct_option', None)
    
    cache_set(cache_key, data, 60)  # Cache for 1 minute for active quizzes
    return jsonify(data), 200

@app.route('/api/quizzes/<int:quiz_id>', methods=['PUT'])
@token_required(admin_required=True)
def update_quiz(current_user, quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    quiz.title = data.get('title', quiz.title)
    quiz.date_of_quiz = data.get('date_of_quiz', quiz.date_of_quiz)
    quiz.time_duration = data.get('time_duration', quiz.time_duration)
    quiz.remarks = data.get('remarks', quiz.remarks)
    
    db.session.commit()
    
    # Clear cache
    cache_delete(f'chapter_{quiz.chapter_id}')
    cache_delete(f'quiz_{quiz_id}_user_{current_user.id}')
    
    return jsonify({
        'message': 'Quiz updated successfully',
        'quiz': quiz.to_dict()
    }), 200

@app.route('/api/quizzes/<int:quiz_id>', methods=['DELETE'])
@token_required(admin_required=True)
def delete_quiz(current_user, quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id
    
    db.session.delete(quiz)
    db.session.commit()
    
    # Clear cache
    cache_delete(f'chapter_{chapter_id}')
    cache_delete(f'quiz_{quiz_id}_user_{current_user.id}')
    
    return jsonify({'message': 'Quiz deleted successfully'}), 200

# Question APIs
@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['POST'])
@token_required(admin_required=True)
def create_question(current_user, quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    print(data)
    if not data or not data.get('question_statement'):
        return jsonify({'message': 'Question statement is required'}), 400
    
    new_question = Question(
        question_statement=data['question_statement'],
        option1=data.get('option1', ''),
        option2=data.get('option2', ''),
        option3=data.get('option3', ''),
        option4=data.get('option4', ''),
        correct_option=int(data.get('correct_option', 1)),
        quiz_id=quiz_id
    )
    
    db.session.add(new_question)
    db.session.commit()
    
    # Clear cache
    cache_delete(f'quiz_{quiz_id}_user_{current_user.id}')
    
    return jsonify({
        'message': 'Question created successfully',
        'question': new_question.to_dict(include_answer=True)
    }), 201

@app.route('/api/questions/<int:question_id>', methods=['PUT'])
@token_required(admin_required=True)
def update_question(current_user, question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    question.question_statement = data.get('question_statement', question.question_statement)
    question.option1 = data.get('option1', question.option1)
    question.option2 = data.get('option2', question.option2)
    question.option3 = data.get('option3', question.option3)
    question.option4 = data.get('option4', question.option4)
    question.correct_option = int(data.get('correct_option', question.correct_option))
    
    db.session.commit()
    
    # Clear cache
    cache_delete(f'quiz_{question.quiz_id}_user_{current_user.id}')
    
    return jsonify({
        'message': 'Question updated successfully',
        'question': question.to_dict(include_answer=True)
    }), 200

@app.route('/api/questions/<int:question_id>', methods=['DELETE'])
@token_required(admin_required=True)
def delete_question(current_user, question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    
    db.session.delete(question)
    db.session.commit()
    
    # Clear cache
    cache_delete(f'quiz_{quiz_id}_user_{current_user.id}')
    
    return jsonify({'message': 'Question deleted successfully'}), 200

@app.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
@token_required()
def submit_quiz(current_user, quiz_id):
    if current_user.is_admin:
        return jsonify({'message': 'Admins cannot take quizzes'}), 403
    
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    if not data or 'answers' not in data:
        return jsonify({'message': 'Answers are required'}), 400
    
    user_answers = data['answers']  # Format: {question_id: selected_option}
    score = 0
    total_questions = len(quiz.questions)
    results = []
    
    for question in quiz.questions:
        user_answer = user_answers.get(str(question.id))
        is_correct = user_answer and int(user_answer) == question.correct_option
        
        if is_correct:
            score += 1
        
        results.append({
            'question_id': question.id,
            'question_statement': question.question_statement,
            'user_answer': user_answer,
            'correct_answer': question.correct_option,
            'is_correct': is_correct
        })
    
    if total_questions > 0:
        new_score = Score(
            user_id=current_user.id,
            quiz_id=quiz_id,
            score=score,
            total_questions=total_questions,
            results=results
        )
        db.session.add(new_score)
        db.session.commit()
        
        # Invalidate user dashboard and scores cache
        cache_delete(f'user_dashboard_{current_user.id}')
        cache_delete(f'user_scores_{current_user.id}')
        
        return jsonify({
            'message': 'Quiz submitted successfully',
            'score': score,
            'total_questions': total_questions,
            'percentage': round((score / total_questions) * 100, 2),
            'results': results,
            'score_id': new_score.id
        }), 200
    
    return jsonify({'message': 'Quiz has no questions'}), 400

# @app.route('/api/users/<int:user_id>/scores', methods=['GET'])
# @token_required()
# def get_user_scores(current_user, user_id):
#     if current_user.id != user_id and not current_user.is_admin:
#         return jsonify({'message': 'Unauthorized to view these scores'}), 403
    
#     cache_key = f'user_scores_{user_id}'
#     cached_data = cache_get(cache_key)
    
#     if cached_data:
#         return jsonify(cached_data), 200
    
#     scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp.desc()).all()
#     data = [score.to_dict() for score in scores]
    
#     cache_set(cache_key, data, 180)  # Cache for 3 minutes
#     return jsonify(data), 200

@app.route('/api/user/scores', methods=['GET'])
@token_required()
def get_current_user_scores(current_user):
    cache_key = f'user_scores_{current_user.id}'
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return jsonify(cached_data), 200
    
    scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.timestamp.desc()).all()
    data = [score.to_dict() for score in scores]
    
    cache_set(cache_key, data, 180)  # Cache for 3 minutes
    return jsonify(data), 200

@app.route('/api/user/quizzes/<int:quiz_id>/results/<int:score_id>', methods=['GET'])
@token_required()
def get_quiz_results(current_user, quiz_id, score_id):
    if current_user.is_admin:
        return jsonify({'message': 'Admins cannot view quiz results'}), 403
    
    score = Score.query.get_or_404(score_id)
    if score.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized to view this score'}), 403
    
    quiz = Quiz.query.get_or_404(quiz_id)
    if score.quiz_id != quiz_id:
        return jsonify({'message': 'Score does not match quiz'}), 400
    
    # Fetch user answers from the submit_quiz results (assuming stored in results)
    results = Score.query.filter_by(id=score_id).first().results or []
    
    return jsonify({
        'quiz': quiz.to_dict(),
        'score': score.to_dict(),
        'user_answers': {r['question_id']: r['user_answer'] for r in results if r['user_answer'] is not None}
    }), 200

@app.route('/api/dashboard/user', methods=['GET'])
@token_required()
def user_dashboard(current_user):
    if current_user.is_admin:
        return jsonify({'message': 'Use admin dashboard endpoint'}), 403
    
    cache_key = f'user_dashboard_{current_user.id}'
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return jsonify(cached_data), 200
    
    user_scores = Score.query.filter_by(user_id=current_user.id).all()
    total_attempts = len(user_scores)
    
    avg_score = 0
    if total_attempts > 0:
        total_percentage = sum(
            (s.score / s.total_questions) * 100 
            for s in user_scores if s.total_questions > 0
        )
        valid_attempts = sum(1 for s in user_scores if s.total_questions > 0)
        if valid_attempts > 0:
            avg_score = total_percentage / valid_attempts
    
    subjects = Subject.query.all()
    
    data = {
        'user': current_user.to_dict(),
        'subjects': [subject.to_dict() for subject in subjects],
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 2)
    }
    
    cache_set(cache_key, data, 300)  # Cache for 5 minutes
    return jsonify(data), 200

@app.route('/api/dashboard/admin', methods=['GET'])
@token_required(admin_required=True)
def admin_dashboard(current_user):
    cache_key = 'admin_dashboard'
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return jsonify(cached_data), 200
    
    # Score summary for all users
    score_summary = db.session.query(
        User.id,
        User.username,
        User.full_name,
        func.count(Score.id).label('total_attempts'),
        func.avg(Score.score * 100.0 / Score.total_questions).label('avg_score')
    ).join(Score, User.id == Score.user_id).group_by(User.id).all()
    
    print(score_summary)
    # Count of all entities
    subjects_count = Subject.query.count()
    chapters_count = Chapter.query.count()
    quizzes_count = Quiz.query.count()
    questions_count = Question.query.count()
    users_count = User.query.filter_by(is_admin=False).count()
    
    subjects = Subject.query.all()
    
    data = {
        'subjects': [subject.to_dict() for subject in subjects],
        'score_summary': [
            {
                'user_id': row.id,
                'username': row.username,
                'full_name': row.full_name,
                'total_attempts': row.total_attempts,
                'avg_score': round(row.avg_score, 2) if row.avg_score else 0
            } for row in score_summary
        ],
        'stats': {
            'subjects_count': subjects_count,
            'chapters_count': chapters_count,
            'quizzes_count': quizzes_count,
            'questions_count': questions_count,
            'users_count': users_count
        }
    }
    
    cache_set(cache_key, data, 600)  # Cache for 10 minutes
    return jsonify(data), 200

@app.route('/api/users/<int:user_id>/scores', methods=['GET'])
@token_required()
def get_user_scores(current_user, user_id):
    if current_user.id != user_id and not current_user.is_admin:
        return jsonify({'message': 'Unauthorized to view these scores'}), 403
    
    cache_key = f'user_scores_{user_id}'
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return jsonify(cached_data), 200
    
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp.desc()).all()
    data = [score.to_dict() for score in scores]
    
    cache_set(cache_key, data, 180)  # Cache for 3 minutes
    return jsonify(data), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required()
def get_user(current_user, user_id):
    if current_user.id != user_id and not current_user.is_admin:
        return jsonify({'message': 'Unauthorized to view this user'}), 403
    
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

from backend.tasks import export_quiz_csv

@app.route('/api/export', methods=['GET'])
@token_required(admin_required=True)
def data_export(current_user):
    export_quiz_csv()
    return jsonify({'message': 'CSV file exported initiated.'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'message': 'Bad request'}), 400

# Initialize app
def init_app():
    with app.app_context():
        db.create_all()
        create_admin()
        if Subject.query.count() == 0:
            seed_default_content()
        print("Database initialized")
        print("Admin user created (username: admin, password: 0000)")
        if redis_client:
            print("Redis connected successfully")
        else:
            print("Redis not available - caching disabled")

@app.route('/')
def index():
    return render_template('index.html')

from backend.worker import celery
from backend.tasks import *

if __name__ == '__main__':
    init_app()
    app.run(debug=True)
