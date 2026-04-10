# Quick Start Guide - Smart Locker System

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python manage.py migrate
python manage.py create_admin
```

### Step 3: Run Server
```bash
python manage.py runserver
```

Open your browser and visit: **http://localhost:8000**

---

## 🔑 Default Admin Credentials

- **Username**: admin
- **Password**: admin123

---

## 📋 Quick Test Checklist

### 1. Login as Admin
- Use the admin credentials above
- You should see the Admin Panel tab

### 2. Create Lockers
- Go to "Admin Panel" tab
- Create a few lockers with different locations
- Example:
  - Locker Number: A101
  - Location: Building A - Floor 1
  - Size: Medium

### 3. Register a New User
- Logout from admin
- Click "Register" tab
- Create a new user account

### 4. Test Reservation Flow
- Login as the new user
- View available lockers
- Click "Reserve" on an available locker
- Check "My Reservations" tab
- Release the locker

---

## 🎯 Key Features to Test

### User Features
✅ Register and login
✅ View available lockers (cached with Redis)
✅ Reserve a locker
✅ View own reservations
✅ Release locker

### Admin Features
✅ All user features
✅ Create new lockers
✅ Update locker details
✅ Deactivate lockers
✅ View all reservations

---

## 🔧 Troubleshooting

### Redis Not Running?
The available lockers endpoint will still work but won't be cached.
To enable caching, start Redis:
```bash
redis-server
```

### Database Issues?
Reset the database:
```bash
# Delete the database file (Windows)
Remove-Item db.sqlite3

# Re-run migrations
python manage.py migrate
python manage.py create_admin
```

### Can't Login?
Make sure you ran:
```bash
python manage.py create_admin
```

---

## 📱 Access the Application

- **Web UI**: http://localhost:8000
- **API Base**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin (Django admin)

---

## 🎨 UI Features

The web interface includes:
- Modern gradient design
- Responsive layout (works on mobile)
- Real-time statistics dashboard
- Tab-based navigation
- Color-coded locker status
- One-click reservation
- User role badges

---

## 📝 API Testing with cURL

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","name":"Test User","password":"testpass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Create Locker (with token)
```bash
curl -X POST http://localhost:8000/api/lockers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"locker_number":"A101","location":"Building A","size":"medium","status":"available"}'
```

### Get Available Lockers
```bash
curl -X GET http://localhost:8000/api/lockers/available/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Reserve Locker
```bash
curl -X POST http://localhost:8000/api/reservations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"locker_id": 1}'
```

---

## 🎉 You're All Set!

Enjoy testing the Smart Locker Management System!

For detailed documentation, see README.md
