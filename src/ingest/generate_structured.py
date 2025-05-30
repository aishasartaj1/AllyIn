import pandas as pd

# Customers data
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Acme Corp', 'Beta LLC', 'Gamma Inc', 'Delta Ltd', 'Epsilon GmbH'],
    'country': ['USA', 'UK', 'Germany', 'Canada', 'India']
})

# Orders data
orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105],
    'customer_id': [1, 1, 2, 4, 5],
    'amount': [250, 300, 450, 150, 600]
})

# Save to CSV
customers.to_csv('data/structured/customers.csv', index=False)
orders.to_csv('data/structured/orders.csv', index=False)

print("Sample structured CSVs generated.")
