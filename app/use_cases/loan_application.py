from app.domains.services import LoanApplicationService
from app.domains.schemas import LoanApplicationInput


class LoanApplicationUseCase:
    """
    Use case for processing loan applications.
    """

    def __init__(self, service: LoanApplicationService):
        self.service = service

    async def apply_for_loan(self, application: LoanApplicationInput, db):
        """
        Handles the entire loan application flow
        """

        await self.service.process_loan_application(application, db)
        return {"message": "Loan application received", "applicant_id": application.applicant_id}

    async def get_application_status(self, applicant_id: str, db):
        """
        Fetch loan application status from Redis or PostgreSQL
        :param applicant_id: str
        :param db: Session
        """
        return await self.service.get_application_status(applicant_id, db)


