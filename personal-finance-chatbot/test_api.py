import requests
import json

API_URL = "http://127.0.0.1:8000"

def test_nlu_endpoint():
    """Test the NLU endpoint"""
    print("Testing NLU endpoint...")
    payload = {"text": "I need help with my budget planning"}
    try:
        response = requests.post(f"{API_URL}/nlu", json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.ok:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing NLU endpoint: {e}")

def test_generate_endpoint():
    """Test the generate endpoint"""
    print("\nTesting Generate endpoint...")
    payload = {"question": "How can I save money as a student?", "persona": "student"}
    try:
        response = requests.post(f"{API_URL}/generate", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.ok:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing Generate endpoint: {e}")

def test_budget_endpoint():
    """Test the budget summary endpoint"""
    print("\nTesting Budget Summary endpoint...")
    payload = {
        "income": 3000.0,
        "expenses": {"Rent": 1000, "Food": 300, "Transportation": 200},
        "savings_goal": 500.0,
        "persona": "student"
    }
    try:
        response = requests.post(f"{API_URL}/budget-summary", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.ok:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing Budget Summary endpoint: {e}")

def test_spending_endpoint():
    """Test the spending insights endpoint"""
    print("\nTesting Spending Insights endpoint...")
    payload = {
        "income": 3000.0,
        "expenses": {"Rent": 1000, "Food": 300, "Transportation": 200},
        "goals": [{"name": "Emergency Fund", "amount": "1000", "deadline": "6 months"}],
        "persona": "student"
    }
    try:
        response = requests.post(f"{API_URL}/spending-insights", json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.ok:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing Spending Insights endpoint: {e}")

if __name__ == "__main__":
    print("Testing Personal Finance Chatbot API endpoints...")
    test_nlu_endpoint()
    test_generate_endpoint()
    test_budget_endpoint()
    test_spending_endpoint()
