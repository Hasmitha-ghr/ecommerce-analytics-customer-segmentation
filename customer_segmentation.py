import pandas as pd

# Load cleaned data
df = pd.read_csv("cleaned_ecommerce_data.csv")

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Set analysis date
analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Create RFM table
rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (analysis_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()

# Create RFM scores
rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    4,
    labels=[4, 3, 2, 1]
)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    4,
    labels=[1, 2, 3, 4]
)

# Convert scores to integers
rfm["R_Score"] = rfm["R_Score"].astype(int)
rfm["F_Score"] = rfm["F_Score"].astype(int)
rfm["M_Score"] = rfm["M_Score"].astype(int)

# Calculate total RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"]
    + rfm["F_Score"]
    + rfm["M_Score"]
)

# Customer segmentation function
def customer_segment(score):
    if score >= 10:
        return "High Value"
    elif score >= 7:
        return "Loyal"
    elif score >= 5:
        return "Regular"
    else:
        return "At Risk"

# Apply segmentation
rfm["Customer_Segment"] = rfm["RFM_Score"].apply(customer_segment)

# Display results
print(rfm.head())

print("\nCustomer Segment Distribution:")
print(rfm["Customer_Segment"].value_counts())

# Save segmentation data
rfm.to_csv("customer_segments.csv", index=False)

print("\nCustomer segmentation completed!")
print("customer_segments.csv saved successfully!")