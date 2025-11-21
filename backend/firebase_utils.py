import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

load_dotenv()

cred_path = os.getenv('FIREBASE_CRED_PATH')
if cred_path and os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
else:
    firebase_json = os.getenv("FIREBASE_CREDENTIALS")

    if not firebase_json:
        raise ValueError(
            "找不到 Firebase 憑證：\n"
            "- 請確定 FIREBASE_CRED_PATH 指向檔案\n"
            "- 或設定環境變數 FIREBASE_CREDENTIALS"
        )

    cred_info = json.loads(firebase_json)
    cred = credentials.Certificate(cred_info)

firebase_admin.initialize_app(cred)

db = firestore.client()

def add_record(user_id, record):
    parsed_date = datetime.fromisoformat(record['date'].replace('Z', '+00:00')).isoformat()

    record_data = {
        'name': record['name'],
        'amount': record['amount'],
        'tags': ','.join(record['tags']),
        'type': record['type'],
        'date': parsed_date
    }

    db.collection('users').document(user_id).collection('records').add(record_data)

def get_record(user_id, record_id):
    record_ref = db.collection('users').document(user_id).collection('records').document(record_id)
    record = record_ref.get()
    if record.exists:
        return record.to_dict()
    else:
        return None

def update_record(user_id, record_id, record):
    # Fetch existing record to compare dates
    existing_record_ref = db.collection('users').document(user_id).collection('records').document(record_id)
    existing_record = existing_record_ref.get()
    
    if existing_record.exists:
        existing_date = existing_record.to_dict().get('date')
        if existing_date:
            # Parse both dates to compare up to minute precision
            existing_date_parsed = datetime.fromisoformat(existing_date.replace('Z', '+00:00')).isoformat(timespec='minutes')
            new_date_parsed = datetime.fromisoformat(record['date'].replace('Z', '+00:00')).isoformat(timespec='minutes')
            
            # If dates are the same up to minutes, keep existing full precision date
            if existing_date_parsed == new_date_parsed:
                record['date'] = existing_date
            else:
                # Otherwise, ensure new date has full precision
                record['date'] = datetime.fromisoformat(record['date'].replace('Z', '+00:00')).isoformat()
    
    record_data = {
        'name': record['name'],
        'amount': record['amount'],
        'tags': ','.join(record['tags']),
        'type': record['type'],
        'date': record['date']
    }

    existing_record_ref.set(record_data)

def delete_record(user_id, record_id):
    record_ref = db.collection('users').document(user_id).collection('records').document(record_id)
    record_ref.delete()

def get_records_by_date(user_id, date):
    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)
    
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()
    
    records_ref = db.collection('users').document(user_id).collection('records')
    
    query = records_ref.where('date', '>=', start_date_str).where('date', '<', end_date_str)
    results = query.stream()

    records = []
    for record in results:
        record_data = record.to_dict()
        record_data['record_id'] = record.id
        records.append(record_data)
    
    return records
