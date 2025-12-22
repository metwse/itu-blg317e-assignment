"""Simple tests for management console API (requires console token)."""

import requests

BASE_URL = "http://127.0.0.1:6767/management"

# From .env - update if different
CONSOLE_TOKEN = "management-console-token"

# Management API uses x-management-secret header, not Bearer token
HEADERS = {"x-management-secret": CONSOLE_TOKEN}


def test_list_users():
    """Test GET /users."""
    r = requests.get(f"{BASE_URL}/users", headers=HEADERS)
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Users: {len(data)} items")
    return data


def test_list_providers():
    """Test GET /providers."""
    r = requests.get(f"{BASE_URL}/providers", headers=HEADERS)
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Providers: {len(data)} items")
    return data


def test_list_permissions(provider_id):
    """Test GET /permissions - requires provider_id."""
    r = requests.get(f"{BASE_URL}/permissions", headers=HEADERS, params={
        "provider_id": provider_id
    })
    assert r.status_code == 200
    data = r.json()
    print(f"✓ Permissions for provider {provider_id}: {len(data)} items")


def test_create_and_delete_user():
    """Test POST /users and DELETE /users/<id>."""
    # Create
    r = requests.post(f"{BASE_URL}/users", headers=HEADERS, json={
        "username": "test_user_temp",
        "password": "test123",
        "name": "Test User"
    })
    if r.status_code in [200, 201]:
        user_id = r.json().get("id")
        print(f"✓ Created user: {user_id}")

        # Delete
        r = requests.delete(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
        if r.status_code == 200:
            print(f"✓ Deleted user: {user_id}")
        else:
            print(f"✗ Delete failed: {r.status_code}")
    else:
        print(f"⚠ Create user: {r.status_code} (may already exist)")


def test_create_and_delete_provider():
    """Test POST /providers and DELETE /providers/<id>."""
    # Create
    r = requests.post(f"{BASE_URL}/providers", headers=HEADERS, json={
        "name": "Test Provider Temp",
        "description": "Temporary test provider"
    })
    if r.status_code in [200, 201]:
        provider_id = r.json().get("id")
        print(f"✓ Created provider: {provider_id}")

        # Delete
        r = requests.delete(f"{BASE_URL}/providers/{provider_id}", headers=HEADERS)
        if r.status_code == 200:
            print(f"✓ Deleted provider: {provider_id}")
        else:
            print(f"✗ Delete failed: {r.status_code}")
    else:
        print(f"⚠ Create provider: {r.status_code}")


def test_unauthorized():
    """Test that requests without token are rejected."""
    r = requests.get(f"{BASE_URL}/users")
    assert r.status_code in [401, 403]
    print(f"✓ Unauthorized correctly blocked: {r.status_code}")


if __name__ == "__main__":
    print("=== Testing Management API ===\n")

    test_unauthorized()
    test_list_users()
    providers = test_list_providers()

    # Permissions require a provider_id
    if providers and len(providers) > 0:
        test_list_permissions(providers[0].get("id", 1))
    else:
        print("⚠ Skipping permissions test (no providers)")

    test_create_and_delete_user()
    test_create_and_delete_provider()

    print("\n=== Management tests complete! ===")
