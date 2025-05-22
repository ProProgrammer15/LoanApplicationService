from fastapi import APIRouter, HTTPException, Depends
from app.use_cases.loan_application import LoanApplicationUseCase
from app.domains.services import LoanApplicationService
from app.domains.schemas import LoanApplicationInput
from app.infrastructure.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

loan_application_service = LoanApplicationService()
loan_application_use_case = LoanApplicationUseCase(loan_application_service)


@router.post("/application")
async def apply_for_loan(application: LoanApplicationInput, db: Session = Depends(get_db)):
    try:
        response = await loan_application_use_case.apply_for_loan(application, db)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/application/{applicant_id}")
async def get_application_status(applicant_id: str, db: Session = Depends(get_db)):
    """
    Get the status of a loan application.
    :param applicant_id: The ID of the applicant.
    :param db: The database session.
    :return: The loan application status.
    """
    status = await loan_application_use_case.get_application_status(applicant_id, db)
    if not status:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"status": status}
