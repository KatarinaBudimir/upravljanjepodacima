
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'objava_topic',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

objava_count = 0

for message in consumer:
    objava_data = message.value
    if objava_data['action'] == 'create':
        objava_count += 1
        print(f"Nove objave: {objava_count}")

