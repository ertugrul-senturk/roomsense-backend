# RoomSense Lecture Management API Documentation

## Base URL
```
http://localhost:8061/api
```

## Endpoints

### 1. Create Lecture
Create a new lecture for a lecturer.

**Endpoint:** `POST /lectures/`

**Request Body:**
```json
{
  "lecturerId": "lecturer-sessionId",
  "courseName": "Computer Science 101",
  "semesterStartDate": "2024-01-15",
  "semesterEndDate": "2024-05-15",
  "classSessions": [
    {
      "id": "1",
      "dayOfWeek": "Monday",
      "startTime": "14:00",
      "endTime": "15:15"
    },
    {
      "id": "2",
      "dayOfWeek": "Wednesday",
      "startTime": "14:00",
      "endTime": "15:15"
    }
  ],
  "lectureDays": [
    {
      "id": "session-2024-01-15",
      "date": "2024-01-15",
      "dayOfWeek": "Monday",
      "startTime": "14:00",
      "endTime": "15:15"
    }
    // ... more generated days
  ]
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "lecture": {
    "id": "6927ce6884017ad767e0534a",
    "lecturerId": "lecturer-sessionId",
    "courseName": "Computer Science 101",
    "semesterStartDate": "2024-01-15",
    "semesterEndDate": "2024-05-15",
    "classSessions": [...],
    "lectureDays": [...],
    "createdAt": "2025-11-27T10:00:00.000Z",
    "updatedAt": "2025-11-27T10:00:00.000Z"
  }
}
```

---

### 2. Get Lecturer's Lectures
Get all lectures for a specific lecturer.

**Endpoint:** `GET /lectures/lecturer/:lecturerId`

**Example:** `GET /lectures/lecturer/lecturer-12345`

**Response:** `200 OK`
```json
{
  "success": true,
  "lectures": [
    {
      "id": "6927ce6884017ad767e0534a",
      "lecturerId": "lecturer-12345",
      "courseName": "Computer Science 101",
      "semesterStartDate": "2024-01-15",
      "semesterEndDate": "2024-05-15",
      "classSessions": [...],
      "lectureDays": [...],
      "createdAt": "2025-11-27T10:00:00.000Z",
      "updatedAt": "2025-11-27T10:00:00.000Z"
    }
  ]
}
```

---

### 3. Get Single Lecture
Get a specific lecture by ID.

**Endpoint:** `GET /lectures/:lectureId`

**Example:** `GET /lectures/6927ce6884017ad767e0534a`

**Response:** `200 OK`
```json
{
  "success": true,
  "lecture": {
    "id": "6927ce6884017ad767e0534a",
    "lecturerId": "lecturer-12345",
    "courseName": "Computer Science 101",
    ...
  }
}
```

---

### 4. Update Lecture
Update an existing lecture (edit functionality).

**Endpoint:** `PUT /lectures/:lectureId`

**Request Body:**
```json
{
  "courseName": "Updated Course Name",
  "semesterStartDate": "2024-01-20",
  "semesterEndDate": "2024-05-20",
  "classSessions": [
    {
      "id": "1",
      "dayOfWeek": "Tuesday",
      "startTime": "15:00",
      "endTime": "16:15"
    }
  ],
  "lectureDays": [...]
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "lecture": {
    "id": "6927ce6884017ad767e0534a",
    "courseName": "Updated Course Name",
    ...
  }
}
```

---

### 5. Delete Lecture
Delete a lecture (with lecturer verification).

**Endpoint:** `DELETE /lectures/:lectureId?lecturerId=lecturer-12345`

