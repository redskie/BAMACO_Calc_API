"""
Additional edge case tests for the mai-tools API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_rating_edge_cases():
    print("\n=== Testing rating edge cases ===")
    test_cases = [
        {"level": 15.0, "achievement": 101.0, "desc": "Max level, over 100.5%"},
        {"level": 1.0, "achievement": 50.0, "desc": "Min level, C rank"},
        {"level": 13.7, "achievement": 100.5, "desc": "SSS+ boundary"},
        {"level": 0.0, "achievement": 100.0, "desc": "Zero level"},
        {"level": -13.7, "achievement": 100.0, "desc": "Negative level (utage)"},
    ]

    for case in test_cases:
        try:
            payload = {"level": case["level"], "achievement": case["achievement"]}
            r = requests.post(f"{BASE_URL}/rating", json=payload, timeout=5)
            result = r.json()
            print(f"✓ {case['desc']}: rating={result['rating']:.2f}, rank={result['rank_title']}")
        except Exception as e:
            print(f"✗ {case['desc']}: {e}")

def test_rating_range_all_ranks():
    print("\n=== Testing rating-range for all ranks ===")
    ranks = ["SSS+", "SSS", "SS+", "SS", "S+", "S", "AAA", "AA", "A", "BBB", "BB", "B", "C", "D"]

    for rank in ranks:
        try:
            payload = {"level": 13.0, "rank_title": rank}
            r = requests.post(f"{BASE_URL}/rating-range", json=payload, timeout=2)
            if r.status_code == 200:
                result = r.json()
                print(f"✓ {rank:4s}: [{result['min_rating']}, {result['max_rating']}]")
            else:
                print(f"✗ {rank:4s}: HTTP {r.status_code}")
        except requests.exceptions.Timeout:
            print(f"✗ {rank:4s}: Timeout (skipping)")
            break
        except Exception as e:
            print(f"✗ {rank:4s}: {e}")

def test_recommended_levels_various_ratings():
    print("\n=== Testing recommended-levels with various target ratings ===")
    test_ratings = [10, 50, 100, 200, 300]

    for rating in test_ratings:
        try:
            payload = {"rating": rating}
            r = requests.post(f"{BASE_URL}/recommended-levels", json=payload, timeout=5)
            result = r.json()
            total_suggestions = sum(len(levels) for levels in result.values())
            print(f"✓ Rating {rating}: {len(result)} rank groups, {total_suggestions} total suggestions")
        except Exception as e:
            print(f"✗ Rating {rating}: {e}")

def test_invalid_inputs():
    print("\n=== Testing invalid inputs ===")

    # Invalid rank title
    try:
        payload = {"level": 13.0, "rank_title": "INVALID"}
        r = requests.post(f"{BASE_URL}/rating-range", json=payload, timeout=5)
        if r.status_code == 404:
            print("✓ Invalid rank title properly rejected (404)")
        else:
            print(f"✗ Invalid rank title: Expected 404, got {r.status_code}")
    except Exception as e:
        print(f"✗ Invalid rank title: {e}")

    # Missing required fields
    try:
        r = requests.post(f"{BASE_URL}/rating", json={}, timeout=5)
        if r.status_code == 422:
            print("✓ Missing fields properly rejected (422)")
        else:
            print(f"✗ Missing fields: Expected 422, got {r.status_code}")
    except Exception as e:
        print(f"✗ Missing fields: {e}")

if __name__ == "__main__":
    print("Running edge case tests...")
    test_rating_edge_cases()
    test_rating_range_all_ranks()
    test_recommended_levels_various_ratings()
    test_invalid_inputs()
    print("\n" + "="*50)
    print("Edge case testing complete!")
