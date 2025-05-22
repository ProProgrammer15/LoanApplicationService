from aiokafka import AIOKafkaProducer
import json
import os

KAFKA_URL = os.getenv("KAFKA_URL")

async def produce_loan_application(application: dict):
    """Publish loan application to Kafka"""

    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_URL)
    await producer.start()
    try:
        message = json.dumps(application)
        await producer.send_and_wait("loan-applications", value=message.encode())
    except Exception as e:
        print(e)


