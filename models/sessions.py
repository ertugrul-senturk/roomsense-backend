from datetime import datetime
from bson.objectid import ObjectId

class SessionModel:

    @staticmethod
    def createSession(db, sessionData):
        sessionData["createdAt"] = datetime.utcnow()
        sessionData["updatedAt"] = datetime.utcnow()

        result = db.sessions.insert_one(sessionData)
        return {**sessionData, "_id": result.inserted_id}
    
    @staticmethod
    def findSessionByObjectId(db, sessionId):
        session = db.sessions.find_one({"_id": ObjectId(sessionId)})
        return session
    
    def findSessionsByUserUniqueId(db, userUniqueId):
        sessions = list(db.sessions.find({"uniqueNumber": userUniqueId}))
        # print("===================")
        # print("all sessions",sessions)
        # print("===================")
        return sessions
    
    def findSessionBySessionId(db, sessionId):
        session = db.sessions.find_one({"sessionId": sessionId})
        return session
    
    @staticmethod
    def updateSession(db, sessionId, updateData):
        updateData["updatedAt"] = datetime.utcnow()
        updateData.pop('_id', None)  # Prevent updating the _id field if present
        result = db.sessions.update_one(
            {"sessionId": sessionId},
            {"$set": updateData}
        )
        return result
    
    @staticmethod
    def deleteSession(db, sessionId):
        result = db.sessions.delete_one({"sessionId": sessionId})
        return result