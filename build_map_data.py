import json
import pandas as pd

# === Name mapping: CSV name -> GeoJSON name ===
name_map = {
    'Ghazni':    'Ghanzi',
    'Jawzjan':   'Jowzjan',
    'Nimroz':    'Nimruz',
    'Paktya':    'Paktia',
    'Panjsher':  'Panjshir',
    'Sar-e-Pul': 'Sar-e Pol',
}

# Load CSV
df = pd.read_csv('idp_ndvi_joined.csv')

# Apply name mapping
df['geo_name'] = df['Province'].replace(name_map)

# Load GeoJSON
with open('geoBoundaries-AFG-ADM1_simplified.geojson', 'r') as f:
    geo = json.load(f)

# Inject data into GeoJSON properties
for feature in geo['features']:
    geo_name = feature['properties']['shapeName']
    feature['properties']['data'] = {}

    for year in [2020, 2021, 2022]:
        row = df[(df['geo_name'] == geo_name) & (df['year'] == year)]
        if not row.empty:
            feature['properties']['data'][str(year)] = {
                'idp': int(row.iloc[0]['IDP_total']),
                'ndvi': round(float(row.iloc[0]['NDVI_anomaly']), 6),
                'province': row.iloc[0]['Province']
            }
        else:
            feature['properties']['data'][str(year)] = {
                'idp': 0,
                'ndvi': 0,
                'province': geo_name
            }

# Save enriched GeoJSON
with open('afghanistan_data.geojson', 'w') as f:
    json.dump(geo, f)

print("✅ afghanistan_data.geojson created")

# Verify
matched = 0
for feature in geo['features']:
    d = feature['properties']['data']
    if d['2021']['idp'] > 0:
        matched += 1
        
print(f"✅ {matched}/34 provinces have 2021 IDP data")