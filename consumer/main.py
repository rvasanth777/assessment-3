from kafka import KafkaConsumer
import json
import psycopg2
from prometheus_client import start_http_server, Counter

# Start Prometheus metrics server (on port 8001)
start_http_server(8001)

# Define Prometheus Counter
messages_consumed = Counter('messages_consumed_total', 'Total number of messages consumed')

# Set up Kafka Consumer
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='consumer-group-1'
)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='transactions_db',
    user='vasanth',
    password='yourpassword',  # Update with your actual password
    host='postgres',
    port='5432'
)
cursor = conn.cursor()

print("Consumer started and listening for messages...")

# Consume messages and insert into DB
for msg in consumer:
    data = msg.value
    print(f"Consumed message: {data}")

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

    # Increment Prometheus counter
    messages_consumed.inc()

