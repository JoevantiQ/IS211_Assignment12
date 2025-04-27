from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for session management

DATABASE = 'hw13.db'

# Helper function to get DB connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

# -------- ROUTES -------- #

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username or password!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# Dashboard page
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()
    return render_template('dashboard.html', students=students, quizzes=quizzes)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------------- #

# Add a student
@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if not first_name or not last_name:
            flash('All fields are required!', 'error')
            return render_template('add_student.html')

        conn = get_db_connection()
        conn.execute('INSERT INTO students (first_name, last_name) VALUES (?, ?)',
                     (first_name, last_name))
        conn.commit()
        conn.close()

        flash('Student added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_student.html')

# Add a quiz
@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        quiz_date = request.form['quiz_date']

        if not subject or not num_questions or not quiz_date:
            flash('All fields are required!', 'error')
            return render_template('add_quiz.html')

        conn = get_db_connection()
        conn.execute('INSERT INTO quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)',
                     (subject, num_questions, quiz_date))
        conn.commit()
        conn.close()

        flash('Quiz added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_quiz.html')

# View a student's quiz results
@app.route('/student/<int:student_id>')
def view_student_results(student_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    results = conn.execute('''
        SELECT quizzes.subject, quizzes.quiz_date, results.score
        FROM results
        JOIN quizzes ON results.quiz_id = quizzes.id
        WHERE results.student_id = ?
    ''', (student_id,)).fetchall()
    conn.close()

    return render_template('view_results.html', student=student, results=results)

# Add a student's quiz result
@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        score = request.form['score']

        if not student_id or not quiz_id or not score:
            flash('All fields are required!', 'error')
            students = conn.execute('SELECT * FROM students').fetchall()
            quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
            conn.close()
            return render_template('add_result.html', students=students, quizzes=quizzes)

        conn.execute('INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)',
                     (student_id, quiz_id, score))
        conn.commit()
        conn.close()

        flash('Result added successfully!', 'success')
        return redirect(url_for('dashboard'))

    students = conn.execute('SELECT * FROM students').fetchall()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()

    return render_template('add_result.html', students=students, quizzes=quizzes)


if __name__ == '__main__':
    app.run(debug=True)
