"""Run all test suites."""

import subprocess
import sys

print("=" * 50)
print("RUNNING ALL TESTS")
print("=" * 50)
print("\nMake sure the server is running on http://127.0.0.1:6767\n")

tests = [
    ("Public API", "test_public.py"),
    ("Portal API", "test_portal.py"),
    ("Management API", "test_management.py"),
]

failed = []

for name, script in tests:
    print(f"\n{'=' * 50}")
    print(f"Running: {name}")
    print("=" * 50)

    result = subprocess.run([sys.executable, script], cwd="tests")

    if result.returncode != 0:
        failed.append(name)

print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)

if failed:
    print(f"✗ Failed: {', '.join(failed)}")
else:
    print("✓ All test suites passed!")
