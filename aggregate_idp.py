import pandas as pd

df = pd.read_csv('idp_combined.csv')

# Aggregate IDP count by Province and Round
province = df.groupby(['ADM1Code', 'Province', 'round', 'year_col'])['IDP_count'].sum().reset_index()

# Rename for clarity
province.columns = ['ADM1Code', 'Province', 'round', 'year', 'IDP_total']

# Sort
province = province.sort_values(['Province', 'round'])

# Save
province.to_csv('idp_by_province.csv', index=False)

print(f"✅ {len(province)} rows saved")
print(f"✅ {province['Province'].nunique()} unique provinces")
print("\nSample — top 10 rows:")
print(province.head(10).to_string(index=False))