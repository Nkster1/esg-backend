import requests

if __name__ == '__main__':
    payload = {
        "legal_name": "Shell LLC",
        "ownership": "Stock Company",
        "legal_form": "LLC",
        "location": "USA",
        "sector": "",
        "activities": "we refine oil to gasoline\n",
        "products": "Oil Refinement",
        "markets": "we operate globally",
        "supply_chain": "we do everything ourselves",
        "num_employees": "10000"
    }
    r = requests.post('http://127.0.0.1:8000/langchain/esg_report', json=payload)
    print(r)
