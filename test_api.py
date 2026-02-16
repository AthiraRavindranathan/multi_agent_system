"""
Test script for Multi-Agent Support System API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_agents():
    """Test agents list endpoint"""
    print("\n=== Testing Agents Endpoint ===")
    response = requests.get(f"{BASE_URL}/agents")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_support_faq():
    """Test FAQ query"""
    print("\n=== Testing FAQ Query ===")
    payload = {
        "question": "How do I reset my password?",
        "customer_id": "test123",
        "priority": "normal"
    }
    response = requests.post(f"{BASE_URL}/support", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_support_technical():
    """Test technical query"""
    print("\n=== Testing Technical Query ===")
    payload = {
        "question": "My application keeps crashing with an error",
        "customer_id": "test456",
        "priority": "high"
    }
    response = requests.post(f"{BASE_URL}/support", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_support_billing():
    """Test billing query"""
    print("\n=== Testing Billing Query ===")
    payload = {
        "question": "I need a refund for my last payment",
        "customer_id": "test789",
        "priority": "normal"
    }
    response = requests.post(f"{BASE_URL}/support", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Agent Support System - API Tests")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Agents List", test_agents),
        ("FAQ Query", test_support_faq),
        ("Technical Query", test_support_technical),
        ("Billing Query", test_support_billing)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\nError in {name}: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
