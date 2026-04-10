# Elastic APM Setup - Quick Start Guide

## ✅ What's Already Done

I've already configured your Django app for Elastic APM:

1. ✅ Added `elasticapm.contrib.django` to INSTALLED_APPS
2. ✅ Added APM middleware to MIDDLEWARE
3. ✅ Configured ELASTIC_APM settings
4. ✅ Added elastic-apm to requirements.txt
5. ✅ Created `start_apm.bat` script

---

## 🚀 Step-by-Step Setup

### Step 1: Install Elastic APM

```bash
pip install elastic-apm
```

**OR just run:**
```bash
start_apm.bat
```

---

### Step 2: Start Elasticsearch & Kibana

You need Elasticsearch running for APM to work.

**Option A: Using Docker (Recommended)**
```bash
# Start just Elasticsearch
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# Start Kibana
docker run -d --name kibana --link elasticsearch:elasticsearch -p 5601:5600 docker.elastic.co/kibana/kibana:8.11.0
```

**Option B: Use the ELK docker-compose**
```bash
docker-compose -f docker-compose-elk.yml up -d
```

**Verify Elasticsearch is running:**
```bash
curl http://localhost:9200
```

You should see:
```json
{
  "name" : "...",
  "cluster_name" : "...",
  "version" : {
    "number" : "8.11.0"
  }
}
```

---

### Step 3: Start APM Server

```bash
# Using the script
start_apm.bat

# OR manually
docker run -d --name apm-server -p 8200:8200 docker.elastic.co/apm/apm-server:8.11.0 -e -E output.elasticsearch.hosts=["http://localhost:9200"]
```

**Verify APM Server is running:**
```bash
curl http://localhost:8200
```

---

### Step 4: Start Your Django App

```bash
python manage.py runserver
```

You should see in the console:
```
INFO 2026-04-08 elasticapm APM Server connection established
```

---

### Step 5: Generate Some Data

Use your application to create some activity:

1. **Login** as admin (admin/admin123)
2. **Create** a few lockers
3. **Register** a new user
4. **Reserve** and **release** lockers
5. **Edit** some lockers

This generates APM data that will be sent to Kibana.

---

### Step 6: View in Kibana

1. **Open Kibana**: http://localhost:5601

2. **Go to APM**:
   - Click on the menu (☰) in top-left
   - Click on **APM** under "Observability"

3. **Select Your Service**:
   - Click on `smart-locker-system`
   - You'll see:
     - **Transactions** - All API requests
     - **Errors** - Any errors that occurred
     - **Service Map** - Visual diagram

4. **Explore**:
   - Click on any transaction to see details
   - View response times
   - See database queries
   - Check error stack traces

---

## 📊 What You'll See in Kibana APM

### 1. Services Tab
```
smart-locker-system
├── Transactions: 150
├── Errors: 3
├── Avg Response Time: 45ms
└── Throughput: 10 req/min
```

### 2. Transactions
Shows all your API endpoints:
```
POST /api/auth/login/        - 120ms avg
POST /api/auth/register/     - 95ms avg
GET  /api/lockers/           - 35ms avg
POST /api/lockers/           - 50ms avg
GET  /api/lockers/available/ - 25ms avg (cached)
POST /api/reservations/      - 80ms avg
PUT  /api/reservations/:id/release/ - 65ms avg
```

### 3. Errors
Any errors with full stack traces:
```
ValidationError - Registration failed
  File: accounts/views.py, line 25
  User: anonymous
  Time: 2026-04-08 19:30:15

ConnectionError - Redis not available
  File: lockers/views.py, line 100
  User: admin
  Time: 2026-04-08 19:31:20
```

### 4. Performance Metrics
- Response time percentiles (p50, p95, p99)
- Database query times
- Cache hit/miss rates
- Throughput over time

### 5. Service Map
Visual diagram showing:
```
[Client] → [Django App] → [PostgreSQL]
                        → [Redis]
                        → [Elasticsearch]
```

---

## 🎯 APM Features You Get

### Automatic Tracking:
✅ All HTTP requests (endpoints, response times)  
✅ Database queries (SQL statements, duration)  
✅ Cache operations (Redis commands)  
✅ Errors with stack traces  
✅ Request/response sizes  
✅ User agent information  

### Django-Specific:
✅ View function names  
✅ URL patterns  
✅ Template rendering times  
✅ Middleware performance  
✅ ORM query counts  

### Custom Tracking (Optional):

You can add custom tracking to your code:

```python
from elasticapm import capture_span, label

# Track custom operations
@capture_span("create_locker")
def create_locker(request):
    # Your code here
    label("locker_number", "A101")
    label("admin_user", request.user.username)
```

---

## 🔧 Configuration Options

### Current Settings (in settings.py):

