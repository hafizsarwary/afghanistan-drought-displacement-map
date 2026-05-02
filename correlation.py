import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('idp_ndvi_joined.csv')

# Force correct types
df['year'] = df['year'].astype(int)
df['IDP_total'] = pd.to_numeric(df['IDP_total'], errors='coerce')
df['NDVI_anomaly'] = pd.to_numeric(df['NDVI_anomaly'], errors='coerce')
df = df.dropna(subset=['IDP_total', 'NDVI_anomaly'])

print("=== Correlation: NDVI Anomaly vs IDP count ===\n")
for year in [2020, 2021, 2022]:
    subset = df[df['year'] == year]
    r, p = stats.pearsonr(subset['NDVI_anomaly'], subset['IDP_total'])
    print(f"{year}: r = {r:.3f}, p-value = {p:.4f}, n = {len(subset)}")

r, p = stats.pearsonr(df['NDVI_anomaly'], df['IDP_total'])
print(f"\nOverall: r = {r:.3f}, p-value = {p:.4f}, n = {len(df)}")

# --- Plot ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
years = [2020, 2021, 2022]
colors = ['#2196F3', '#F44336', '#FF9800']

ymax = df['IDP_total'].max() * 1.1
print(f"\nY axis max will be: {ymax}")

for i, (year, color) in enumerate(zip(years, colors)):
    subset = df[df['year'] == year].copy()
    print(f"\n{year} — {len(subset)} rows, IDP range: {subset['IDP_total'].min()} to {subset['IDP_total'].max()}")
    
    x = subset['NDVI_anomaly'].values
    y = subset['IDP_total'].values
    
    axes[i].scatter(x, y, color=color, alpha=0.7, s=60)
    axes[i].set_ylim(0, ymax)
    axes[i].set_title(f'{year}', fontsize=13, fontweight='bold')
    axes[i].set_xlabel('NDVI Anomaly')
    axes[i].set_ylabel('IDP Count')
    axes[i].axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    
    # Label high IDP provinces
    for _, row in subset.iterrows():
        if row['IDP_total'] > 50000:
            axes[i].annotate(row['Province'],
                           (row['NDVI_anomaly'], row['IDP_total']),
                           fontsize=7, ha='right')

plt.suptitle('NDVI Anomaly vs IDP Displacement — Afghanistan',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_plot.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Plot saved")