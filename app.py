import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path

app = Flask(__name__)
app.secret_key = "student_marks_project_secret"

DB_PATH = Path(__file__).with_name("student_marks.db")
SUBJECTS = ["Software Engineering", "Web Engineering", "Database Systems", "Networking", "Project Management"]
MAX_MARK_PER_SUBJECT = 100

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE,
            email TEXT,
            department TEXT,
            level TEXT,
            mark1 INTEGER NOT NULL,
            mark2 INTEGER NOT NULL,
            mark3 INTEGER NOT NULL,
            mark4 INTEGER NOT NULL,
            mark5 INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            grade TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if count == 0:
        demo_students = [
            ("Ziyad Ali Alghadban", "SE-101", "ziyad@example.com", "Software Engineering", "Level 7", 95, 91, 88, 93, 90),
            ("Mohammed Khalid", "SE-102", "mohammed@example.com", "Software Engineering", "Level 7", 82, 79, 85, 80, 84),
            ("Abdulaziz Ahmed", "SE-103", "abdulaziz@example.com", "Software Engineering", "Level 6", 70, 74, 68, 77, 72),
        ]
        for full_name, roll_number, email, department, level, *marks in demo_students:
            total, percentage, grade, status = calculate_result(marks)
            conn.execute("""
                INSERT INTO students
                (full_name, roll_number, email, department, level, mark1, mark2, mark3, mark4, mark5, total, percentage, grade, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (full_name, roll_number, email, department, level, *marks, total, percentage, grade, status))
    conn.commit()
    conn.close()

def calculate_result(marks):
    total = sum(marks)
    percentage = round(total / len(marks), 2) if marks else 0
    if percentage >= 90: grade = "A+"
    elif percentage >= 80: grade = "A"
    elif percentage >= 70: grade = "B"
    elif percentage >= 60: grade = "C"
    elif percentage >= 50: grade = "D"
    else: grade = "F"
    status = "Pass" if percentage >= 50 else "Fail"
    return total, percentage, grade, status

def read_marks(form):
    marks = []
    for i in range(1, 6):
        try:
            mark = int(form.get(f"mark{i}", 0))
        except ValueError:
            mark = 0
        marks.append(mark)
    return marks

@app.route("/")
def dashboard():
    search = request.args.get("search", "").strip()
    conn = get_db_connection()
    if search:
        students = conn.execute(
            "SELECT * FROM students WHERE roll_number LIKE ? OR full_name LIKE ? ORDER BY id DESC",
            (f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
        students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    stats = conn.execute("SELECT COUNT(*) AS total_students, AVG(percentage) AS avg_percentage FROM students").fetchone()
    conn.close()
    return render_template("dashboard.html", students=students, stats=stats, search=search)

@app.route("/student/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        roll_number = request.form.get("roll_number", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        level = request.form.get("level", "").strip()
        marks = read_marks(request.form)

        if not full_name or not roll_number:
            flash("Student name and roll number are required.", "danger")
            return render_template("student_form.html", subjects=SUBJECTS, student=request.form, mode="add")

        total, percentage, grade, status = calculate_result(marks)
        conn = get_db_connection()
        try:
            conn.execute("""
                INSERT INTO students
                (full_name, roll_number, email, department, level, mark1, mark2, mark3, mark4, mark5, total, percentage, grade, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (full_name, roll_number, email, department, level, *marks, total, percentage, grade, status))
            conn.commit()
            flash("Student record added successfully.", "success")
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            flash("Roll number already exists.", "danger")
        finally:
            conn.close()
    return render_template("student_form.html", subjects=SUBJECTS, student=None, mode="add")

@app.route("/student/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not student:
        conn.close()
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        marks = read_marks(request.form)
        total, percentage, grade, status = calculate_result(marks)
        conn.execute("""
            UPDATE students SET full_name=?, roll_number=?, email=?, department=?, level=?,
            mark1=?, mark2=?, mark3=?, mark4=?, mark5=?, total=?, percentage=?, grade=?, status=?
            WHERE id=?
        """, (request.form.get("full_name"), request.form.get("roll_number"), request.form.get("email"), 
              request.form.get("department"), request.form.get("level"), *marks, total, percentage, grade, status, student_id))
        conn.commit()
        conn.close()
        flash("Student record updated successfully.", "success")
        return redirect(url_for("dashboard"))
    conn.close()
    return render_template("student_form.html", subjects=SUBJECTS, student=student, mode="edit")

@app.route("/student/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    flash("Student record deleted.", "info")
    return redirect(url_for("dashboard"))

@app.route("/student/<int:student_id>")
def view_result(student_id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    conn.close()
    return render_template("result.html", student=student, subjects=SUBJECTS)

# التعديل الجوهري هنا ليتوافق مع Render
if __name__ == "__main__":
    init_db()
    # السيرفر هو من يحدد المنفذ تلقائياً
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
