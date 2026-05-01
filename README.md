# Student Marks Management System - Easy Demo Version

This version is prepared for quick project demonstration.

## What changed
- No login page and no password required.
- No MySQL setup required.
- Uses SQLite automatically.
- Database is created automatically when the app starts.
- Demo student records are inserted automatically the first time.
- The website opens directly on the dashboard.

## How to run
Double-click:

```text
run.bat
```

Or run manually:

```bash
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## Project Features
- Add student records
- Edit student records
- Delete student records
- Search by student name or roll number
- Enter marks for five subjects
- Automatic total, percentage, grade, and pass/fail status
- Final result page
- Professional dashboard design

## Project Files
- `app.py` - Flask backend using SQLite
- `templates/` - HTML pages
- `static/` - CSS and JavaScript
- `student_marks.db` - created automatically
- `Project_Report.pdf` - project report
- `Presentation_Demo.pptx` - presentation slides
