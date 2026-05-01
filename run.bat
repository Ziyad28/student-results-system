@echo off
cd /d %~dp0
echo Starting Student Marks Management System...
echo.
echo First time only: installing required packages.
python -m pip install -r requirements.txt
cls
echo Opening website automatically...
echo Do not close this window while presenting the project.
python app.py
pause
