from backend.models import User, Score, Quiz, Chapter, Subject
from backend.worker import celery
from datetime import datetime
from celery.schedules import crontab
import csv
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_mail(receiver, subject, message, content="text", attachment=None):
    msg = MIMEMultipart()
    msg['From'] = "support@quizapp.com"
    msg['To'] = receiver
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment:
        with open(attachment, 'rb') as attachment_:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_.read())
            
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
        encoders.encode_base64(part)
        msg.attach(part)

    server = smtplib.SMTP(host="localhost", port=1025)
    server.login("support@quizapp.com", "")
    server.send_message(msg)
    server.quit()
    return 'The mail sent successfully !!'

@celery.task
def send_daily_reminder():
    users = User.query.filter_by(is_admin=False).all()
    for user in users:
        last_score = Score.query.filter_by(user_id=user.id).order_by(Score.timestamp.desc()).first()
        if not last_score or (datetime.utcnow() - last_score.timestamp).days > 1:
            subject = "Reminder: Take a Quiz Today!"
            message = f"""
            Dear {user.full_name or user.username},

            It looks like you haven't taken a quiz recently. Visit our Quiz System to test your knowledge on various subjects!

            Best regards,
            The Quiz System Team
            """
            try:
                send_mail(user.username, subject, message, content="text")
                print(f"Reminder sent to {user.username}")
            except Exception as e:
                print(f"Failed to send reminder to {user.username}: {str(e)}")

@celery.task
def generate_monthly_report():
    users = User.query.filter_by(is_admin=False).all()
    for user in users:
        scores = Score.query.filter_by(user_id=user.id).join(
            Quiz
        ).join(
            Chapter, Quiz.chapter_id == Chapter.id
        ).join(
            Subject, Chapter.subject_id == Subject.id
        ).all()
        
        if not scores:
            continue  # Skip users with no quiz scores
        
        # Generate HTML report with detailed score table
        score_rows = ""
        total_score = 0
        total_questions = 0
        for score in scores:
            total_score += score.score
            total_questions += score.total_questions
            score_rows += f"""
            <tr>
                <td>{score.id}</td>
                <td>{score.quiz.title}</td>
                <td>{score.quiz.chapter.subject.name}</td>
                <td>{score.quiz.chapter.name}</td>
                <td>{score.timestamp.isoformat()}</td>
                <td>{score.score}/{score.total_questions}</td>
                <td>{round((score.score / score.total_questions) * 100, 2) if score.total_questions > 0 else 0,}%</td>
            </tr>
            """
        
        report = f"""
        <html>
        <head>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                h1, h2 {{ font-family: Arial, sans-serif; }}
            </style>
        </head>
        <body>
            <h1>Monthly Quiz Report for {user.full_name or user.username}</h1>
            <h2>Summary</h2>
            <p>Total Quizzes Taken: {len(scores)}</p>
            <p>Average Score: {round(total_score/max(total_questions,1)*100, 2)}%</p>
            <h2>Quiz Details</h2>
            <table>
                <tr>
                    <th>Score ID</th>
                    <th>Quiz Title</th>
                    <th>Subject</th>
                    <th>Chapter</th>
                    <th>Date Taken</th>
                    <th>Score</th>
                    <th>Percentage</th>
                </tr>
                {score_rows}
            </table>
        </body>
        </html>
        """
        
        try:
            send_mail(
                user.username,
                f"Monthly Quiz Report - {datetime.utcnow().strftime('%B %Y')}",
                report,
                content="html"
            )
            print(f"Monthly report sent to {user.username}")
        except Exception as e:
            print(f"Failed to send report to {user.username}: {str(e)}")
    
    return {'status': 'success', 'message': 'Monthly reports sent to all users'}

@celery.task
def export_quiz_csv():
    scores = Score.query.join(
        Quiz
    ).join(
        Chapter, Quiz.chapter_id == Chapter.id
    ).join(
        Subject, Chapter.subject_id == Subject.id
    ).join(
        User, Score.user_id == User.id
    ).all()
    
    # Define CSV file path
    output_dir = 'exports'
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(output_dir, f'quiz_data_{timestamp}.csv')
    
    # Write to CSV
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Score ID', 'Username', 'Quiz Title', 'Subject', 'Chapter', 'Date Taken', 'Score', 'Total Questions', 'Percentage'])
        for score in scores:
            writer.writerow([
                score.id,
                score.user.username,
                score.quiz.title,
                score.quiz.chapter.subject.name,
                score.quiz.chapter.name,
                score.timestamp.isoformat(),
                score.score,
                score.total_questions,
                round((score.score / score.total_questions) * 100, 2) if score.total_questions > 0 else 0,
            ])
    
    # Send username with CSV attachment
    try:
        send_mail(
            "admin@quizapp.com",
            "Your Quiz Data Export",
            f"Dear Admin,\n\nAttached is your quiz score data in CSV format.\n\nBest regards,\nThe Quiz System Team",
            content="text",
            attachment=file_path
        )
        print(f"CSV exported and sent to admin@quizapp.com")
        return {'status': 'success', 'message': f'CSV exported to {file_path} and sent to admin@quizapp.com'}
    except Exception as e:
        print(f"Failed to send CSV to admin@quizapp.com: {str(e)}")
        return {'status': 'error', 'message': str(e)}

# Schedule tasks
celery.conf.beat_schedule = {
    'daily-reminder': {
        'task': 'backend.tasks.send_daily_reminder',
        'schedule': crontab(hour=22, minute=41),  
    },
    'monthly-report': {
        'task': 'backend.tasks.generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),  
    },
}