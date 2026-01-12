"""
Test script for the mai-tools API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("\n=== Testing /health ===")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_ranks():
    print("\n=== Testing /ranks ===")
    try:
        r = requests.get(f"{BASE_URL}/ranks", timeout=5)
        print(f"Status: {r.status_code}")
        data = r.json()
        print(f"Number of ranks: {len(data)}")
        print(f"First rank: {data[0]}")
        print(f"Last rank: {data[-1]}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_rating():
    print("\n=== Testing /rating ===")
    try:
        payload = {"level": 13.7, "achievement": 100.3}
        r = requests.post(f"{BASE_URL}/rating", json=payload, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Request: {payload}")
        print(f"Response: {r.json()}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_rating_range():
    print("\n=== Testing /rating-range ===")
    try:
        payload = {"level": 13.7, "rank_title": "SSS"}
        r = requests.post(f"{BASE_URL}/rating-range", json=payload, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Request: {payload}")
        print(f"Response: {r.json()}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_recommended_levels():
    print("\n=== Testing /recommended-levels ===")
    try:
        payload = {"rating": 100}
        r = requests.post(f"{BASE_URL}/recommended-levels", json=payload, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Request: {payload}")
        data = r.json()
        print(f"Ranks returned: {list(data.keys())}")
        if "SSS+" in data:
            print(f"SSS+ levels (first 3): {data['SSS+'][:3]}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Starting API tests...")
    results = {
        "health": test_health(),
        "ranks": test_ranks(),
        "rating": test_rating(),
        "rating_range": test_rating_range(),
        "recommended_levels": test_recommended_levels(),
    }

    print("\n" + "="*50)
    print("TEST RESULTS:")
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name}: {status}")

    all_passed = all(results.values())
    print("="*50)
    print(f"\nOverall: {'All tests passed!' if all_passed else 'Some tests failed.'}")
