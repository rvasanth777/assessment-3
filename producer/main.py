import json
import random
import time
from kafka import KafkaProducer
from datetime import datetime

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['kafka:9093'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Produce random transaction data
transaction_id_prefix = "txn_"

while True:
    transaction = {
        'transaction_id': f"{transaction_id_prefix}{random.randint(1000, 9999)}",
        'amount': round(random.uniform(10.0, 500.0), 2),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Send message to Kafka topic
    producer.send('transactions_topic', value=transaction)
    print(f"Sent transaction: {transaction['transaction_id']}")
    
    time.sleep(1)  # Produce a new transaction every second

