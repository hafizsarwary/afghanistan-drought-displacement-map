import json
import pandas as pd

# Load GeoJSON
with open('geoBoundaries-AFG-ADM1_simplified.geojson', 'r') as f:
    geo = json.load(f)

# Extract province names from GeoJSON
geo_names = sorted([f['properties']['shapeName'] for f in geo['features']])

# Load CSV
df = pd.read_csv('idp_ndvi_joined.csv')
csv_names = sorted(df['Province'].unique())

print("=== GeoJSON province names ===")
for n in geo_names:
    print(f"  {n}")

print(f"\n=== CSV province names ===")
for n in csv_names:
    print(f"  {n}")

print(f"\n=== In GeoJSON but NOT in CSV ===")
for n in geo_names:
    if n not in csv_names:
        print(f"  '{n}'")

print(f"\n=== In CSV but NOT in GeoJSON ===")
for n in csv_names:
    if n not in geo_names:
        print(f"  '{n}'")