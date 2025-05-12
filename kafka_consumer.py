from kafka import KafkaConsumer
import json
import psycopg2
from prometheus_client import start_http_server, Counter

# Start Prometheus HTTP metrics server on port 8001
start_http_server(8001)

# Define a Prometheus counter metric
messages_consumed = Counter('messages_consumed_total', 'Total messages consumed')

# Kafka consumer setup
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='my-consumer-group'
)

# PostgreSQL connection
conn = psycopg2.connect(
    dbname='transactions_db',
    user='vasanth',
    password='devops123',
    host='postgres',
    port='5432'
)
cursor = conn.cursor()

print("Consumer started. Waiting for messages...")

for msg in consumer:
    data = msg.value
    print(f"Received: {data}")

    # Insert into DB
    cursor.execute(
        "INSERT INTO transactions (transaction_id, description, amount, status, created_at) VALUES (%s, %s, %s, %s, %s)",
        (
            data.get('transaction_id'),
            data.get('description', ''),
            data.get('amount'),
            data.get('status', 'success'),
            data.get('timestamp')
        )
    )
    conn.commit()

    # 📈 Increment Prometheus metric here
    messages_consumed.inc()

