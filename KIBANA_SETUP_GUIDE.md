# Kibana Integration Guide - Complete Setup

## Overview

This guide shows you how to ship Django logs to Kibana for real-time monitoring.

---

## Method 1: Docker ELK Stack (Recommended)

### Prerequisites:
- Docker Desktop installed
- At least 4GB RAM available

### Step 1: Start ELK Stack

```bash
# Navigate to project directory
cd c:\Users\Mathan\Desktop\locker_system

# Start ELK services
docker-compose -f docker-compose-elk.yml up -d
```

This starts:
- **Elasticsearch** on port 9200
- **Kibana** on port 5601
- **Logstash** on port 5044

### Step 2: Verify Services

```bash
# Check if Elasticsearch is running
curl http://localhost:9200

# Check if Kibana is running
curl http://localhost:5601
```

### Step 3: Access Kibana

Open browser: **http://localhost:5601**

### Step 4: Install Filebeat (to ship logs)

**Windows (PowerShell as Administrator):**
```powershell
# Download Filebeat
Invoke-WebRequest -Uri "https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.11.0-windows-x86_64.zip" -OutFile "filebeat.zip"

# Extract
Expand-Archive -Path filebeat.zip -DestinationPath C:\Program Files\

# Rename folder
Rename-Item "C:\Program Files\filebeat-8.11.0-windows-x86_64" "filebeat"
```

### Step 5: Configure Filebeat

Create `C:\Program Files\filebeat\filebeat.yml`:

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - C:\Users\Mathan\Desktop\locker_system\logs\*.log
  json.keys_under_root: true
  json.add_error_key: true
  multiline.type: pattern
  multiline.pattern: '^[0-9]{4}-[0-9]{2}-[0-9]{2}'
  multiline.negate: true
  multiline.match: after

output.logstash:
  hosts: ["localhost:5044"]

# OR directly to Elasticsearch (simpler):
# output.elasticsearch:
#   hosts: ["http://localhost:9200"]
#   index: "locker-system-logs-%{+yyyy.MM.dd}"
```

### Step 6: Start Filebeat

```powershell
cd "C:\Program Files\filebeat"

# Install as service (optional)
.\install-service-filebeat.ps1

# Start Filebeat
Start-Service filebeat

# OR run in foreground for testing
.\filebeat.exe -e
```

### Step 7: Configure Kibana

1. **Open Kibana**: http://localhost:5601

2. **Create Index Pattern**:
   - Go to **Stack Management** → **Index Patterns**
   - Click **Create index pattern**
   - Pattern: `locker-system-logs-*`
   - Time field: `@timestamp`
   - Click **Create**

3. **View Logs**:
   - Go to **Discover**
   - Select your index pattern
   - See logs in real-time!

---

## Method 2: Elastic APM (Simplest - Recommended for Django)

This is the easiest method with minimal setup.

### Step 1: Install Elastic APM

```bash
pip install elastic-apm
```

### Step 2: Update Django Settings

**File:** `locker_system/settings.py`

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... other apps
    'elasticapm.contrib.django',
]
```

Add APM configuration:
```python
ELASTIC_APM = {
    'SERVICE_NAME': 'smart-locker-system',
    'SERVER_URL': 'http://localhost:8200',  # APM Server
    'SECRET_TOKEN': '',  # Optional
    'ENVIRONMENT': 'development',  # or 'production'
    'DEBUG': True,
}
```

Add middleware (at the TOP of MIDDLEWARE):
```python
MIDDLEWARE = [
    'elasticapm.contrib.django.middleware.TracingMiddleware',  # Add this FIRST
    # ... other middleware
]
```

### Step 3: Start APM Server

```bash
# Using Docker
docker run -d --name apm-server -p 8200:8200 docker.elastic.co/apm/apm-server:8.11.0 -e -E output.elasticsearch.hosts=["http://elasticsearch:9200"]
```

### Step 4: View in Kibana

1. Open Kibana: http://localhost:5601
2. Go to **APM** section
3. Select `smart-locker-system` service
4. See:
   - Transaction traces
   - Errors
   - Performance metrics
   - Logs

---

## Method 3: Direct JSON Logging to Elasticsearch (No Logstash)

Simplest approach without Filebeat/Logstash.

### Step 1: Install Elasticsearch Python Client

```bash
pip install elasticsearch
```

### Step 2: Create Elasticsearch Handler

Create `accounts/logging_handlers.py`:

```python
import logging
from elasticsearch import Elasticsearch
from datetime import datetime
import json

class ElasticsearchHandler(logging.Handler):
    def __init__(self, es_host='localhost', es_port=9200, index='locker-logs'):
        super().__init__()
        self.es = Elasticsearch([f'http://{es_host}:{es_port}'])
        self.index = index
    
    def emit(self, record):
        try:
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'module': record.module,
                'message': record.getMessage(),
                'pathname': record.pathname,
                'lineno': record.lineno,
            }
            
            if record.exc_info:
                log_entry['exception'] = self.format(record)
            
            self.es.index(index=self.index, document=log_entry)
        except Exception:
            self.handleError(record)
```

