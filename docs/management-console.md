# Management Console API `/management`
This API handles the high-level business logic for organization management.
It allows the onboarding of new Providers, management of User accounts, and
the assignment of data entry Permissions. Unlike the `/internal` layer, this
layer performs business validation (e.g., resolving IDs to names, ensuring
referential integrity) to support the UI.


## Resources
### Users
Manage the identities of system actors (Admins, Provider Admins, Data Clerks).

#### List All Users
Returns a list of all registered users.

* **Endpoint:** `GET /users`
* **Response:**
```json
[
  {
    "id": 4,
    "email": "me@metehanselvi.com",
    "name": "Metehan Selvi"
  },
  ...
]
```

#### Create User
Registers a new user in the system.

* **Endpoint:** `POST /users`
* **Body:**
```json
{
  "email": "me@metehanselvi.com",
  "password": "initial_secure_password",
  "name": "Metehan Selvi"
}

```

#### Delete User
Permanently removes a user.

* **Endpoint:** `DELETE /users/<id>`
* **Response:** `200 OK` (Returns deleted ID).

#### Reset Password
Administrative override to reset a user's password.

* **Endpoint:** `PATCH /users/<id>/reset-password`
* **Body:**
```json
{ "password": "new_password_123" }

```


### Providers (Institutions)
Manage the organizations responsible for entering data.

#### List Providers
Returns all providers with resolved User names for their administrative and
technical accounts.

* **Endpoint:** `GET /providers`
* **Response:**
```json
[
  {
    "id": 10,
    "name": "Turkey Statistics Agency",
    "description": "Official data provider for TUR",
    "website_url": "https://turkstat.gov.tr",
    "immutable": false,
    "administrative_account": { "id": 5, "name": "Metehan Selvi" },
    "technical_account": { "id": 6, "name": "John Doe" }
  }
]

```


#### Create Provider
Onboards a new institution. A valid `administrative_account` (User ID) is
mandatory.

* **Endpoint:** `POST /providers`
* **Body:**
```json
{
  "name": "Turkey Statistics Agency",
  "administrative_account": 5,  // User ID
  "technical_account": null,    // Optional
  "description": "...",
  "immutable": false
}

```


#### Update Provider
Used to assign a technical account, update description, or toggle login access.

* **Endpoint:** `PATCH /providers/<id>`
* **Body:** (All fields optional)
```json
{
  "technical_account": 6,
  "immutable": true
}

```


#### Delete Provider
Removes the provider and cascades delete to all their Permissions and
Indicators.

* **Endpoint:** `DELETE /providers/<id>`


### Permissions (Scope)
Controls *where* and *when* a Provider is allowed to enter data.

#### List Permissions
Fetches the active permissions for a specific provider.

* **Endpoint:** `GET /permissions`
* **Query Parameters:**
* `provider_id` (required): The ID of the provider to inspect.


* **Response:**
```json
[
  {
    "id": 101,
    "provider_id": 10,
    "scope": { "type": "economy", "value": "TUR" },
    "year_start": 2020,
    "year_end": 2025,
    "footnote": "Annual GDP updates"
  },
  {
    "id": 102,
    "provider_id": 10,
    "scope": { "type": "region", "value": "ECS" },
    "year_start": 2022,
    "year_end": 2022
  }
]

```


#### Grant Permission
Authorizes a provider to write data for a specific scope. \
*Note: You must provide **either** `economy_code` **OR** `region`, never both.*

* **Endpoint:** `POST /permissions`
* **Body:**
```json
{
  "provider_id": 10,
  "year_start": 2020,
  "year_end": 2025,
  "economy_code": "TUR", // Optional (Mutual exclusive with region)
  "region": null,        // Optional (Mutual exclusive with economy_code)
  "footnote": "Authorization ref #9988"
}

```


#### Revoke Permission
Removes a specific authorization rule.

* **Endpoint:** `DELETE /permissions/<id>`


## Data Dictionary & Rules
* **Role Constraint:** A `technical_account` must be an existing User ID.
* **Admin Constraint:** An `administrative_account` cannot be null; every
  provider must have an owner.
* **Scope XOR:** A Permission is strictly for an Economy (e.g., 'TUR') OR a
  Region (e.g., 'ECS'). It cannot apply to both simultaneously.
* **Immutable:** If `immutable` is set to `true` for a Provider, its accounts
  cannot authenticate via the Portal Layer to enter data, effectively freezing
  the provider without deleting it.
