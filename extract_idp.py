import pandas as pd

files = {
    'round11_2020': ('round11_2020.xlsx', 'Arrival IDPs 2020'),
    'round13_2021_june': ('round13_2021_june.xlsx', 'Arrival IDPs 2021'),
    'round14_2021_dec': ('round14_2021_dec.xlsx', 'Arrival IDPs 2021'),
    'round15_2022': ('round15_2022.xlsx', 'Arrival IDPs 2022'),
}

all_rounds = []

for name, (file, idp_col) in files.items():
    df = pd.read_excel(file, sheet_name='Map4_IDP_Arrival', header=2)
    
    # Keep only what we need
    df = df[['ADM1Code', 'Province', 'ADM2Code', 'District', idp_col]].copy()
    df.columns = ['ADM1Code', 'Province', 'ADM2Code', 'District', 'IDP_count']
    df['round'] = name
    df['year_col'] = idp_col
    
    # Drop empty rows
    df = df.dropna(subset=['Province', 'District'])
    df = df[df['Province'] != 'Province']  # remove any header rows
    
    all_rounds.append(df)
    print(f"✅ {name} — {len(df)} districts")

# Combine all rounds
combined = pd.concat(all_rounds, ignore_index=True)
combined.to_csv('idp_combined.csv', index=False)
print(f"\n✅ Combined file saved — {len(combined)} total rows")