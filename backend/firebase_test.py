import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("backend/firebase_key.json")

firebase_admin.initialize_app(cred)

db = firestore.client()

session_data = {
    "uid": "test_user",
    "posture_score": 87,
    "warning_count": 2,
    "created_at": "2026-05-28"
}

db.collection("sessions").add(session_data)

print("Session Data Saved!")