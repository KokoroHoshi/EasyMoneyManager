import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

cred = credentials.Certificate('./firebaseServiceAccountKey.json')
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
    record_data = {
        'name': record['name'],
        'amount': record['amount'],
        'tags': ','.join(record['tags']),
        'type': record['type'],
        'date': record['date']
    }
    db.collection('users').document(user_id).collection('records').document(record_id).set(record_data)

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
