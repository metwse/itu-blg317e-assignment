# World Bank Data Visualization
The term project for the ITU Database Management Systems (BLG 317E) course.
This application provides a web-based interface for visualizing data from the
World Bank.

## Direct Database Access API
The direct data management routes are protected and grouped under the
`/internal` prefix. Routes in this group are not enabled by default, you can
enable them by setting `INTERNAL_ACCESS_TOKEN` environment variable.

## Quick Start
This is the fastest way to get the entire project (application and database)
running. This method uses the settings in the `docker-compose.yml` file.

Steps:
1. Run the project using Docker Compose:
   ```sh
   docker compose up -d
   ```
2. That's it!
    - The application will be accessible at `http://localhost:6767`.
    - The PostgreSQL database will be exposed on port `1234` for debugging.

## Loading Fixtures
You can fetch WorldBank data and load into database using `fixtures` module.
`fixtures` keep track of loaded tables with `.load_status` file, and loading
continues from last completed step if it has been interrupted. Also, database
configuration of fixtures also read from `.env` and environment variables.

You can load initial data using:
```
python3 -m fixtures
```

## Architecture & Design Pattern
This project implements a layered architecture with a heavy reliance on Python
generics TypeVar to minimize code duplication.

### The "Generic Trio" Pattern
The entire internal backend resolves around three generic types:
1. `T (Entity):` The database entity (e.g., `Provider`).
2. `U (UpdateDTO):` Data transfer object for updates (e.g.,
   `ProviderUpdateDto`).
3. `C (CreateDTO):` Data transfer object for creation (e.g.,
   `ProviderCreateDto`).

### Layers
1. **Handlers (Presentation Layer):** \
   Inherits from `BaseHandler[T, U, C]`. Automatically handles HTTP parsing,
   validation, and standard responses (200 OK, 201 Created, 404 Not Found).
2. **Services (Business Layer):** \
   Inherits from `BaseService[T, U, C]`. Acts as the bridge between handlers
   and repositories.
3. **Repositories (Data Access Layer):** \
   Inherits from `BaseRepo[T, U, C]`. \
   **Dynamic SQL Generation:** Instead of writing SQL for every table, the
   `BaseRepo` inspects the Pydantic models at runtime to generate `INSERT`,
   `UPDATE`, and `SELECT` statements automatically.
4. **State (Dependency Injection):**
   The `State` class acts as a container, initializing all services with the
   database pool and injecting dependencies where needed.

## Manual Development Setup
This method is for development if you want to run the database in Docker but
run the application service (Python) locally on your host machine.

### Configuration
The application reads its configuration from environment variables, which can
be loaded from a `.env` file.

Copy the example file:
```sh
cp .env.example .env
```

You can keep the configuration provided in `.env.example` the same in this
setup.

### Build & Run the Database
This will build a custom Docker image for the database (which includes the
initial schema) and run it as a container.

1. Navigate to the db directory and build the image:
   ```sh
   cd db/
   docker build -t blg317e-dev-db .
   ```
2. Run the database container:
   ```sh
   docker run -d \
       --name blg317e-dev-db \
       -p 127.0.0.1:2345:5432 \
       blg317e-dev-db
   ```
   Here, we specified `localhost` to not expose the database to public.

This setup maps the container’s internal PostgreSQL port `5432` to port `2345`
on your host machine.

You can change the host port (`2345`) if needed, just make sure to update the
`DATABASE_URL` accordingly. The internal container port (`5432`) should remain
unchanged.

### Run the Application
You can run the back end service with `python3 -m src` command, after
installing dependencies in `requirements.txt` with
`pip install -r requirements.txt`.

### Cleanup
To stop and remove the manual development database container:

```sh
docker stop blg317e-dev-db
docker rm blg317e-dev-db
```

## License
This project licensed under the AGPL-3.0 license. See the `LICENSE` file for
details.

## Why is There a `package.json`?
Some editors require an `eslint.config.js` to properly lint JavaScript. The
project itself does not depend on `npm`, you do not need `node` in order to run
this project.
