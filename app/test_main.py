from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code==200
    assert response.json()=={"docs_entry_point":"/docs"}

def test_duplicated_beneficiary():
    response = client.get("/duplicated/beneficiary")
    assert response.status_code==200
    assert response.json()[0]["properties"]["case_type"]=="beneficiaire"