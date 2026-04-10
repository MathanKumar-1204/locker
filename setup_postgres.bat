@echo off
echo ========================================
echo Setup PostgreSQL Database
echo ========================================
echo.

echo Step 1: Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo Migrations completed successfully!
echo.

echo Step 2: Creating admin user...
python manage.py create_admin
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Database: PostgreSQL (Supabase)
echo Admin Credentials:
echo Username: admin
echo Password: admin123
echo Role: admin
echo.
echo To start the server, run:
echo   python manage.py runserver
echo.
pause