### Step 3: Add to Django Settings

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'elasticsearch': {
            '()': 'accounts.logging_handlers.ElasticsearchHandler',
            'es_host': 'localhost',
            'es_port': 9200,
            'index': 'locker-system-logs',
            'level': 'INFO',
        },
    },
    'loggers': {
        'accounts': {
            'handlers': ['console', 'file', 'elasticsearch'],
            'level': 'INFO',
        },
        'lockers': {
            'handlers': ['console', 'file', 'elasticsearch'],
            'level': 'INFO',
        },
        'reservations': {
            'handlers': ['console', 'file', 'elasticsearch'],
            'level': 'INFO',
        },
    },
}
```

---

## Quick Start - Method 1 (Docker ELK)

### All-in-One Commands:

```bash
# 1. Start ELK stack
cd c:\Users\Mathan\Desktop\locker_system
docker-compose -f docker-compose-elk.yml up -d

# 2. Wait 30 seconds for services to start
timeout /t 30

# 3. Check services
curl http://localhost:9200
curl http://localhost:5601

# 4. Start your Django app
python manage.py runserver

# 5. Generate some logs (use the app)

# 6. Open Kibana
# http://localhost:5601
```

### Kibana Setup (One-time):

1. **Open**: http://localhost:5601
2. **Go to**: Stack Management → Index Patterns
3. **Create**: Pattern `locker-system-logs-*`
4. **Time field**: `@timestamp`
5. **View logs**: Discover tab

---

## What You'll See in Kibana

### Log Examples:

**Authentication:**
```
INFO 2026-04-08 19:30:15 accounts.views User logged in: admin
WARNING 2026-04-08 19:30:20 accounts.serializers Failed login attempt for username: hacker
INFO 2026-04-08 19:30:25 accounts.serializers New user registered: john_doe with role: user
```

**Locker Operations:**
```
INFO 2026-04-08 19:31:00 lockers.views Admin admin created locker: A101
INFO 2026-04-08 19:31:05 lockers.views Admin admin updated locker: A101
INFO 2026-04-08 19:31:10 lockers.views Admin admin deactivated locker: B202
```

**Reservations:**
```
INFO 2026-04-08 19:32:00 reservations.serializers Reservation created: 1, User: john_doe, Locker: A101
INFO 2026-04-08 19:32:30 reservations.serializers Reservation released: 1, Locker: A101
```

**Cache:**
```
INFO 2026-04-08 19:33:00 lockers.views Cache miss - querying database for available lockers
INFO 2026-04-08 19:33:01 lockers.views Returning cached available lockers
```

### Kibana Features:

✅ **Real-time log streaming**  
✅ **Search and filter logs**  
✅ **Create dashboards**  
✅ **Set up alerts**  
✅ **Visualize error rates**  
✅ **Track user activity**  
✅ **Monitor performance**  

---

## Dashboard Examples

### 1. Authentication Dashboard
- Login success rate
- Failed login attempts
- New registrations over time
- Active users

### 2. Locker Operations Dashboard
- Lockers created/updated/deleted
- Most active admins
- Locker status distribution

### 3. Reservation Dashboard
- Reservations per hour/day
- Average reservation duration
- Most popular lockers
- Release rate

### 4. Error Dashboard
- Error count over time
- Errors by module
- Most common error messages
- Error trends

---

## Production Deployment

### Docker Compose for Production:

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=your_secure_password
    volumes:
      - es_data:/usr/share/elasticsearch/data
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=kibana_system
      - ELASTICSEARCH_PASSWORD=your_secure_password
    ports:
      - "5601:5601"

volumes:
  es_data:
```

### Environment Variables:

```bash
# .env file
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
KIBANA_HOST=localhost
KIBANA_PORT=5600
APM_SECRET_TOKEN=your_secret_token
```

---

## Troubleshooting

### Elasticsearch Not Starting:
```bash
# Check Docker logs
docker logs elasticsearch

# Increase memory limit
# Docker Desktop → Settings → Resources → Memory: 4GB+
```

### Kibana Can't Connect:
```bash
# Check if Elasticsearch is ready
curl http://localhost:9200

# Restart Kibana
docker restart kibana
```

### No Logs in Kibana:
```bash
# Check Filebeat status
Get-Service filebeat

# Check Filebeat logs
Get-Content "C:\Program Files\filebeat\logs\filebeat"

# Test log file exists
dir C:\Users\Mathan\Desktop\locker_system\logs\
```

---

## Summary

### Easiest Method: Elastic APM
```bash
pip install elastic-apm
# Update settings.py
# Start APM server
# View in Kibana APM section
```

### Most Flexible: Docker ELK + Filebeat
```bash
docker-compose -f docker-compose-elk.yml up -d
# Install Filebeat
# Configure filebeat.yml
# View in Kibana Discover
```

### Custom: Direct to Elasticsearch
```bash
pip install elasticsearch
# Create custom handler
# Add to LOGGING config
# View in Kibana
```

**Choose the method that best fits your needs!** 🎉
