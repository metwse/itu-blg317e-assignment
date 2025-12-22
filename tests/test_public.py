"""Simple tests for public API endpoints (no auth required)."""

import requests

BASE_URL = "http://127.0.0.1:6767/api/public"


def test_list_economies():
    """Test GET /economies - should return list of countries."""
    r = requests.get(f"{BASE_URL}/economies")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    print(f"✓ Economies: {len(data)} items")


def test_list_regions():
    """Test GET /regions - should return list of regions."""
    r = requests.get(f"{BASE_URL}/regions")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    print(f"✓ Regions: {len(data)} items")


def test_list_income_levels():
    """Test GET /income-levels - should return income level categories."""
    r = requests.get(f"{BASE_URL}/income-levels")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    print(f"✓ Income levels: {len(data)} items")


def test_list_providers():
    """Test GET /providers - should return data providers."""
    r = requests.get(f"{BASE_URL}/providers")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    print(f"✓ Providers: {len(data)} items")


def test_list_indicators():
    """Test GET /indicators - should return indicator data."""
    r = requests.get(f"{BASE_URL}/indicators", params={"limit": 10})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    print(f"✓ Indicators: {len(data)} items (limited to 10)")


def test_list_indicators_with_filter():
    """Test GET /indicators with filters."""
    r = requests.get(f"{BASE_URL}/indicators", params={
        "economy_code": "USA",
        "year_start": 2000,
        "year_end": 2020,
        "limit": 5
    })
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Filtered indicators (USA 2000-2020): {len(data)} items")


def test_economic_indicators():
    """Test GET /indicators/economic."""
    r = requests.get(f"{BASE_URL}/indicators/economic", params={"limit": 5})
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Economic indicators: {len(data)} items")


def test_health_indicators():
    """Test GET /indicators/health."""
    r = requests.get(f"{BASE_URL}/indicators/health", params={"limit": 5})
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Health indicators: {len(data)} items")


def test_environment_indicators():
    """Test GET /indicators/environment."""
    r = requests.get(f"{BASE_URL}/indicators/environment", params={"limit": 5})
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Environment indicators: {len(data)} items")


def test_stats():
    """Test GET /stats - should return database statistics."""
    r = requests.get(f"{BASE_URL}/stats")
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Stats: {data}")


if __name__ == "__main__":
    print("=== Testing Public API ===\n")
    test_list_economies()
    test_list_regions()
    test_list_income_levels()
    test_list_providers()
    test_list_indicators()
    test_list_indicators_with_filter()
    test_economic_indicators()
    test_health_indicators()
    test_environment_indicators()
    test_stats()
    print("\n=== All public tests passed! ===")
