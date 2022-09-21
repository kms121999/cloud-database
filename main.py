import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

SERVICE_ACCOUNT_CRED_FILE = "./service_account.json"

creds = credentials.Certificate(SERVICE_ACCOUNT_CRED_FILE)

app = firebase_admin.initialize_app(creds)

db = firestore.client()

