@echo off
echo ========================================
echo Kibana ELK Stack Setup
echo ========================================
echo.

echo This will start Elasticsearch, Kibana, and Logstash
echo Make sure Docker Desktop is running!
echo.
pause

echo Starting ELK Stack...
docker-compose -f docker-compose-elk.yml up -d

echo.
echo Waiting for services to start (30 seconds)...
timeout /t 30

echo.
echo Checking services...
echo.

echo Testing Elasticsearch...
curl -s http://localhost:9200
if errorlevel 1 (
    echo ERROR: Elasticsearch not running!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ELK Stack Started Successfully!
echo ========================================
echo.
echo Services:
echo   Elasticsearch: http://localhost:9200
echo   Kibana:        http://localhost:5601
echo   Logstash:      localhost:5044
echo.
echo Next Steps:
echo 1. Open Kibana: http://localhost:5601
echo 2. Create index pattern: locker-system-logs-*
echo 3. View logs in Discover tab
echo.
echo See KIBANA_SETUP_GUIDE.md for detailed instructions
echo.
pause
