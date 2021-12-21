from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hw13.db'
db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Quizzes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    num = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)

    def __init__(self, subject, num, date):
        self.subject = subject
        self.num = num
        self.date = date


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String, nullable=False)
    quiz = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, student, quiz, score):
        self.student = student
        self.quiz = quiz
        self.score = score


@app.route('/', methods=['POST', 'GET'])
def index():
        return render_template("index.html",)

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    students = Students.query.order_by(Students.id)
    quizzes = Quizzes.query.order_by(Quizzes.id)
    scores = Scores.query.order_by(Scores.id)
    return render_template("dashboard.html", students=students, quizzes=quizzes, scores=scores)


@app.route('/addstudent', methods=['POST', 'GET'])
def addstudent():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        new_student = Students(first_name=first_name, last_name=last_name)
        db.session.add(new_student)
        db.session.commit()
        return redirect('/addstudent')
    else:
        return render_template("addstudent.html",)


@app.route('/addquiz', methods=['POST', 'GET'])
def addquiz():
    if request.method == 'POST':
        subject = request.form['subject']
        num = request.form['num']
        date = request.form['date']
        new_quiz = Quizzes(subject=subject, num=num, date=date)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect('/addquiz')
    else:
        return render_template("addquiz.html",)


@app.route('/addgrade', methods=['POST', 'GET'])
def addgrade():
    if request.method == 'POST':
        student = request.form['student']
        quiz = request.form['quiz']
        score = request.form['score']
        new_grade = Scores(student=student, quiz=quiz, score=score)
        db.session.add(new_grade)
        db.session.commit()
        return redirect('/addgrade')
    else:
        students = Students.query.order_by(Students.id)
        quizzes = Quizzes.query.order_by(Quizzes.id)
        return render_template("addgrade.html", students=students, quizzes=quizzes)


if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.run(debug=True)
