import duckdb
import pandas as pd

def persist_to_duckdb(df: pd.DataFrame, table_name: str = "supplier_inventory"):
    """
    purpose: transitions the processed dataframe into an embedded OLAP (columnar) database.
    this allows for high-speed sql aggregations and acts as a localized state manager before shopify sync.
    parameters: 
        - df (pd.DataFrame): the fully processed inventory dataframe.
        - table_name (str): the target table name in the database (default: 'supplier_inventory').
    return values: 
        - duckdb.DuckDBPyConnection: an active connection object to query the in-memory database.
    errors: 
        - fails if the dataframe is empty or contains unsupported sql data types.
    side effects: 
        - creates an in-memory database instance that consumes ram until the connection is closed.
    """
    
    # establish an in-memory database connection. 
    # using ':memory:' ensures no disk I/O bottlenecks and cleans up automatically when the script ends.
    conn = duckdb.connect(database=':memory:')
    
    # dynamically execute a sql create table statement. 
    # duckdb can directly read the pandas 'df' object from the local python environment without copying the data.
    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    return conn