"""
Lecture Service
Business logic for lecture management
"""
from bson import ObjectId
from datetime import datetime
import logging

from models.lecture import Lecture, StudentQuestion
from models.user import User

logger = logging.getLogger(__name__)


class LectureService:
    """Service for managing lectures and student questions"""
    
    def __init__(self, db):
        """
        Initialize lecture service
        
        Args:
            db: MongoDB database instance
        """
        self.db = db
        self.lectures = db.lectures
        self.questions = db.student_questions

    def verify_and_get_user(self, session_id):
        try:
            user =  User.find_by_active_session(self.db, session_id)
            if user is None:
                raise ValueError('Session is not active')
            return user
        except Exception as e:
            raise e
    
    def create_lecture(self, session_id, course_name, semester_start, semester_end,
                      class_sessions, lecture_days):
        """
        Create a new lecture
        
        Args:
            session_id: User session ID (string)
            course_name: Name of the course
            semester_start: Start date (YYYY-MM-DD)
            semester_end: End date (YYYY-MM-DD)
            class_sessions: List of class session objects
            lecture_days: List of generated lecture day objects
            
        Returns:
            Created lecture document
        """
        user = self.verify_and_get_user(session_id)
        try:
            # Validate class sessions
            for session in class_sessions:
                if not Lecture.validate_class_session(session):
                    raise ValueError(f"Invalid class session: {session}")
            
            # Validate lecture days
            for day in lecture_days:
                if not Lecture.validate_lecture_day(day):
                    raise ValueError(f"Invalid lecture day: {day}")
            
            # Create lecture document
            lecture_doc = Lecture.create(
                lecturer_id=user['_id'],
                course_name=course_name,
                semester_start=semester_start,
                semester_end=semester_end,
                class_sessions=class_sessions,
                lecture_days=lecture_days
            )
            
            # Insert into database
            result = self.lectures.insert_one(lecture_doc)
            lecture_doc['_id'] = result.inserted_id
            
            logger.info(f"Created lecture: {result.inserted_id} for lecturer: {user['_id']}")
            
            return Lecture.to_json(lecture_doc)
            
        except Exception as e:
            logger.error(f"Error creating lecture: {str(e)}")
            raise
    
    def get_lectures_by_lecturer(self, session_id):
        """
        Get all lectures for a specific lecturer
        
        Args:
            session_id: Lecturer's user ID (string)
            
        Returns:
            List of lecture documents
        """
        user = self.verify_and_get_user(session_id)
        try:
            lectures = list(self.lectures.find({'lecturerId': user['_id']}))
            return [Lecture.to_json(lecture) for lecture in lectures]
        except Exception as e:
            logger.error(f"Error fetching lectures for session {session_id}: {str(e)}")
            raise
    
    def get_lecture_by_id(self, session_id, lecture_id):
        """
        Get a specific lecture by ID
        
        Args:
            lecture_id: Lecture ID (string)
            session_id: Session ID (string)
            
        Returns:
            Lecture document or None
        """
        self.verify_and_get_user(session_id)
        try:
            lecture = self.lectures.find_one({'_id': ObjectId(lecture_id)})
            return Lecture.to_json(lecture) if lecture else None
        except Exception as e:
            logger.error(f"Error fetching lecture {lecture_id}: {str(e)}")
            raise
    
    def update_lecture(self, session_id, lecture_id, updates):
        self.verify_and_get_user(session_id)
        """
        Update a lecture
        
        Args:
            lecture_id: Lecture ID (string)
            session_id: Session ID (string)
            updates: Dictionary of fields to update
            
        Returns:
            Updated lecture document or None
        """
        self.verify_and_get_user(session_id)
        try:
            # Add updatedAt timestamp
            updates['updatedAt'] = datetime.utcnow()
            
            # Validate class sessions if provided
            if 'classSessions' in updates:
                for session in updates['classSessions']:
                    if not Lecture.validate_class_session(session):
                        raise ValueError(f"Invalid class session: {session}")
            
            # Validate lecture days if provided
            if 'lectureDays' in updates:
                for day in updates['lectureDays']:
                    if not Lecture.validate_lecture_day(day):
                        raise ValueError(f"Invalid lecture day: {day}")
            
            result = self.lectures.find_one_and_update(
                {'_id': ObjectId(lecture_id)},
                {'$set': updates},
                return_document=True
            )
            
            logger.info(f"Updated lecture: {lecture_id}")
            
            return Lecture.to_json(result) if result else None

        except Exception as e:
            logger.error(f"Error updating lecture {lecture_id}: {str(e)}")
            raise
    
    def update_lecture_day(self, session_id, lecture_id,day_id, day_updates):
        """
        Update a specific lecture day within a lecture
        
        Args:
            lecture_id: Lecture ID (string)
            session_id: Session ID (string)
            day_id: Lecture day ID (string)
            day_updates: Dictionary of day fields to update
            
        Returns:
            Updated lecture document or None
        """
        self.verify_and_get_user(session_id)
        try:
            # Validate timeline items if provided
            if 'timeline' in day_updates and day_updates['timeline']:
                for item in day_updates['timeline']:
                    if not Lecture.validate_timeline_item(item):
                        raise ValueError(f"Invalid timeline item: {item}")

            # Find the lecture
            lecture = self.lectures.find_one({'_id': ObjectId(lecture_id)})
            if not lecture:
                return None
            
            # Update the specific day
            lecture_days = lecture.get('lectureDays', [])
            day_found = False
            
            for day in lecture_days:
                if day.get('id') == day_id:
                    day.update(day_updates)
                    day_found = True
                    break
            
            if not day_found:
                raise ValueError(f"Lecture day {day_id} not found")
            
            # Update the lecture
            result = self.lectures.find_one_and_update(
                {'_id': ObjectId(lecture_id)},
                {
                    '$set': {
                        'lectureDays': lecture_days,
                        'updatedAt': datetime.utcnow()
                    }
                },
                return_document=True
            )
            
            logger.info(f"Updated lecture day {day_id} in lecture {lecture_id}")
            
            return Lecture.to_json(result) if result else None
            
        except Exception as e:
            logger.error(f"Error updating lecture day: {str(e)}")
            raise
    
    def delete_lecture(self, session_id, lecture_id):
        """
        Delete a lecture (with verification that it belongs to the lecturer)
        
        Args:
            lecture_id: Lecture ID (string)
            session_id: Lecturer's user ID (string)
            
        Returns:
            Boolean indicating success
        """
        user = self.verify_and_get_user(session_id)
        try:
            result = self.lectures.delete_one({
                '_id': ObjectId(lecture_id),
                'lecturerId': user['_id']
            })
            
            if result.deleted_count > 0:
                # Also delete associated questions
                self.questions.delete_many({'lectureId': lecture_id})
                logger.info(f"Deleted lecture: {lecture_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting lecture {lecture_id}: {str(e)}")
            raise
    
    # Student Questions
    
    def create_question(self, lecture_id, student_name, question_text):
        """
        Create a student question
        
        Args:
            lecture_id: Lecture ID (string)
            student_name: Student's name
            question_text: Question content
            
        Returns:
            Created question document
        """
        try:
            question_doc = StudentQuestion.create(
                lecture_id=lecture_id,
                student_name=student_name,
                question=question_text
            )
            
            result = self.questions.insert_one(question_doc)
            question_doc['_id'] = result.inserted_id
            
            logger.info(f"Created question for lecture: {lecture_id}")
            
            return StudentQuestion.to_json(question_doc)
            
        except Exception as e:
            logger.error(f"Error creating question: {str(e)}")
            raise
    
    def get_questions_by_lecture(self, session_id, lecture_id):
        """
        Get all questions for a specific lecture
        
        Args:
            lecture_id: Lecture ID (string)
            session_id: Session ID (string)
            
        Returns:
            List of question documents
        """
        self.verify_and_get_user(session_id)
        try:
            questions = list(self.questions.find({'lectureId': lecture_id}))
            return [StudentQuestion.to_json(q) for q in questions]
        except Exception as e:
            logger.error(f"Error fetching questions for lecture {lecture_id}: {str(e)}")
            raise
    
    def get_unanswered_questions_count(self, session_id):
        """
        Get count of unanswered questions for all lecturer's lectures
        
        Args:
            session_id: User's session id (string)
            
        Returns:
            Count of unanswered questions
        """
        user = self.verify_and_get_user(session_id)
        try:
            # Get all lectures for this lecturer
            lectures = list(self.lectures.find(
                {'lecturerId': user['_id']},
                {'_id': 1}
            ))
            lecture_ids = [str(lecture['_id']) for lecture in lectures]
            
            # Count unanswered questions
            count = self.questions.count_documents({
                'lectureId': {'$in': lecture_ids},
                'isAnswered': False
            })
            
            return count
            
        except Exception as e:
            logger.error(f"Error counting questions: {str(e)}")
            raise
    
    def mark_question_answered(self, session_id, question_id):
        """
        Mark a question as answered
        
        Args:
            session_id: User's session id (string)
            question_id: Question ID (string)
            
        Returns:
            Boolean indicating success
        """
        self.verify_and_get_user(session_id)
        try:
            result = self.questions.update_one(
                {'_id': ObjectId(question_id)},
                {'$set': {'isAnswered': True}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error marking question {question_id} as answered: {str(e)}")
            raise
