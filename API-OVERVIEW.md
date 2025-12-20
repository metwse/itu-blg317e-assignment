# Backend Route Architecture & Security Layers Overview
The architecture strictly separates concerns based on the user's role and the
sensitivity of the operation.

See [docs/](docs/) for details.

## 1. Public Layer (Transparency)
**Base URL:** `/api/public` \
**Authentication:** `None` (Public Access) \
**Audience:** Guests, Researchers, Public Dashboard.

**Purpose:** Provides read-only access to published data. This layer returns
filtered, aggregated, and safe-to-consume data. It does not expose internal
IDs or sensitive metadata.


## 2. Portal Layer (Operations)
**Base URL:** `/api/portal` \
**Authentication:** `Authorization: Bearer <JWT>` \
**Context Header:** `X-Provider-Context: <provider_id>` (Required for data
  operations) \
**Audience:** Provider Admins, Technical Accounts (Data Clerks).

**Purpose:** Users log in here to enter data. Since a single user can manage
multiple institutions, the `X-Provider-Context` header determines which "hat"
the user is wearing during the request.


## 3. Management Layer (Organization)
**Base URL:** `/management` \
**Authentication:** `X-Management-Secret: <SECRET_KEY>` \
**Audience:** Operations Manager / System Owner (Via Management Console UI).

**Purpose:** Handles the business logic of the organization. This layer is used
to onboard new institutions (Providers), create user accounts, and assign
permissions. It abstracts away the raw database IDs into a user-friendly
management flow.


## 4. Internal Layer (Infrastructure / God Mode)
**Base URL:** `/internal` \
**Authentication:** `X-Super-Admin-Secret: <SECRET_KEY>` \
**Audience:** Super Admin, Setup Wizard, Automation Scripts.

**Purpose:** Direct, unrestricted access to the underlying database tables.
This layer bypasses many business validation rules and is used for debugging,
initial system setup (The Wizard), or bulk data migration scripts.

This routes auto-generated, follows the scheme:
* `GET /internal/<table_name>?limit=n&offset=m`: Lists the elements
* `POST /internal/<table_name>`: Raw insert, e.g. without permissions check
* `GET /internal/<table_name>/<id>`: Fetch one element
* `DELETE /internal/<table_name>/<id>`: Hard delete
* `PATCH /internal/<table_name>/<id>`: Update

If a table has a composite primary key, the id field in its internal routes
will be combination of all of its keys. E.g. for indicators table, id written
as `<provider_id>/<economy_code>/<year>`,
