"""Reads the structure of whatever database the .env points to."""

from sqlalchemy import MetaData, Table, inspect, text

metadata = MetaData()
reflected_tables: dict[str, Table] = {}


def get_server_info(engine) -> dict:
    """Postgres version and every database in the server."""
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version()")).scalar()
        # pg_database is shared by the whole server, so one connection sees them all
        databases = (
            conn.execute(
                text("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname")
            )
            .scalars()
            .all()
        )
    return {"version": version, "databases": list(databases)}


def get_schema_names(engine) -> list[str]:
    """Schemas in the connected database."""
    return inspect(engine).get_schema_names()


def get_tables(engine, schema: str) -> list[str]:
    """Table names in a schema."""
    return inspect(engine).get_table_names(schema=schema)


def get_views(engine, schema: str) -> list[str]:
    """View names in a schema."""
    return inspect(engine).get_view_names(schema=schema)


def get_table_detail(engine, schema: str, table: str) -> dict:
    """Columns, primary key and foreign keys of one table."""
    inspector = inspect(engine)
    columns = [
        {**col, "type": str(col["type"])} for col in inspector.get_columns(table, schema=schema)
    ]
    return {
        "columns": columns,
        "primary_key": inspector.get_pk_constraint(table, schema=schema),
        "foreign_keys": inspector.get_foreign_keys(table, schema=schema),
    }


def get_primary_key_columns(engine, schema: str, table: str) -> list[str]:
    """Columns that form the primary key of a table."""
    return inspect(engine).get_pk_constraint(table, schema=schema)["constrained_columns"]


def find_fk_relation(engine, schema: str, table_a: str, table_b: str) -> dict | None:
    """Foreign key joining two tables, or None if they are not related."""
    inspector = inspect(engine)
    for source, target in ((table_a, table_b), (table_b, table_a)):
        for fk in inspector.get_foreign_keys(source, schema=schema):
            if fk["referred_table"] == target:
                return {
                    "from_table": source,
                    "from_column": fk["constrained_columns"][0],
                    "to_table": target,
                    "to_column": fk["referred_columns"][0],
                }
    return None


def init_reflection(engine, schema: str = "public"):
    """Load every table of the schema once, so any of them can be queried."""
    if reflected_tables:
        return
    # Core reflect() instead of automap: automap hides link tables that only hold foreign keys
    metadata.reflect(bind=engine, schema=schema)
    for table in metadata.tables.values():
        reflected_tables[table.name] = table
