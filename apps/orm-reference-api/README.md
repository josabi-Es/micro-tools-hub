# Postgres Explorer

Browse any PostgreSQL database through a REST API, one level at a time: server, database, schema, table, rows and joins. It reads the structure of the database at startup, so it works with tables you never described in code.

Point `POSTGRES_DB` at another database, restart, and you are exploring that one instead. No code changes.

## Levels

| Level | Endpoint | Needs key |
|---|---|---|
| 0 | `GET /health` the app is running | no |
| 0 | `GET /ready` the app can reach Postgres | no |
| 1 | `GET /server/info` Postgres version and every database in the server | yes |
| 2 | `GET /database` the database in use and its schemas | yes |
| 3 | `GET /schemas/{schema}/tables` tables in a schema | yes |
| 3 | `GET /schemas/{schema}/views` views in a schema | yes |
| 4 | `GET /schemas/{schema}/tables/{table}` columns, keys and relations | yes |
| 5 | `GET /data/{table}` read rows, up to 100 | yes |
| 5 | `POST /data/{table}` add a row | yes |
| 5 | `DELETE /data/{table}/{id}` remove a row | yes |
| 6 | `GET /data/{table}/joins?with={other}` join two related tables | yes |

Good to know:

* Deleting a row that another table still points at is refused with a `400`. Nothing is deleted behind your back.
* Link tables that only hold foreign keys are listed and can be joined like any other table.
* `DELETE` needs a table whose primary key is a single column. Tables with a composite key answer `400` and explain why.
* Sending a column that does not exist in a `POST` answers `400` with the offending names.

## Setup

```bash
cp .env.template .env
```

Fill in your Postgres details and pick a key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Using the key

Every endpoint except `/health` and `/ready` needs the key in a header:

```bash
curl -H "X-API-Key: your_key" http://localhost:8000/database
```

In Swagger (`/docs`), press **Authorize**, paste the key, press **Authorize** again and then **Close**. Without that step the browser sends no header and you get a `401`.

A `401` tells you which part is wrong: no header sent, header sent with the wrong value, or no key set on the server.

## Run locally

```bash
uv sync
uv run uvicorn main:app --reload
```

A quick walk through the levels:

```bash
KEY=your_key
curl -H "X-API-Key: $KEY" localhost:8000/server/info
curl -H "X-API-Key: $KEY" localhost:8000/database
curl -H "X-API-Key: $KEY" localhost:8000/schemas/public/tables
curl -H "X-API-Key: $KEY" localhost:8000/schemas/public/tables/task
curl -H "X-API-Key: $KEY" localhost:8000/data/task
curl -H "X-API-Key: $KEY" "localhost:8000/data/task/joins?with=project"
```

## Run with Docker

The `.env` file is left out of the image on purpose, so pass the values when you start the container:

```bash
docker build -t orm-reference-api .
docker run -p 8000:8000 \
  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=mydb -e POSTGRES_HOST=host.docker.internal -e POSTGRES_PORT=5432 \
  -e API_KEY=your_key \
  orm-reference-api
```

## Not included

Free SQL queries are left out on purpose. Every read goes through the levels above.
