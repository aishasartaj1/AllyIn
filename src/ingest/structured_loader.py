import duckdb
import pandas as pd
import os

# Load CSVs
customers = pd.read_csv("data/structured/customers.csv")
orders = pd.read_csv("data/structured/orders.csv")
flags = pd.read_csv("data/structured/flags.csv")

# Normalize column names + convert to DATE
flags.columns = flags.columns.str.strip()
flags["date"] = pd.to_datetime(flags["date"]).dt.date  # ✅ force to DATE, not TIMESTAMP
print("Flags DataFrame:")
print(flags)


# Ensure folder exists
os.makedirs("data/structured", exist_ok=True)

if os.path.exists("data/structured/data.duckdb"):
    os.remove("data/structured/data.duckdb")

# Create a persistent DuckDB file
con = duckdb.connect("data/structured/data.duckdb")

# Save tables
con.execute("CREATE OR REPLACE TABLE customers AS SELECT * FROM customers")
con.execute("CREATE OR REPLACE TABLE orders AS SELECT * FROM orders")
con.execute("CREATE OR REPLACE TABLE flags AS SELECT * FROM flags")

# ✅ Query to validate flagged clients (last 12 months)
result = con.sql("""
    SELECT c.name AS client_name, f.flag_type, f.date
    FROM customers c
    JOIN flags f ON c.customer_id = f.client_id
    WHERE f.flag_type = 'restatement'
      AND f.date >= CURRENT_DATE - INTERVAL '12 months'
""").df()

print(result)
print("✅ DuckDB file updated and saved.")
