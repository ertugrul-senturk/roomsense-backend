# 🚀 Flask Backend Integration Guide

## 📦 What's Included

Your Flask backend now has complete lecture management functionality!

### New Files Added:
1. **models/lecture.py** - Lecture and StudentQuestion models
2. **services/lecture_service.py** - Business logic for lectures
3. **routes/lecture_routes.py** - API endpoints
4. **app.py** (updated) - Integrated lecture routes

### Updated Files:
- **app.py** - Added lecture service and routes initialization

---

## 🎯 API Endpoints

### Lectures
- `POST /api/lectures/` - Create lecture
- `GET /api/lectures/lecturer/<lecturer_id>` - Get all lectures
- `GET /api/lectures/<lecture_id>` - Get single lecture  
- `PUT /api/lectures/<lecture_id>` - Update lecture
- `DELETE /api/lectures/<lecture_id>?lecturerId=<id>` - Delete lecture
- `PUT /api/lectures/<lecture_id>/day/<day_id>` - Update lecture day

### Questions
- `POST /api/lectures/<lecture_id>/questions` - Create question
- `GET /api/lectures/<lecture_id>/questions` - Get questions
- `GET /api/lectures/lecturer/<lecturer_id>/questions/unanswered/count` - Count unanswered
- `PUT /api/lectures/questions/<question_id>/answer` - Mark answered

---

## 🔧 Setup Instructions

### 1. Start Flask Backend

```bash
cd flask-backend

# Install dependencies (if needed)
pip install -r requirements.txt

# Run the app
python app.py
```

Backend runs on: **http://localhost:8061**

### 2. Verify Backend is Running

```bash
curl http://localhost:8061/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-27T10:00:00.000Z"
}
```

### 3. Test Lecture API

```bash
# Create a lecture
curl -X POST http://localhost:8061/api/lectures/ \
  -H "Content-Type: application/json" \
  -d '{
    "lecturerId": "lecturer-test123",
    "courseName": "Test Course",
    "semesterStartDate": "2024-01-15",
    "semesterEndDate": "2024-05-15",
    "classSessions": [{
      "id": "1",
      "dayOfWeek": "Monday",
      "startTime": "14:00",
      "endTime": "15:15"
    }],
    "lectureDays": [{
      "id": "session-2024-01-15",
      "date": "2024-01-15",
      "dayOfWeek": "Monday",
      "startTime": "14:00",
      "endTime": "15:15"
    }]
  }'

# Get all lectures for lecturer
curl http://localhost:8061/api/lectures/lecturer/lecturer-test123
```

---

## 📱 Frontend Integration

### Option 1: Use Provided API Client (Recommended)

File: `complete-app/lib/api.ts`

```typescript
import { lectureApi } from '@/lib/api';

// Create lecture
const result = await lectureApi.createLecture(lectureData);

// Get lectures
const lectures = await lectureApi.getLecturerLectures(lecturerId);

// Update lecture
await lectureApi.updateLecture(lectureId, updates);

// Delete lecture
await lectureApi.deleteLecture(lectureId, lecturerId);
```

### Option 2: Direct Fetch Calls

```typescript
// Create lecture
const response = await fetch('http://localhost:8061/api/lectures/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(lectureData)
});
const data = await response.json();
```

---

## 🔄 Migration from localStorage

### Before (localStorage):
```typescript
const stored = localStorage.getItem(`lectures-${lecturerId}`);
const lectures = JSON.parse(stored);
```

### After (API):
```typescript
const result = await lectureApi.getLecturerLectures(lecturerId);
const lectures = result.data;
```

---

## 🗄️ MongoDB Collections

### `lectures` Collection
```javascript
{
  _id: ObjectId("..."),
  lecturerId: "lecturer-12345",
  courseName: "Computer Science 101",
  semesterStartDate: "2024-01-15",
  semesterEndDate: "2024-05-15",
  classSessions: [...],
  lectureDays: [...],
  createdAt: ISODate("..."),
  updatedAt: ISODate("...")
}
```

### `student_questions` Collection
```javascript
{
  _id: ObjectId("..."),
  lectureId: "6927ce6884017ad767e0534a",
  studentName: "Alice",
  question: "What is recursion?",
  isAnswered: false,
  createdAt: ISODate("...")
}
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` in flask-backend:

```bash
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/roomsense
PORT=8061
```

### Frontend Environment

Create `.env.local` in complete-app:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8061/api
```

---

## 🧪 Testing

### 1. Test Create Lecture
```bash
curl -X POST http://localhost:8061/api/lectures/ \
  -H "Content-Type: application/json" \
  -d @test-lecture.json
```

### 2. Test Get Lectures
```bash
curl http://localhost:8061/api/lectures/lecturer/lecturer-12345
```

### 3. Test Update Day
```bash
curl -X PUT http://localhost:8061/api/lectures/<lecture-id>/day/<day-id> \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Variables",
    "timeline": [...],
    "notes": "Great class"
  }'
```

### 4. Test Student Question
```bash
curl -X POST http://localhost:8061/api/lectures/<lecture-id>/questions \
  -H "Content-Type: application/json" \
  -d '{
    "studentName": "Alice",
    "question": "What is recursion?"
  }'
```

---

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check if port is in use
lsof -i :8061

# Kill process if needed
kill -9 <PID>

# Restart
python app.py
```

### MongoDB Connection Issues
```bash
# Check MongoDB is running
sudo systemctl status mongod

# Start if needed
sudo systemctl start mongod
```

### CORS Errors
Backend has CORS enabled. If still having issues, check browser console.

### 404 Not Found
Ensure you're using correct endpoint:
- ✅ `http://localhost:8061/api/lectures/`
- ❌ `http://localhost:8061/lectures/`

---

## 📚 Complete API Documentation

See `API_DOCUMENTATION.md` for:
- All endpoints with examples
- Request/response formats
- Error codes
- Testing with cURL

---

## 🔐 Security Notes

### Production Checklist:
- [ ] Add authentication middleware
- [ ] Validate lecturer owns lecture before edit/delete
- [ ] Rate limiting on question submissions
- [ ] Input sanitization
- [ ] HTTPS only
- [ ] Environment variables for secrets
- [ ] Database connection pooling

---

## 📊 File Structure

```
flask-backend/
├── app.py                      ← Main Flask app (updated)
├── models/
│   ├── lecture.py             ← NEW: Lecture models
│   ├── user.py
│   └── verification.py
├── services/
│   ├── lecture_service.py     ← NEW: Lecture business logic
│   ├── auth_service.py
│   └── email_service.py
├── routes/
│   ├── lecture_routes.py      ← NEW: Lecture endpoints
│   ├── auth_routes.py
│   └── session_routes.py
├── config/
│   └── config.py
├── requirements.txt
└── API_DOCUMENTATION.md       ← NEW: Full API docs
```

---

## 🎯 Quick Start Summary

```bash
# 1. Start backend
cd flask-backend
python app.py

# 2. In another terminal, start frontend
cd complete-app
npm run dev

# 3. Test in browser
http://localhost:3000
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Backend runs on port 8061
- [ ] /health endpoint returns 200
- [ ] Can create a lecture via API
- [ ] Can retrieve lectures
- [ ] Can update lecture day
- [ ] Can submit student question
- [ ] Frontend connects to backend
- [ ] No CORS errors

---

## 🎉 You're Ready!

Your Flask backend now has:
✅ Complete lecture management
✅ Student questions system
✅ MongoDB integration
✅ RESTful API
✅ Error handling
✅ Validation
✅ Documentation

**Next steps:** Update your Next.js frontend to use the API instead of localStorage!
