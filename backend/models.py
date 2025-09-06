from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    scores = db.relationship('Score', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'qualification': self.qualification,
            'dob': self.dob,
            'is_admin': self.is_admin
        }

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'chapters': [chapter.to_dict() for chapter in self.chapters]
        }

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else None,
            'quizzes': [quiz.to_dict() for quiz in self.quizzes]
        }

# class Quiz(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_of_quiz = db.Column(db.String(20))
#     time_duration = db.Column(db.String(10))
#     remarks = db.Column(db.Text)
#     chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
#     questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
#     scores = db.relationship('Score', backref='quiz', lazy=True, cascade="all, delete-orphan")

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'title': self.title,
#             'date_of_quiz': self.date_of_quiz,
#             'time_duration': self.time_duration,
#             'remarks': self.remarks,
#             'chapter_id': self.chapter_id,
#             'chapter_name': self.chapter.name if self.chapter else None,
#             'subject_name': self.chapter.subject.name if self.chapter and self.chapter.subject else None,
#             'subject_id': self.chapter.subject.id if self.chapter and self.chapter.subject else None,
#             'questions': [question.to_dict() for question in self.questions]
#         }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    option3 = db.Column(db.Text)
    option4 = db.Column(db.Text)
    correct_option = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    def to_dict(self, include_answer=False):
        data = {
            'id': self.id,
            'question_statement': self.question_statement,
            'option1': self.option1,
            'option2': self.option2,
            'option3': self.option3,
            'option4': self.option4,
            'quiz_id': self.quiz_id
        }
        if include_answer:
            data['correct_option'] = self.correct_option
        return data

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    results = db.Column(db.JSON, nullable=True)  # Store results JSON

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'quiz_id': self.quiz_id,
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': round((self.score / self.total_questions) * 100, 2) if self.total_questions > 0 else 0,
            'timestamp': self.timestamp.isoformat(),
            'quiz_title': self.quiz.title if self.quiz else None,
            'chapter_name': self.quiz.chapter.name if self.quiz and self.quiz.chapter else None,
            'subject_name': self.quiz.chapter.subject.name if self.quiz and self.quiz.chapter and self.quiz.chapter.subject else None,
            'results': self.results or []  # Include results for quiz results endpoint
        }

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_of_quiz = db.Column(db.String(20))
    time_duration = db.Column(db.String(10))
    remarks = db.Column(db.Text)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date_of_quiz': self.date_of_quiz,
            'time_duration': self.time_duration,
            'remarks': self.remarks,
            'chapter_id': self.chapter_id,
            'chapter_name': self.chapter.name if self.chapter else None,
            'subject_id': self.chapter.subject.id if self.chapter and self.chapter.subject else None,
            'subject_name': self.chapter.subject.name if self.chapter and self.chapter.subject else None,
            'questions': [question.to_dict(include_answer=True) for question in self.questions]
        }