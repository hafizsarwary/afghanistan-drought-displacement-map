# Afghanistan Drought & Displacement Map

**Live map → [hafizsarwary.github.io/afghanistan-drought-displacement-map](https://hafizsarwary.github.io/afghanistan-drought-displacement-map/)**

---

## Why I built this

In 2021, Afghanistan went through one of the worst years in its recent history. The government collapsed, the regime changed, and at the same time the country was hit by one of the worst droughts in decades. Afghanistan runs heavily on agriculture — when the land dries up, people have no choice but to leave.

I wanted to see what this actually looked like in data. Not in a report, not in a news article — in satellite imagery and real displacement numbers. So I built this.

---

## What it shows

An interactive map of Afghanistan showing:
- **Drought severity** per province (from NASA satellite data) for 2020, 2021, and 2022
- **Displacement numbers** per province (from IOM field surveys)
- Switch between years to see how the crisis evolved

Click any province to see the exact numbers and what they mean.

---

## The finding that surprised me

I expected provinces with the worst drought to have the highest displacement numbers. That's not what the data showed.

Kabul and Balkh — which had near-normal vegetation — recorded the most displaced people. Because people were fleeing *to* them, not from them. The drought was destroying rural livelihoods in the west and north, and people were moving toward the cities.

**Drought-driven displacement is directional.** That's not something you see in a table — you need to map it.

---

## How I built it

### Data sources
- **NASA MODIS MOD13A3** — monthly vegetation index at 1km resolution, accessed via Google Earth Engine
- **IOM Displacement Tracking Matrix** — Baseline Mobility Assessment Rounds 11–15 (2020–2022), downloaded from dtm.iom.int
- **geoBoundaries ADM1** — Afghanistan province boundaries

### Process
1. Loaded MODIS NDVI in Google Earth Engine and computed a 5-year baseline (2015–2019)
2. Calculated NDVI anomaly per year — how much worse or better vegetation was compared to the baseline
3. Extracted mean anomaly per province using zonal statistics
4. Downloaded and cleaned IOM displacement data from 4 rounds of field surveys (Excel files with non-standard headers)
5. Aggregated district-level IDP counts to province level
6. Joined the satellite data with the displacement data — ran into 6 province name mismatches between datasets, fixed with a manual mapping dictionary
7. Ran a Pearson correlation test — result was not significant (r=0.014, p=0.94 for 2021), which is actually the finding, not a failure
8. Embedded the joined data into the GeoJSON province boundaries
9. Built the interactive map with Leaflet.js

### Tools
`Google Earth Engine` `Python` `pandas` `scipy` `Leaflet.js` `GeoJSON`

---

## Files in this repo

| File | What it does |
|------|-------------|
| `index.html` | The complete interactive web map |
| `afghanistan_data.geojson` | Province boundaries with NDVI + IDP data embedded |
| `extract_idp.py` | Extracts IDP arrival data from IOM Excel files |
| `aggregate_idp.py` | Aggregates district-level data to province level |
| `join_data.py` | Joins NDVI anomaly data with IDP data |
| `build_map_data.py` | Enriches GeoJSON with the joined dataset |
| `correlation.py` | Pearson correlation analysis + scatter plots |
| `check_names.py` | Checks province name mismatches between datasets |

---

## Limitations

- IDP data doesn't separate drought displacement from conflict displacement — both are mixed in the IOM counts
- NDVI is a proxy for vegetation health, not a direct drought measurement
- Helmand and Herat provinces had no IDP data in the downloaded rounds
- Provincial averages hide variation within provinces

---

## Data credits

- NASA / USGS — MODIS MOD13A3 v061
- IOM DTM Afghanistan — dtm.iom.int
- geoBoundaries — geoboundaries.org
- Google Earth Engine — earthengine.google.com