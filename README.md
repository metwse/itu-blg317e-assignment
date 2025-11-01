# World Bank Data Visualization
ITU Database Management Systems course, term project assignment repository.

## Development Database Setup
You can start a local PostgreSQL instance using the provided Dockerfile inside
the `db/` folder.

### Build the Image
```sh
cd db/
docker build -t blg317e-dev-db
```

### Run the Container
This setup maps the container’s internal PostgreSQL port `5432` to port `2345`
on your host machine.

You can change the host port (`2345`) if needed, just make sure to update the
`DATABASE_URL` accordingly. The internal container port (`5432`) should remain
unchanged.

```sh
docker run -d \
  --name blg317e-dev-db \
  -p 2345:5432 \
  blg317e-dev-db
```

This starts PostgreSQL with the initial schema defined in SQL files in `db/`.

### Cleanup
These commands stop and remove both the development and test database
containers. If you only want to remove one of them, simply pass its name as an
argument.

```sh
docker stop blg317e-dev-db
docker rm --force blg317e-dev-db
```

## License
This project licensed under the AGPL-3.0 license.
