import json
import psycopg2
from kafka import KafkaConsumer

conn = psycopg2.connect(
    host="postgres",
    database="transactions_db",
    user="user",
    password="password"
)
cur = conn.cursor()

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='kafka:9093',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    cur.execute(
        "INSERT INTO transactions (transaction_id, amount, timestamp) VALUES (%s, %s, %s)",
        (data['transaction_id'], data['amount'], data['timestamp'])
    )
    conn.commit()

