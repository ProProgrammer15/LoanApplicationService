import pytest
from main import app
from fastapi.testclient import TestClient
from app.infrastructure.database import SessionLocal
import os
from unittest.mock import patch
from app.domains.models import LoanApplication

os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL")

@pytest.fixture
def client():
    client = TestClient(app)
    yield client

@pytest.fixture
def db():
    # Create a new database session
    db_session = SessionLocal()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function", autouse=True)
def reset_database(db):
    """Ensure database is cleaned up after each test"""
    # Reset or roll back changes made during the test
    db.query(LoanApplication).delete()
    db.commit()


@pytest.fixture
def mock_kafka_producer():
    """Fixture to mock Kafka producer"""
    with patch('aiokafka.AIOKafkaProducer.send_and_wait') as mock_send_and_wait:
        yield mock_send_and_wait