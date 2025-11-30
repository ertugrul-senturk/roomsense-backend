"""
Lecture Routes
API endpoints for lecture management
"""
from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)


def init_lecture_routes(lecture_service):
    """
    Initialize lecture routes blueprint
    
    Args:
        lecture_service: LectureService instance
        
    Returns:
        Flask blueprint
    """
    blueprint = Blueprint('lectures', __name__, url_prefix='/api/lectures')
    
    # ==================== LECTURE ENDPOINTS ====================
    
    @blueprint.route('/', methods=['POST'])
    def create_lecture():
        """
        Create a new lecture
        
        Request body:
        {
            "lecturerId": "lecturer-sessionId",
            "courseName": "Course Name",
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
        }
        """
        try:
            data = request.get_json()

            
            # Validate required fields
            required_fields = ['sessionId', 'courseName', 'semesterStartDate',
                             'semesterEndDate', 'classSessions', 'lectureDays']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'message': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400
            
            # Create lecture
            lecture = lecture_service.create_lecture(
                session_id=data['sessionId'],
                course_name=data['courseName'],
                semester_start=data['semesterStartDate'],
                semester_end=data['semesterEndDate'],
                class_sessions=data['classSessions'],
                lecture_days=data['lectureDays']
            )
            
            return jsonify({
                'success': True,
                'lecture': lecture
            }), 201
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            logger.error(f"Error creating lecture: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to create lecture'
            }), 500
    
    @blueprint.route('/lecturer/<session_id>', methods=['GET'])
    def get_lecturer_lectures(session_id):
        """
        Get all lectures for a specific lecturer
        
        Returns all lectures belonging to the lecturer
        """
        try:
            lectures = lecture_service.get_lectures_by_lecturer(session_id)
            
            return jsonify({
                'success': True,
                'lectures': lectures
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching lectures: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to fetch lectures'
            }), 500
    
    @blueprint.route('/<session_id>/<lecture_key>', methods=['GET'])
    def get_lecture(session_id, lecture_key):
        """
        Get a specific lecture by ID
        """
        try:
            lecture = lecture_service.get_lecture_by_key(session_id, lecture_key)
            
            if not lecture:
                return jsonify({
                    'success': False,
                    'message': 'Lecture not found'
                }), 404
            
            return jsonify({
                'success': True,
                'lecture': lecture
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching lecture: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to fetch lecture'
            }), 500
    
    @blueprint.route('/<session_id>/<lecture_key>', methods=['PUT'])
    def update_lecture(session_id, lecture_key):
        """
        Update a lecture
        
        Request body can include:
        {
            "courseName": "Updated Name",
            "semesterStartDate": "2024-01-15",
            "semesterEndDate": "2024-05-15",
            "classSessions": [...],
            "lectureDays": [...]
        }
        """
        try:
            data = request.get_json()
            
            # Remove fields that shouldn't be updated directly
            data.pop('lecturerId', None)
            data.pop('createdAt', None)
            data.pop('_id', None)
            data.pop('key', None)
            data.pop('id', None)
            
            lecture = lecture_service.update_lecture(session_id, lecture_key, data)
            
            if not lecture:
                return jsonify({
                    'success': False,
                    'message': 'Lecture not found'
                }), 404
            
            return jsonify({
                'success': True,
                'lecture': lecture
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            logger.error(f"Error updating lecture: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to update lecture'
            }), 500
    
    @blueprint.route('/<session_id>/<lecture_key>', methods=['DELETE'])
    def delete_lecture(session_id, lecture_key):
        """
        Delete a lecture
        
        Query params:
            lecturerId: Required for verification
        """
        try:

            if not session_id:
                return jsonify({
                    'success': False,
                    'message': 'sessionId is required'
                }), 400
            
            success = lecture_service.delete_lecture(session_id, lecture_key)
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': 'Lecture not found or unauthorized'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Lecture deleted successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Error deleting lecture: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to delete lecture'
            }), 500
    
    @blueprint.route('/<session_id>/<lecture_key>/day/<day_id>', methods=['PUT'])
    def update_lecture_day(session_id, lecture_key, day_id):
        """
        Update a specific lecture day
        
        Request body:
        {
            "topic": "Variables and Data Types",
            "timeline": [{
                "id": "1",
                "startTime": "14:00",
                "endTime": "14:30",
                "description": "Review homework"
            }],
            "notes": "Great class today"
        }
        """
        try:
            data = request.get_json()
            
            lecture = lecture_service.update_lecture_day(session_id, lecture_key, day_id, data)
            
            if not lecture:
                return jsonify({
                    'success': False,
                    'message': 'Lecture or day not found'
                }), 404
            
            return jsonify({
                'success': True,
                'lecture': lecture
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            logger.error(f"Error updating lecture day: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to update lecture day'
            }), 500
    
    # ==================== QUESTION ENDPOINTS ====================
    
    @blueprint.route('/<lecture_key>/questions', methods=['POST'])
    def create_question(lecture_key):
        """
        Create a student question
        
        Request body:
        {
            "studentName": "John Doe",
            "question": "What is recursion?"
        }
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            if 'studentName' not in data or 'question' not in data:
                return jsonify({
                    'success': False,
                    'message': 'studentName and question are required'
                }), 400
            
            question = lecture_service.create_question(
                lecture_key=lecture_key,
                student_name=data['studentName'],
                question_text=data['question']
            )
            
            return jsonify({
                'success': True,
                'question': question
            }), 201
            
        except Exception as e:
            logger.error(f"Error creating question: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to create question'
            }), 500
    
    @blueprint.route('/<session_id>/<lecture_key>/questions', methods=['GET'])
    def get_lecture_questions(session_id, lecture_key):
        """
        Get all questions for a lecture
        """
        try:
            questions = lecture_service.get_questions_by_lecture(session_id, lecture_key)
            
            return jsonify({
                'success': True,
                'questions': questions
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching questions: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to fetch questions'
            }), 500

    @blueprint.route('/<session_id>/<lecture_key>/questions/next', methods=['GET'])
    def get_next_lecture_question(session_id, lecture_key):
        try:
            question = lecture_service.get_next_question_for_lecture(session_id, lecture_key)

            return jsonify({
                'success': True,
                'question': question  # will be null/None if no question available
            }), 200

        except Exception as e:
            logger.error(f"Error fetching next question: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to fetch next question'
            }), 500

    
    @blueprint.route('/lecturer/<session_id>/questions/unanswered/count', methods=['GET'])
    def get_unanswered_count(session_id):
        """
        Get count of unanswered questions for a lecturer
        """
        try:
            count = lecture_service.get_unanswered_questions_count(session_id)
            
            return jsonify({
                'success': True,
                'count': count
            }), 200
            
        except Exception as e:
            logger.error(f"Error counting questions: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to count questions'
            }), 500
    
    @blueprint.route('/questions/<session_id>/<question_id>/answer', methods=['PUT'])
    def mark_question_answered(session_id, question_id):
        """
        Mark a question as answered
        """
        try:
            success = lecture_service.mark_question_answered(session_id, question_id)
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': 'Question not found'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Question marked as answered'
            }), 200
            
        except Exception as e:
            logger.error(f"Error marking question: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to mark question'
            }), 500
    
    return blueprint



