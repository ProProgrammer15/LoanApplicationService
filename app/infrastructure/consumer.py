import asyncio
from aiokafka import AIOKafkaConsumer
import json
from app.infrastructure.database import get_db
from app.domains.services import LoanApplicationService
from app.domains.models import LoanApplication
from app.infrastructure.cache import cache_status_in_redis
from app.infrastructure.database import store_application_status

loan_application_service = LoanApplicationService()


async def consume_loan_applications():
    """Consume loan applications from Kafka, validate, process, and store results"""
    consumer = AIOKafkaConsumer(
        "loan-applications",
        bootstrap_servers="kafka:9093",
        group_id="loan-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            application_data = msg.value.decode()
            application = json.loads(application_data)

            db = next(get_db())  # Get database session (assuming `get_db` is synchronous)

            loan_application_db = LoanApplication(
                applicant_id=application.get('applicant_id'),
                amount=application.get('amount'),
                term_months=application.get('term_months'),
                status=application.get('status')
            )

            await store_application_status(loan_application_db, db)

            await cache_status_in_redis(application.get('applicant_id'), application.get('status'))

            print(f"Processed loan application for {application['applicant_id']} with status: {application['status']}")
    finally:
        await consumer.stop()

# Run the consume_loan_applications function within an async event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume_loan_applications())
    loop.close()