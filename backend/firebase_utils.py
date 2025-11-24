import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# -----------------------------
# 初始化 Firebase
# -----------------------------
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

# -----------------------------
# CRUD 函式
# -----------------------------
def add_record(user_id, record):
    """
    新增記錄，前端傳入完整 ISO 字串
    """
    record_data = {
        'name': record['name'],
        'amount': record['amount'],
        'tags': ','.join(record['tags']),
        'type': record['type'],
        'date': record['date']  # 前端已是 ISO UTC
    }
    db.collection('users').document(user_id).collection('records').add(record_data)


def get_record(user_id, record_id):
    record_ref = db.collection('users').document(user_id).collection('records').document(record_id)
    record = record_ref.get()
    if record.exists:
        data = record.to_dict()
        data['record_id'] = record.id
        return data
    return None


def update_record(user_id, record_id, record):
    """
    更新記錄，直接覆蓋前端傳來的 ISO 字串
    """
    record_ref = db.collection('users').document(user_id).collection('records').document(record_id)
    record_data = {
        'name': record['name'],
        'amount': record['amount'],
        'tags': ','.join(record['tags']),
        'type': record['type'],
        'date': record['date']
    }
    record_ref.set(record_data)


def delete_record(user_id, record_id):
    record_ref = db.collection('users').document(user_id).collection('records').document(record_id)
    record_ref.delete()


def get_records_by_date(user_id, date):
    """
    根據 YYYY-MM-DD 抓當天所有紀錄
    """
    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)

    start_iso = start_date.isoformat()  # 00:00:00
    end_iso = end_date.isoformat()      # 隔天 00:00:00

    records_ref = db.collection('users').document(user_id).collection('records')
    query = records_ref.where('date', '>=', start_iso).where('date', '<', end_iso)
    results = query.stream()

    records = []
    for record in results:
        data = record.to_dict()
        data['record_id'] = record.id
        records.append(data)

    return records


def get_records_by_utc_range(user_id, start_dt, end_dt):
    """
    根據 UTC datetime 範圍抓紀錄
    start_dt / end_dt 必須是 datetime 物件
    """
    records_ref = db.collection('users').document(user_id).collection('records') \
        .where('date', '>=', start_dt.isoformat()) \
        .where('date', '<=', end_dt.isoformat())
    records = []
    for doc in records_ref.stream():
        data = doc.to_dict()
        data['record_id'] = doc.id
        records.append(data)
    return records
