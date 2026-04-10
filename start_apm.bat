@echo off
echo ========================================
echo Elastic APM Server Setup
echo ========================================
echo.

echo Installing Elastic APM...
pip install elastic-apm
if errorlevel 1 (
    echo ERROR: Failed to install elastic-apm
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting APM Server...
echo ========================================
echo.

echo Checking if Docker is running...
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop first.
    pause
    exit /b 1
)

echo.
echo Starting APM Server container...
docker run -d ^
  --name apm-server ^
  -p 8200:8200 ^
  --network host ^
  docker.elastic.co/apm/apm-server:8.11.0 ^
  -e -E output.elasticsearch.hosts=["http://localhost:9200"]

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start APM Server
    echo.
    echo Alternative: Use Elastic Cloud or install APM Server manually
    echo See: https://www.elastic.co/downloads/apm-server
    pause
    exit /b 1
)

echo.
echo ========================================
echo APM Server Started Successfully!
echo ========================================
echo.
echo APM Server: http://localhost:8200
echo.
echo Next Steps:
echo 1. Start your Django app: python manage.py runserver
echo 2. Use the application to generate data
echo 3. Open Kibana: http://localhost:5601
echo 4. Go to APM section
echo 5. Select "smart-locker-system" service
echo.
pause
