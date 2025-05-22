from pydantic import BaseModel, validator


class LoanApplicationInput(BaseModel):
    applicant_id: str
    amount: float
    term_months: int

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

    @validator('term_months')
    def validate_term_months(cls, v):
        if not (1 <= v <= 60):
            raise ValueError('Term months must be between 1 and 60')
        return v





