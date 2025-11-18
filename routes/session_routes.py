from flask import Blueprint, jsonify, request
import logging

logger=logging.getLogger(__name__)

session_bp=Blueprint('session', __name__, url_prefix='/session')

def init_session_routes(sessions_service):

    @session_bp.route('/create_session', methods=['POST'])
    def create_session():
        try:
            payload=request.get_json()
            result=sessions_service.create_session(payload)

            if result['success']:
                return jsonify(result), 201
            else:
                return jsonify(result), 400
            
        except Exception as e:
            logger.error(f"Create session error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to create session'
            }), 500
        
    @session_bp.route('/get_all_sessions_by_uniqueNumber', methods=['POST'])
    def get_all_sessions():
        try:
            payload=request.get_json()
            uniqueNumber=payload.get('uniqueNumber')
            # uniqueNumber=request.args.get('uniqueNumber')
            # print("===================")
            # print(uniqueNumber)
            # print("===================")
            result=sessions_service.get_all_session_by_user_id(uniqueNumber)
            print("===================")
            print("result = ",result)
            print("===================")
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
            
        except Exception as e:
            logger.error(f"Get all sessions error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to retrieve sessions'
            }), 500
        
    @session_bp.route('/update_session', methods=['POST'])
    def update_session():
        try:
            payload=request.get_json()
            print("===================")
            print("payload = ",payload)
            print("===================")

            sessionId=payload.get('sessionId')
            print("===================")
            print("sessionId = ",sessionId)
            print("===================")
            updateData=payload.get('updateData')
            print("===================")
            print("updateData = ",updateData)
            print("===================")

            result=sessions_service.update_session(sessionId, updateData)

            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
        except Exception as e:
            logger.error(f"Update session error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to update session'
            }), 500
  
        
    return session_bp