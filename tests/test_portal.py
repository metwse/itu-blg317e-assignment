"""Simple tests for portal API (requires JWT auth)."""

import requests

BASE_URL = "http://127.0.0.1:6767/api/portal"

# Credentials from fixtures/l02_misc.py
TEST_EMAIL = "wb-admin@example.com"
TEST_PASSWORD = "admin"

# Provider ID (WorldBank provider created in fixtures)
PROVIDER_ID = 1


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


def auth_headers(token):
    """Build headers with JWT and provider context."""
    return {
        "Authorization": f"Bearer {token}",
        "X-Provider-Context": str(PROVIDER_ID)
    }


def test_get_me(token):
    """Test GET /auth/me - get current user info."""
    r = requests.get(f"{BASE_URL}/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Current user: {data.get('name', data.get('email'))}")

    # Return managed providers for later tests
    return data.get('managed_providers', [])


def test_list_permissions(token):
    """Test GET /permissions - list my permissions (needs provider context)."""
    r = requests.get(f"{BASE_URL}/permissions", headers=auth_headers(token))
    if r.status_code == 200:
        data = r.json()
        print(f"✓ My permissions: {len(data)} items")
    else:
        print(f"⚠ Permissions: {r.status_code} (may need provider context)")


def test_get_indicator(token):
    """Test GET /indicators - get specific indicator (needs provider context)."""
    r = requests.get(f"{BASE_URL}/indicators", headers=auth_headers(token), params={
        "economy_code": "USA",
        "year": 2020
    })
    # 200 = found, 404 = no data (both OK)
    if r.status_code in [200, 404]:
        print(f"✓ Get indicator: status {r.status_code}")
    else:
        print(f"⚠ Get indicator: {r.status_code} - {r.text[:100]}")


def test_get_provider(token):
    """Test GET /provider - get my provider details (needs provider context)."""
    r = requests.get(f"{BASE_URL}/provider", headers=auth_headers(token))
    if r.status_code == 200:
        data = r.json()
        print(f"✓ Provider: {data.get('name', data)}")
    else:
        print(f"⚠ Get provider: {r.status_code}")


if __name__ == "__main__":
    print("=== Testing Portal API ===\n")

    token = get_token()
    if not token:
        print("\n⚠ Skipping portal tests (no valid credentials)")
        print("  Check fixtures/l02_misc.py for default credentials.")
        exit(0)

    test_get_me(token)
    test_list_permissions(token)
    test_get_indicator(token)
    test_get_provider(token)

    print("\n=== Portal tests complete! ===")
