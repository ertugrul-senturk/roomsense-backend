"""
Lecture Model
MongoDB schema for lectures
"""
from datetime import datetime
from bson import ObjectId

class Lecture:
    """Lecture model with validation"""
    
    @staticmethod
    def create(key, lecturer_id, course_name, semester_start, semester_end, class_sessions, lecture_days):
        """
        Create a new lecture document
        
        Args:
            key (str): The key of the lecture
            lecturer_id: MongoDB ObjectId of the lecturer
            course_name: Name of the course
            semester_start: Start date (YYYY-MM-DD)
            semester_end: End date (YYYY-MM-DD)
            class_sessions: List of class session objects
            lecture_days: List of generated lecture day objects
            
        Returns:
            Dictionary representing a lecture document
        """
        return {
            'key': key,
            'lecturerId': lecturer_id,
            'courseName': course_name,
            'semesterStartDate': semester_start,
            'semesterEndDate': semester_end,
            'classSessions': class_sessions,
            'lectureDays': lecture_days,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
    
    @staticmethod
    def validate_class_session(session):
        """Validate a class session object"""
        required_fields = ['dayOfWeek', 'startTime', 'endTime']
        return all(field in session for field in required_fields)
    
    @staticmethod
    def validate_lecture_day(day):
        """Validate a lecture day object"""
        required_fields = ['date', 'dayOfWeek', 'startTime', 'endTime']
        return all(field in day for field in required_fields)
    
    @staticmethod
    def validate_timeline_item(item):
        """Validate a timeline item"""
        required_fields = ['startTime', 'endTime', 'description']
        if not all(field in item for field in required_fields):
            return False
        # Ensure end time is after start time
        return item['endTime'] > item['startTime']
    
    @staticmethod
    def to_json(lecture):
        """Convert lecture document to JSON-serializable format"""
        if lecture is None:
            return None
        
        lecture_copy = lecture.copy()
        
        # Convert ObjectId to string
        if '_id' in lecture_copy:
            lecture_copy['id'] = str(lecture_copy['_id'])
            del lecture_copy['_id']
        
        # Convert lecturerId to string if it's ObjectId
        if 'lecturerId' in lecture_copy and isinstance(lecture_copy['lecturerId'], ObjectId):
            lecture_copy['lecturerId'] = str(lecture_copy['lecturerId'])
        
        # Convert datetime to ISO format
        if 'createdAt' in lecture_copy:
            lecture_copy['createdAt'] = lecture_copy['createdAt'].isoformat()
        if 'updatedAt' in lecture_copy:
            lecture_copy['updatedAt'] = lecture_copy['updatedAt'].isoformat()
        
        return lecture_copy




class StudentQuestion:
    """Student Question model"""

    @staticmethod
    def create(lecture_key, student_name, question):
        """
        Create a new student question document

        Args:
            lecture_key: Lecture key
            student_name: Name of the student
            question: Question text

        Returns:
            Dictionary representing a question document
        """
        return {
            'lectureKey': lecture_key,
            'studentName': student_name,
            'question': question,
            'isAnswered': False,
            'createdAt': datetime.utcnow(),
            # new fields for advanced polling logic
            'isDelivered': False,
            'deliveredAt': None
        }

    @staticmethod
    def to_json(question):
        """Convert question document to JSON-serializable format"""
        if question is None:
            return None

        question_copy = question.copy()

        # Convert ObjectId to string
        if '_id' in question_copy:
            question_copy['id'] = str(question_copy['_id'])
            del question_copy['_id']

        # Convert lectureId to string if it's ObjectId
        if 'lectureId' in question_copy and isinstance(question_copy['lectureId'], ObjectId):
            question_copy['lectureId'] = str(question_copy['lectureId'])

        # Convert datetime to ISO format
        if 'createdAt' in question_copy and isinstance(question_copy['createdAt'], datetime):
            question_copy['createdAt'] = question_copy['createdAt'].isoformat()

        if 'deliveredAt' in question_copy and isinstance(question_copy['deliveredAt'], datetime):
            question_copy['deliveredAt'] = question_copy['deliveredAt'].isoformat()

        return question_copy
