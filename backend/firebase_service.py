import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Firebase 초기화 (한 번만)
if not firebase_admin._apps:
    cred = credentials.Certificate("backend/firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def save_session(session_data: dict):
    db.collection("sessions").add(session_data)