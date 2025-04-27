-- Student table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

-- Quiz tabe
CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    num_questions INTEGER NOT NULL,
    quiz_date TEXT NOT NULL
);

-- Result table
CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
);

-- Insert student
INSERT INTO students (first_name, last_name) VALUES ('John', 'Smith');

-- Insert quiz
INSERT INTO quizzes (subject, num_questions, quiz_date)
VALUES ('Python Basics', 5, '2015-02-05');

-- Insert result (assume John Smith is ID 1 and the quiz is ID 1)
INSERT INTO results (student_id, quiz_id, score)
VALUES (1, 1, 85);