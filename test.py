import duckdb

con = duckdb.connect("data/structured/data.duckdb")
print("DuckDB says today is:", con.sql("SELECT CURRENT_DATE").fetchall())

