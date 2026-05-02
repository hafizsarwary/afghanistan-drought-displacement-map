import pandas as pd

# --- Load both datasets ---
idp = pd.read_csv('idp_by_province.csv')
ndvi = pd.read_csv('ndvi_anomaly_provinces.csv')

# --- Standardize year column in IDP data ---
year_map = {
    'round11_2020': '2020',
    'round13_2021_june': '2021',
    'round14_2021_dec': '2021',
    'round15_2022': '2022'
}
idp['year'] = idp['round'].map(year_map)

# --- For 2021 take the max (Dec round is more complete) ---
idp = idp.sort_values('IDP_total', ascending=False)
idp = idp.drop_duplicates(subset=['Province', 'year'], keep='first')

# --- Standardize province names to uppercase for joining ---
idp['Province_upper'] = idp['Province'].str.strip().str.upper()
ndvi['Province_upper'] = ndvi['ADM1_NAME'].str.strip().str.upper()

# --- Join ---
# --- Fix year type ---
idp['year'] = idp['year'].astype(str)
ndvi['year'] = ndvi['year'].astype(str)

# --- Join ---
merged = pd.merge(idp, ndvi, on=['Province_upper', 'year'], how='inner')

# --- Keep clean columns ---
merged = merged[['ADM1Code', 'Province', 'year', 'IDP_total', 'mean']].copy()
merged.columns = ['ADM1Code', 'Province', 'year', 'IDP_total', 'NDVI_anomaly']

# --- Sort ---
merged = merged.sort_values(['Province', 'year'])

# --- Save ---
merged.to_csv('idp_ndvi_joined.csv', index=False)

print(f"✅ {len(merged)} rows joined")
print(f"✅ {merged['Province'].nunique()} provinces matched")
print("\nSample:")
print(merged.head(12).to_string(index=False))