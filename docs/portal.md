# Portal API `/api/portal`
This API handles the day-to-day data entry operations. It is the primary
interface for Provider Administrators and Technical Accounts to submit
economic, health, and environmental data.

Unlike the public layer, this layer requires **JWT Authentication**.
Furthermore, since a single user may manage multiple providers, all data
manipulation endpoints require a **Context Header** to specify which
institution the user is acting on behalf of.

## Authentication & Headers
* **Authorization:** `Bearer <JWT_TOKEN>` (Required for all except
  `/auth/login`)
* **Context Header:** `X-Provider-Context: <provider_id>` (Required for
  `Permissions` and `Indicators` resources)

## Resources
### Authentication
Manage session initiation and user context resolution.

#### Login
Authenticates a user and returns a JWT token.

* **Endpoint:** `POST /auth/login`
* **Body:**

```json
{
  "email": "me@metehanselvi.com",
  "password": "my_secure_password"
}

```

* **Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1Ni..."
}

```

#### Get Current User (Me)
Returns the currently logged-in user's profile and a list of Providers they
are authorized to manage. The frontend should use the `managed_providers` list
to populate the "Context Switcher" dropdown.

* **Endpoint:** `GET /auth/me`
* **Response:**

```json
{
  "id": 4,
  "name": "Metehan Selvi",
  "email": "me@metehanselvi.com",
  "managed_providers": [
    {
      "id": 10,
      "name": "Turkey Statistics Agency",
      "role": "admin" // or "technical"
    },
    {
      "id": 15,
      "name": "Health Ministry Data Unit",
      "role": "technical"
    }
  ]
}

```

### Permissions (Read-Only)
Allows the portal user to see *where* they are allowed to enter data for the
current context.

#### List My Permissions
Fetches the active permission scopes for the selected Provider Context.

* **Endpoint:** `GET /permissions`
* **Response:**

```json
[
  {
    "id": 101,
    "scope": "TUR", // Economy Code
    "type": "economy",
    "year_start": 2020,
    "year_end": 2025
  },
  {
    "id": 102,
    "scope": "ECS", // Region Code
    "type": "region",
    "year_start": 2023,
    "year_end": 2023
  }
]

```

### Indicators (Data Entry)
The core resource for uploading statistical data. Handles the unified
`indicators` table.

#### Upsert Indicator
Inserts or Updates indicator data for a specific Economy and Year. \
*This endpoint uses the Unified Table structure, accepting Economic, Health,
and Environment fields in a single payload.*

* **Endpoint:** `POST /indicators`
* **Body:**
```json
{
  "economy_code": "TUR",
  "year": 2024,

  // Economic Fields (Optional)
  "gdp_per_capita": 12000.50,
  "industry": 32.5,

  // Health Fields (Optional)
  "diabetes_prevalence": 5.4,
  "community_health_workers": null,

  // Environment Fields (Optional)
  "access_to_electricity": 100.0,
  "energy_use": 500.2
}

```

* **Response:** `200 OK` (If updated) or `201 Created` (If new).

#### Get Indicator (Check Existing)
Fetches existing data for a specific Economy/Year to display in the edit form.

* **Endpoint:** `GET /indicators`
* **Query Parameters:**
* `economy_code` (required)
* `year` (required)


* **Response:**
```json
{
  "provider_id": 10,
  "economy_code": "TUR",
  "year": 2024,
  "gdp_per_capita": 12000.50,
  "diabetes_prevalence": 5.4,
  ...
}

```

## Data Dictionary & Rules
* **Context Requirement:** The backend will strictly validate that the user ID
  extracted from the JWT is associated (as Admin or Technical) with the
  `provider_id` sent in the `X-Provider-Context` header. If they don't match,
  a `403 Forbidden` is returned.
* **Permission Check:** Before writing to `POST /indicators`, the system checks
  the `permissions` table. If the provider does not have a valid permission for
  the requested `economy_code` (or its parent Region) and `year`, the request
  is rejected.
* **Unified Upsert:** The system uses an `ON CONFLICT DO UPDATE` strategy. If
  data for that `provider + economy + year` already exists, it updates only the
  non-null fields provided in the payload (Partial Update).
