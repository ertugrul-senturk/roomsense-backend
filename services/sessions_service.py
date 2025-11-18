import uuid
import logging
from models.sessions import SessionModel
from models.user import User

logger = logging.getLogger(__name__)

class SessionsService:
    def __init__(self, db):
        self.db = db

    def create_session(self, payload):
        """Create a new session"""
        # print("======= RAW PAYLOAD RECEIVED =======")
        # print(payload)
        # print("====================================")
        """
        Expected payload structure:
        {
            "name": "Morning Standup",
            "uniqueNumber": "4950970986",
            "session_expected_start_time": "2025-01-16T10:00:00Z",
            "session_expected_end_time": "2025-01-16T11:00:00Z",

            "session_actual_start_time": null,
            "session_actual_end_time": null,

            "notes_available": false,
            "session_notes": "",

            "allow_queries": true,

            "agenda_available": true,
            "agenda": "Daily tasks"
        }
        """

        # Ensure payload is dict
        if payload is None:
            return {"success": False, "message": "No JSON body received"}

        uniqueNumber = payload.get("uniqueNumber")
        # print("------------------------------")
        # print(uniqueNumber, type(uniqueNumber))
        # print("------------------------------")
        
        if not uniqueNumber or str(uniqueNumber).strip() == "":
            return {"success": False, "message": "userUniqueId is required"}
        
        user= User.find_by_unique_number(self.db, uniqueNumber)
        if not user:
            return {"success": False, "message": "User not found"}
        
        session_id=payload.get("sessionId") or str(uuid.uuid4())

        if SessionModel.findSessionBySessionId(self.db, session_id):
            return {"success": False, "message": "Session ID already exists"}
        
        payload["sessionId"] = session_id

        try:
            saved_session = SessionModel.createSession(self.db, payload)
            """
            Saved session structure:
            {
                "success": True, 
                "message": "Session created successfully", 
                "session": 
                    {
                    "name": "Morning Standup", 
                    "uniqueNumber": "4950970986", 
                    "session_expected_start_time": "2025-01-16T10:00:00Z", 
                    "session_expected_end_time": "2025-01-16T11:00:00Z", 
                    "session_actual_start_time": null, 
                    "session_actual_end_time": null, 
                    "notes_available": false, 
                    "session_notes": "", 
                    "allow_queries": true, 
                    "agenda_available": true, 
                    "agenda": "Daily tasks", 
                    "sessionId": "ebe10ea8-13d0-4923-b492-85903c6f7d1b", 
                    "createdAt": {"$date": "2025-11-18T22:34:34.183Z"}, 
                    "updatedAt": {"$date": "2025-11-18T22:34:34.183Z"}, 
                    "_id": {
                        "$oid": "691cf47a91eea13c1a3f5941"
                    }
                }
            }            
            """


            return {
                "success": True,
                "message": "Session created successfully",
                "session": saved_session
            }
        
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            return {
                "success": False,
                "message": "Failed to create session"
            }
    
    def get_all_session_by_user_id(self, uniqueNumber):
        """Retrieve sessions by user unique ID"""
        try:
            sessions = SessionModel.findSessionsByUserUniqueId(self.db, uniqueNumber)
            # print("===================")
            # print("sessions = ", sessions)
            # print("===================")
            return {
                "success": True,
                "sessions": sessions
            }
        except Exception as e:
            logger.error(f"Error retrieving sessions: {str(e)}")
            return {
                "success": False,
                "message": "Failed to retrieve sessions"
            }
    
    def update_session(self, sessionId, updateData):
        """Update an existing session"""
        try:
            result = SessionModel.updateSession(self.db, sessionId, updateData)
            if result.modified_count == 1:
                return {
                    "success": True,
                    "message": "Session updated successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "No changes made to the session"
                }
        except Exception as e:
            logger.error(f"Error updating session: {str(e)}")
            return {
                "success": False,
                "message": "Failed to update session"
            }