**Query Parameters:**
- `lecturerId` (required): Lecturer's ID for verification

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Lecture deleted successfully"
}
```

---

### 6. Update Lecture Day
Update a specific lecture day (add topic, timeline, notes).

**Endpoint:** `PUT /lectures/:lectureId/day/:dayId`

**Request Body:**
```json
{
  "topic": "Variables and Data Types",
  "timeline": [
    {
      "id": "1",
      "startTime": "14:00",
      "endTime": "14:30",
      "description": "Review homework from last class"
    },
    {
      "id": "2",
      "startTime": "14:30",
      "endTime": "15:15",
      "description": "Lecture on variables"
    }
  ],
  "notes": "Students had great questions about type conversion"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "lecture": {
    "id": "6927ce6884017ad767e0534a",
    "lectureDays": [
      {
        "id": "session-2024-01-15",
        "date": "2024-01-15",
        "topic": "Variables and Data Types",
        "timeline": [...],
        "notes": "Students had great questions..."
      }
    ]
  }
}
```

---

### 7. Create Student Question
Submit a question from a student.

**Endpoint:** `POST /lectures/:lectureId/questions`

**Request Body:**
```json
{
  "studentName": "Alice Johnson",
  "question": "What is the difference between var and let?"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "question": {
    "id": "abc123...",
    "lectureId": "6927ce6884017ad767e0534a",
    "studentName": "Alice Johnson",
    "question": "What is the difference between var and let?",
    "isAnswered": false,
    "createdAt": "2025-11-27T10:30:00.000Z"
  }
}
```

---

### 8. Get Lecture Questions
Get all questions for a specific lecture.

**Endpoint:** `GET /lectures/:lectureId/questions`

**Response:** `200 OK`
```json
{
  "success": true,
  "questions": [
    {
      "id": "abc123...",
      "lectureId": "6927ce6884017ad767e0534a",
      "studentName": "Alice Johnson",
      "question": "What is the difference between var and let?",
      "isAnswered": false,
      "createdAt": "2025-11-27T10:30:00.000Z"
    }
  ]
}
```

---

### 9. Get Unanswered Questions Count
Get count of unanswered questions for a lecturer.

**Endpoint:** `GET /lectures/lecturer/:lecturerId/questions/unanswered/count`

**Response:** `200 OK`
```json
{
  "success": true,
  "count": 5
}
```

---

### 10. Mark Question as Answered
Mark a student question as answered.

**Endpoint:** `PUT /lectures/questions/:questionId/answer`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Question marked as answered"
}
```

---

## Error Responses

All error responses follow this format:

**400 Bad Request**
```json
{
  "success": false,
  "message": "Missing required fields: courseName"
}
```

**404 Not Found**
```json
{
  "success": false,
  "message": "Lecture not found"
}
```

**500 Internal Server Error**
```json
{
  "success": false,
  "message": "Failed to create lecture"
}
```

---

## MongoDB Collections

### `lectures` Collection
```javascript
{
  _id: ObjectId("6927ce6884017ad767e0534a"),
  lecturerId: "lecturer-12345",
  courseName: "Computer Science 101",
  semesterStartDate: "2024-01-15",
  semesterEndDate: "2024-05-15",
  classSessions: [
    {
      id: "1",
      dayOfWeek: "Monday",
      startTime: "14:00",
      endTime: "15:15"
    }
  ],
  lectureDays: [
    {
      id: "session-2024-01-15",
      date: "2024-01-15",
      dayOfWeek: "Monday",
      startTime: "14:00",
      endTime: "15:15",
      topic: "Variables and Data Types", // optional
      notes: "Great class", // optional
      timeline: [ // optional
        {
          id: "1",
          startTime: "14:00",
          endTime: "14:30",
          description: "Review"
        }
      ]
    }
  ],
  createdAt: ISODate("2025-11-27T10:00:00.000Z"),
  updatedAt: ISODate("2025-11-27T10:00:00.000Z")
}
```

### `student_questions` Collection
```javascript
{
  _id: ObjectId("..."),
  lectureId: "6927ce6884017ad767e0534a",
  studentName: "Alice Johnson",
  question: "What is recursion?",
  isAnswered: false,
  createdAt: ISODate("2025-11-27T10:30:00.000Z")
}
```

---

## Testing with cURL

### Create Lecture
```bash
curl -X POST http://localhost:8061/api/lectures/ \
  -H "Content-Type: application/json" \
  -d '{
    "lecturerId": "lecturer-12345",
    "courseName": "CS 101",
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
```

### Get Lecturer's Lectures
```bash
curl http://localhost:8061/api/lectures/lecturer/lecturer-12345
```

### Create Question
```bash
curl -X POST http://localhost:8061/api/lectures/6927ce6884017ad767e0534a/questions \
  -H "Content-Type: application/json" \
  -d '{
    "studentName": "Alice",
    "question": "What is recursion?"
  }'
```

---

## Next.js Integration

Replace localStorage calls with API calls. See `FRONTEND_INTEGRATION.md` for details.
