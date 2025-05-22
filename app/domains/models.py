from sqlalchemy import Column, String, Integer
from sqlmodel import SQLModel, Field


class LoanApplication(SQLModel, table=True):
    __tablename__ = "loan_applications"

    applicant_id: str = Field(primary_key=True)
    amount: int
    term_months: int
    status: str

