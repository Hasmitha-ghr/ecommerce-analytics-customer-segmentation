import pandas as pd

# Load dataset
df = pd.read_excel("Online Retail.xlsx")

print("Original shape:", df.shape)

# Remove duplicates
df = df.drop_duplicates()

# Remove missing Customer IDs
df = df.dropna(subset=["CustomerID"])

# Remove cancelled orders
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Remove invalid quantity
df = df[df["Quantity"] > 0]

# Remove invalid prices
df = df[df["UnitPrice"] > 0]

# Create Revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Create date features
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["MonthName"] = df["InvoiceDate"].dt.month_name()
df["Day"] = df["InvoiceDate"].dt.day
df["Hour"] = df["InvoiceDate"].dt.hour

# Convert CustomerID
df["CustomerID"] = df["CustomerID"].astype(int)

# Save cleaned dataset
df.to_csv("cleaned_ecommerce_data.csv", index=False)

print("Cleaned shape:", df.shape)
print(df.head())

print("Dataset saved successfully!")
print("\nFINAL DATA CHECK")
print("Total Rows:", len(df))
print("Total Revenue:", df["Revenue"].sum())
print("Total Orders:", df["InvoiceNo"].nunique())
print("Total Customers:", df["CustomerID"].nunique())
print("Minimum Date:", df["InvoiceDate"].min())
print("Maximum Date:", df["InvoiceDate"].max())