from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='172.31.40.57:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

message = {
    "transaction_id": 1,
    "user_id": 101,
    "amount": 999.99,
    "timestamp": "datetime.utcnow().isoformat() + "Z""
}

producer.send('transactions', message)
producer.flush()

print("Message sent to Kafka topic 'transactions'")

