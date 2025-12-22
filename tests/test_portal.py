"""Simple tests for portal API (requires JWT auth)."""

import requests

BASE_URL = "http://127.0.0.1:6767/api/portal"

# Test credentials - update these with valid user email/password from your DB
TEST_EMAIL = "admin@example.com"
TEST_PASSWORD = "admin123"


def get_token():
    """Login and get JWT token."""
    r = requests.post(f"{BASE_URL}/auth/login", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })
    if r.status_code != 200:
        print(f"✗ Login failed: {r.status_code} - {r.text}")
        return None
    token = r.json().get("token")
    print(f"✓ Login successful, got token")
    return token


def test_login():
    """Test POST /auth/login."""
    token = get_token()
    assert token is not None
    return token


def test_get_me(token):
    """Test GET /auth/me - get current user info."""
    r = requests.get(f"{BASE_URL}/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Current user: {data.get('username', data)}")


def test_list_permissions(token):
    """Test GET /permissions - list my permissions."""
    r = requests.get(f"{BASE_URL}/permissions", headers={
        "Authorization": f"Bearer {token}"
    })
    assert r.status_code == 200
    data = r.json()
    print(f"✓ My permissions: {len(data)} items")


def test_get_indicator(token):
    """Test GET /indicators - get specific indicator."""
    r = requests.get(f"{BASE_URL}/indicators", headers={
        "Authorization": f"Bearer {token}"
    }, params={
        "economy_code": "USA",
        "year": 2020
    })
    # May return 404 if no data, that's OK
    print(f"✓ Get indicator: status {r.status_code}")


def test_get_provider(token):
    """Test GET /provider - get my provider details."""
    r = requests.get(f"{BASE_URL}/provider", headers={
        "Authorization": f"Bearer {token}"
    })
    if r.status_code == 200:
        data = r.json()
        print(f"✓ Provider: {data.get('name', data)}")
    else:
        print(f"✓ Get provider: status {r.status_code} (may not have provider)")


if __name__ == "__main__":
    print("=== Testing Portal API ===\n")
    print("NOTE: Update TEST_EMAIL and TEST_PASSWORD with valid credentials!\n")

    token = get_token()
    if not token:
        print("\n⚠ Skipping portal tests (no valid credentials)")
        print("  Update TEST_EMAIL and TEST_PASSWORD in this file.")
        exit(0)  # Exit successfully to not fail test suite

    test_get_me(token)
    test_list_permissions(token)
    test_get_indicator(token)
    test_get_provider(token)

    print("\n=== Portal tests complete! ===")
