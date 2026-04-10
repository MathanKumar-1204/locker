@echo off
echo ========================================
echo Smart Locker System - Setup Script
echo ========================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo Step 2: Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo Migrations completed successfully!
echo.

echo Step 3: Creating admin user...
python manage.py create_admin
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Admin Credentials:
echo Username: admin
echo Password: admin123
echo.
echo To start the server, run:
echo   python manage.py runserver
echo.
echo Then open your browser to:
echo   http://localhost:8000
echo.
pause
