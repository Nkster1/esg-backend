from fastapi.testclient import TestClient
from main import app  # or wherever your FastAPI app is defined

client = TestClient(app)


def test_esg_report_caching():
    # Create a mock company
    company = {
        "legal_name": "OpenAI Ltd.",
        "ownership": "Private",
        "legal_form": "Limited Company",
        "location": "San Francisco, CA, USA",
        "sector": "Artificial Intelligence",
        "num_employees": "500",
        "activities": "Research and Development in AI",
        "products": "GPT models, Codex",
        "markets": "Global",
        "supply_chain": "Cloud providers, Hardware providers"
    }
    # Make a request to the test client and store the response
    response = client.post("/langchain/esg_report", json=company)

    # Assert the status code is 200 (indicating success)
    assert response.status_code == 200
    res = response.json()

    response = client.post("/langchain/esg_report", json=company)
    assert response.json() == res

