from app.domains.schemas import LoanApplicationInput
from app.infrastructure.database import check_applicant_exists
from app.infrastructure.cache import redis_client
from app.infrastructure.database import get_application_status
from sqlalchemy.orm import Session
from app.infrastructure.producer import produce_loan_application


class LoanApplicationService:

    async def approve_application(self, application: LoanApplicationInput, db) -> str:
        """
        Validates loan application and determines status
        :param application: LoanApplicationInput
        :return: "approved" or "rejected"
        """
        if await check_applicant_exists(application.applicant_id, db):
            raise ValueError("Applicant already exists")

        return "approved" if application.amount < 5000 else "rejected"

    async def process_loan_application(self, application: LoanApplicationInput, db):
        """Processes the loan application: validate, store, and cache results."""
        status = await self.approve_application(application, db)

        application = {**application.dict(), 'status': status}

        try:
            await produce_loan_application(application)
        except Exception as e:
            return f"Failed to produce loan application: {e}"

        return application

    async def get_application_status(self, applicant_id: str, db: Session):
        """
        Fetch loan application status from Redis or PostgreSQL
        :param applicant_id: str
        :param db: Session
        """

        status = await redis_client.get(applicant_id)
        if status:
            return status.decode()

        status = await get_application_status(applicant_id, db)
        if not status:
            return None
        return status
