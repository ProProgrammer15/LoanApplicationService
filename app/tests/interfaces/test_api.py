

def test_apply_for_loan(client, db, mock_kafka_producer):
    """Test loan application with valid and invalid data"""

    data = {
        "applicant_id": "123",
        "amount": 4000,
        "term_months": 12
    }
    response = client.post("/application", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Loan application received", "applicant_id": "123"}

    mock_kafka_producer.assert_called_once()


def test_loan_validations(client, db, mock_kafka_producer):
    invalid_data = {
        "applicant_id": "124",
        "amount": -100,
        "term_months": 12
    }
    response = client.post("/application", json=invalid_data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Value error, Amount must be greater than 0"

    invalid_term_data = {
        "applicant_id": "125",
        "amount": 6000,
        "term_months": 70
    }
    response = client.post("/application", json=invalid_term_data)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Value error, Term months must be between 1 and 60"
