from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from logger_config import logger
from models.database import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT, get_db, get_engine
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from utils.auth import verify_api_key
from utils.reflection import (
    find_fk_relation,
    get_primary_key_columns,
    get_schema_names,
    get_server_info,
    get_table_detail,
    get_tables,
    get_views,
    init_reflection,
    reflected_tables,
)

app = FastAPI(title="Postgres Explorer")
logger.info("Postgres Explorer API started")

explorer = APIRouter(dependencies=[Depends(verify_api_key)])


def get_table(table_name: str):
    """Find a reflected table by name, or fail with a clear 404."""
    init_reflection(get_engine())
    table = reflected_tables.get(table_name)
    if table is None:
        logger.warning(f"Table '{table_name}' does not exist in the database")
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    return table


# Level 0: health checks, open without a key


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    """Say the app is running."""
    logger.info("GET /health")
    return {"status": "ok"}


@app.get("/ready", tags=["Health"])
def ready(db: Session = Depends(get_db)) -> dict[str, str]:
    """Check the app can really reach Postgres."""
    logger.info("GET /ready, checking the database")
    db.execute(text("SELECT 1"))
    logger.info("GET /ready, database answered")
    return {"status": "ok"}


# Level 1: the Postgres server


@explorer.get("/server/info", tags=["Server"])
def server_info():
    """Postgres version and the databases it holds."""
    logger.info("GET /server/info")
    info = get_server_info(get_engine())
    return {"host": POSTGRES_HOST, "port": POSTGRES_PORT, **info}


# Level 2: the connected database


@explorer.get("/database", tags=["Database"])
def database_info():
    """The database in use and its schemas."""
    logger.info(f"GET /database, using {POSTGRES_DB}")
    return {"database": POSTGRES_DB, "schemas": get_schema_names(get_engine())}


# Level 3: what lives inside a schema


@explorer.get("/schemas/{schema_name}/tables", tags=["Schema"])
def list_schema_tables(schema_name: str):
    """Tables inside a schema."""
    logger.info(f"GET /schemas/{schema_name}/tables")
    tables = get_tables(get_engine(), schema_name)
    logger.info(f"GET /schemas/{schema_name}/tables, returned {len(tables)} tables")
    return {"schema": schema_name, "tables": tables}


@explorer.get("/schemas/{schema_name}/views", tags=["Schema"])
def list_schema_views(schema_name: str):
    """Views inside a schema."""
    logger.info(f"GET /schemas/{schema_name}/views")
    views = get_views(get_engine(), schema_name)
    logger.info(f"GET /schemas/{schema_name}/views, returned {len(views)} views")
    return {"schema": schema_name, "views": views}


# Level 4: the shape of one table


@explorer.get("/schemas/{schema_name}/tables/{table_name}", tags=["Table"])
def table_structure(schema_name: str, table_name: str):
    """Columns, keys and relations of a table."""
    logger.info(f"GET /schemas/{schema_name}/tables/{table_name}")
    return get_table_detail(get_engine(), schema_name, table_name)


# Level 5: rows of any table


@explorer.get("/data/{table_name}", tags=["Data"])
def read_table_data(table_name: str, db: Session = Depends(get_db)):
    """Read the first rows of a table."""
    logger.info(f"GET /data/{table_name}")
    table = get_table(table_name)
    rows = db.execute(select(table).limit(100)).all()
    logger.info(f"GET /data/{table_name}, returned {len(rows)} rows")
    return [dict(row._mapping) for row in rows]


@explorer.post("/data/{table_name}", tags=["Data"])
def create_table_row(table_name: str, body: dict, db: Session = Depends(get_db)):
    """Add a row to a table."""
    logger.info(f"POST /data/{table_name} creating row")
    table = get_table(table_name)

    unknown_keys = set(body.keys()) - set(table.columns.keys())
    if unknown_keys:
        raise HTTPException(status_code=400, detail=f"Unknown columns: {sorted(unknown_keys)}")

    try:
        created = db.execute(table.insert().values(**body).returning(*table.columns)).one()
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc.orig)) from exc
    logger.info(f"POST /data/{table_name} created")
    return dict(created._mapping)


@explorer.delete("/data/{table_name}/{row_id}", tags=["Data"])
def delete_table_row(table_name: str, row_id: str, db: Session = Depends(get_db)):
    """Remove a row by its id."""
    logger.info(f"DELETE /data/{table_name}/{row_id}")
    table = get_table(table_name)

    pk_columns = get_primary_key_columns(get_engine(), "public", table_name)
    if len(pk_columns) != 1:
        # one value cannot point at one row here, so deleting could remove several
        raise HTTPException(
            status_code=400,
            detail=(
                f"Table '{table_name}' has {'no' if not pk_columns else 'a composite'} "
                f"primary key ({pk_columns or 'none'}); deleting by a single id is not supported."
            ),
        )

    pk_column = table.columns[pk_columns[0]]
    pk_value = int(row_id) if row_id.isdigit() else row_id
    if db.execute(select(table).where(pk_column == pk_value)).first() is None:
        raise HTTPException(status_code=404, detail=f"Row {row_id} not found in '{table_name}'")

    try:
        db.execute(table.delete().where(pk_column == pk_value))
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        logger.warning(f"DELETE /data/{table_name}/{row_id} blocked by a foreign key")
        raise HTTPException(status_code=400, detail=str(exc.orig)) from exc
    logger.info(f"DELETE /data/{table_name}/{row_id} deleted")
    return {"message": f"Row {row_id} deleted from '{table_name}'"}


# Level 6: two tables joined by a foreign key


@explorer.get("/data/{table_name}/joins", tags=["Joins"])
def join_tables(
    table_name: str,
    with_table: str = Query(alias="with"),
    db: Session = Depends(get_db),
):
    """Join two related tables and return the rows together."""
    logger.info(f"GET /data/{table_name}/joins?with={with_table}")
    table_a = get_table(table_name)
    table_b = get_table(with_table)

    relation = find_fk_relation(get_engine(), "public", table_name, with_table)
    if relation is None:
        logger.warning(f"No foreign key between '{table_name}' and '{with_table}'")
        raise HTTPException(
            status_code=400,
            detail=(
                f"No foreign key relation detected between '{table_name}' and "
                f"'{with_table}'. Only tables linked by a foreign key can be joined."
            ),
        )

    by_name = {table_name: table_a, with_table: table_b}
    left = by_name[relation["from_table"]].columns[relation["from_column"]]
    right = by_name[relation["to_table"]].columns[relation["to_column"]]

    names_a = [c.name for c in table_a.columns]
    names_b = [c.name for c in table_b.columns]
    statement = (
        select(*table_a.columns, *table_b.columns)
        .select_from(table_a.join(table_b, left == right))
        .limit(100)
    )
    rows = db.execute(statement).all()
    logger.info(f"GET /data/{table_name}/joins?with={with_table}, returned {len(rows)} rows")
    # keep each table apart, both usually have a column called id
    return {
        "relation": relation,
        "rows": [
            {
                table_name: dict(zip(names_a, row[: len(names_a)])),
                with_table: dict(zip(names_b, row[len(names_a) :])),
            }
            for row in rows
        ],
    }


app.include_router(explorer)
