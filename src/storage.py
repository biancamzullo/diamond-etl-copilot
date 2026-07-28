import duckdb
import pandas as pd

def persist_to_duckdb(df: pd.DataFrame, table_name: str = "supplier_inventory"):
    """Persists processed DataFrame to DuckDB in-memory store."""
    conn = duckdb.connect(database=':memory:')
    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    return conn