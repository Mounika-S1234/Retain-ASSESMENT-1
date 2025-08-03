from threading import Lock
from datetime import datetime

url_store = {}
store_lock = Lock()

def store_url(short_code, long_url):
    with store_lock:
        url_store[short_code] = {
            "url": long_url,
            "created_at": datetime.now(),
            "clicks": 0
        }

def get_url_data(short_code):
    with store_lock:
        return url_store.get(short_code)

def increment_clicks(short_code):
    with store_lock:
        if short_code in url_store:
            url_store[short_code]["clicks"] += 1
