from fastapi import FastAPI
from kafka import KafkaProducer
import json
from datetime import datetime

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='kafka:9093',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.post("/send/")
def send_transaction():
    message = {
        "transaction_id": "abc123",
        "amount": 560.75,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    producer.send("transactions", message)
    return {"status": "Message sent", "data": message}

