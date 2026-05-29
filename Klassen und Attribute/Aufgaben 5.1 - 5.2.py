import time
from datetime import datetime
import psutil
from pymongo import MongoClient

class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        self.cpu = cpu if cpu is not None else psutil.cpu_percent(interval=1)
        self.ram_total = ram_total if ram_total is not None else psutil.virtual_memory().total
        self.ram_used = ram_used if ram_used is not None else psutil.virtual_memory().used
        self.timestamp = timestamp if timestamp is not None else datetime.now()

col = MongoClient("mongodb://localhost:27017/")["restaurants"]["power_stats"]

while True:
    p = Power()
    # Entfernt die interne MongoDB-ID aus dem Dictionary für die Konsolen-Ausgabe
    data = p.__dict__.copy()
    col.insert_one(p.__dict__)
    print(f"Gespeichert: CPU: {data['cpu']}% | RAM total: {data['ram_total']} | RAM verwendet: {data['ram_used']} | Zeit: {data['timestamp']}")