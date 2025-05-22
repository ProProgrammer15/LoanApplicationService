from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.domains.models import LoanApplication  # SQLAlchemy model
from sqlmodel import SQLModel
import os
from sqlalchemy.orm import Session

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create the database tables if they don't exist."""
    SQLModel.metadata.create_all(bind=engine)


def get_db():
    """Get a new database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def store_application_status(application: LoanApplication, db: Session):
    """
    Store the loan application status in PostgreSQL.
    """
    db.add(application)
    db.commit()


async def get_application_status(applicant_id: str, db: Session):
    """Query the database to get the loan application status."""
    loan_application = db.query(LoanApplication).filter(LoanApplication.applicant_id == applicant_id).first()

    if loan_application:
        return loan_application.status
    return None


async def check_applicant_exists(applicant_id: str, db:Session) -> bool:
    """
    Check if the applicant exists in the database.
    :param applicant_id:
    :param db:
    :return:
    """
    return db.query(LoanApplication).filter(LoanApplication.applicant_id == applicant_id).first() is not None