```python
ELASTIC_APM = {
    'SERVICE_NAME': 'smart-locker-system',  # Your app name
    'SERVER_URL': 'http://localhost:8200',  # APM Server
    'SECRET_TOKEN': '',                     # Optional security token
    'ENVIRONMENT': 'development',           # dev/staging/production
    'DEBUG': True,                          # Enable debug mode
}
```

### Production Settings:

```python
ELASTIC_APM = {
    'SERVICE_NAME': 'smart-locker-system',
    'SERVER_URL': 'https://apm.yourdomain.com:8200',
    'SECRET_TOKEN': 'your-secret-token-here',
    'ENVIRONMENT': 'production',
    'DEBUG': False,
    'RECORDING': True,  # Enable/disable data collection
    'ENABLED': True,    # Enable/disable APM completely
}
```

---

## 📈 Example Kibana Dashboards

### 1. API Performance Dashboard

**Metrics:**
- Average response time by endpoint
- Requests per minute
- Error rate percentage
- P95 response time

**Visualizations:**
```
Response Time Over Time (Line Chart)
├── POST /api/auth/login/    - 120ms
├── GET /api/lockers/        - 35ms
└── POST /api/reservations/  - 80ms

Top Slowest Endpoints (Table)
├── POST /api/auth/login/    - 120ms avg
├── POST /api/reservations/  - 80ms avg
└── PUT /api/lockers/:id/    - 65ms avg
```

### 2. Error Monitoring Dashboard

**Metrics:**
- Errors over time
- Errors by type
- Most affected endpoints
- User impact

**Alerts:**
- Error rate > 5%
- Response time > 500ms
- Database query > 100ms

### 3. User Activity Dashboard

**Metrics:**
- Active users over time
- Login success rate
- Most active admins
- Reservation patterns

---

## 🚨 Setting Up Alerts

In Kibana, you can set up alerts:

1. **Go to**: Stack Management → Rules and Connectors
2. **Create Rule**:
   - **Name**: High Error Rate
   - **Condition**: Error count > 10 in 5 minutes
   - **Action**: Send email/Slack notification

**Example Alerts:**
- 🔴 Error rate exceeds 5%
- 🟡 Average response time > 200ms
- 🔵 New user registrations spike
- ⚠️ Cache miss rate > 50%

---

## 🐛 Troubleshooting

### APM Server Not Connecting:

```bash
# Check APM Server logs
docker logs apm-server

# Restart APM Server
docker restart apm-server

# Check if Elasticsearch is running
curl http://localhost:9200
```

### No Data in Kibana:

1. **Check Django logs** for APM connection messages
2. **Generate some traffic** - use the app
3. **Wait 1-2 minutes** for data to appear
4. **Check APM Server**:
   ```bash
   curl http://localhost:8200
   ```

### High Memory Usage:

```bash
# Stop APM Server when not needed
docker stop apm-server

# Start again when needed
docker start apm-server
```

---

## 📝 Testing the Setup

### Quick Test:

```bash
# 1. Start services
docker start elasticsearch
docker start kibana
docker start apm-server

# 2. Start Django
python manage.py runserver

# 3. Make some requests
curl http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 4. Check Kibana
# http://localhost:5601 → APM → smart-locker-system
```

---

## 🎓 What Makes APM Better Than Regular Logs?

### Regular Logs:
```
INFO User logged in: admin
ERROR Database connection failed
```

### APM Data:
```
Transaction: POST /api/auth/login/
├── Duration: 120ms
├── Database Queries: 3 (45ms total)
├── Cache Hits: 2
├── User Agent: Mozilla/5.0
├── IP: 192.168.1.100
├── Response Size: 675 bytes
└── Stack Trace: (if error)
    File: accounts/views.py, line 25
    Function: LoginView.post()
```

**APM gives you the complete picture!** 🎯

---

## 📚 Next Steps

1. ✅ **Install elastic-apm**: `pip install elastic-apm`
2. ✅ **Start Elasticsearch**: `docker run ...`
3. ✅ **Start APM Server**: `start_apm.bat`
4. ✅ **Start Django**: `python manage.py runserver`
5. ✅ **Use the app**: Generate some data
6. ✅ **Open Kibana**: http://localhost:5601
7. ✅ **Explore APM**: View transactions, errors, metrics

---

## 🎉 Summary

**What's Configured:**
- ✅ Django APM middleware
- ✅ Automatic request tracking
- ✅ Database query monitoring
- ✅ Error tracking with stack traces
- ✅ Performance metrics
- ✅ Service map visualization

**What You Need to Do:**
1. Install elastic-apm package
2. Start Elasticsearch & APM Server
3. Use your application
4. View data in Kibana APM section

**Ready to monitor your app like a pro!** 🚀
