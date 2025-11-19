from flask import Blueprint, jsonify, request
import logging
from datetime import datetime

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
            # print("===================")
            # print("result = ",result)
            # print("===================")
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
        
    @session_bp.route('/get_session_by_sessionId', methods=['POST'])
    def get_sessions_by_sessionId():
        try:
            payload=request.get_json()
            sessionId=payload.get('sessionId')
            result=sessions_service.get_session_by_sessionId(sessionId)

            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
        except Exception as e:
            logger.error(f"Get session by sessionId error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to retrieve session'
            }), 500
        
    @session_bp.route('/update_session', methods=['POST'])
    def update_session():
        try:
            payload=request.get_json()
            # print("===================")
            # print("payload = ",payload)
            # print("===================")

            sessionId=payload.get('sessionId')
            # print("===================")
            # print("sessionId = ",sessionId)
            # print("===================")
            updateData=payload.get('updateData')
            # print("===================")
            # print("updateData = ",updateData)
            # print("===================")

            result=sessions_service.update_session(sessionId, updateData)

            if result:
                  return jsonify({
                    "success": True,
                    "message": "Session updated successfully"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "message": "Failed to update session"
                }), 400
            
        except Exception as e:
            logger.error(f"Update session error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to update session'
            }), 500
        
    @session_bp.route('/start_session', methods=['POST'])
    def start_session():
        try:
            payload=request.get_json()
            sessionId=payload.get('sessionId')
            result=sessions_service.start_session(sessionId)

            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
        except Exception as e:
            logger.error(f"Start session error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to start session'
            }), 500
        
    @session_bp.route('/end_session', methods=['POST'])
    def end_session():
        try:
            payload=request.get_json()
            sessionId=payload.get('sessionId')
            result=sessions_service.end_session(sessionId)

            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
        except Exception as e:
            logger.error(f"End session error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to end session'
            }), 500
        
    @session_bp.route('/delete_session', methods=['POST'])
    def delete_session():
        try:
            payload=request.get_json()
            sessionId=payload.get('sessionId')
            result=sessions_service.delete_session(sessionId)

            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
            
        except Exception as e:
            logger.error(f"Delete session error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to delete session'
            }), 500
        
    @session_bp.route('/send_query', methods=['POST'])
    def send_query():
        try:
            payload = request.get_json()
            sessionId = payload.get('sessionId')
            query = payload.get('query')
            print("===================")
            print("sessionId = ",sessionId)
            print("query = ",query)
            print("===================")

            session=sessions_service.get_session_by_sessionId(sessionId)['session']
            print("===================")
            print(session)
            # if session['is']
            print("===================")
            print(session['allow_queries'], type(session['allow_queries']))
            print("===================")
            if session['allow_queries'] is False :
                return jsonify({
                    'success': False,
                    'message': 'Queries are not allowed for this session'
                }), 403
            
            print("===================")
            print("Session allows queries")

            if session['session_is_active'] is False:
                return jsonify({
                    'success': False,
                    'message': 'Cannot send query to an inactive session'
                }), 403
            print("===================")
            print("Session is active")

            
            
            # if queries are allowed
            # add a new array element to the queries array in the session document
            session_query={
                "query": query,
                "query_read": False,
                "timestamp": str(datetime.utcnow())
            }


            session['queries']=session.get('queries', [])
            session['queries'].append(session_query)
            session['new_query']=True

            print("===================")
            print("Updated session:", session)
            result = sessions_service.update_session(sessionId, session)

            if result:
                  return jsonify({
                    "success": True,
                    "message": "Session updated successfully"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "message": "Failed to update session"
                }), 400
        except Exception as e:
            logger.error(f"Send query error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to send query'
            }), 500
        
    @session_bp.route('/get_unread_queries', methods=['POST'])
    def get_unread_queries():
        try:
            payload = request.get_json()
            sessionId = payload.get('sessionId')

            session=sessions_service.get_session_by_sessionId(sessionId)['session']
            if not session:
                return jsonify({
                    'success': False,
                    'message': 'Session not found'
                }), 404

            session.pop('_id', None)
            unread_queries = [q for q in session.get('queries', []) if not q.get('query_read', True)]

            # also mark unread queries as read
            for query in session.get('queries', []):
                if not query.get('query_read', True):
                    query['query_read'] = True
            
            session['new_query'] = False
            result =sessions_service.update_session(sessionId, session)
            # print("===================")
            # print("Updated session after marking queries as read:", session)
            # print("===================")
            print(unread_queries)

            return jsonify({
                'success': True,
                'unread_queries': unread_queries
            }), 200

        except Exception as e:
            logger.error(f"Get unread queries error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to get unread queries'
            }), 500

    return session_bp