import ee
import geopandas as gpd
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

ee.Initialize(project='time-management-app-483902')

# shapefileを読み込んでee.Geometryに変換
shp = gpd.read_file('test/test.shp').to_crs('EPSG:4326')  # satellite_financeフォルダから実行すること
geojson = json.loads(shp.geometry.to_json())
roi = ee.Geometry(geojson['features'][0]['geometry'])

# 分析期間
periods = {
    '2020_spring_before_construction': ('2020-03-01', '2020-05-31'),
    '2022_autumn_grading':             ('2022-09-01', '2022-11-30'),
    '2024_spring_building_complete':   ('2024-03-01', '2024-05-31'),
    '2025_autumn_mass_production':     ('2025-09-01', '2025-11-30'),
}

def get_indices(start_date, end_date):
    img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .median()

    ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
    ndbi = img.normalizedDifference(['B11', 'B8']).rename('NDBI')
    bsi  = img.expression(
        '((SWIR + RED) - (NIR + BLUE)) / ((SWIR + RED) + (NIR + BLUE))',
        {'SWIR': img.select('B11'), 'RED': img.select('B4'),
         'NIR': img.select('B8'),  'BLUE': img.select('B2')}
    ).rename('BSI')

    stats = ndvi.addBands(ndbi).addBands(bsi).reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=roi,
        scale=10,
        maxPixels=1e9,
    )
    return stats.getInfo()

# 各期間の指標を計算
records = []
for label, (start, end) in periods.items():
    print(f"計算中: {label}")
    stats = get_indices(start, end)
    records.append({
        'period': label,
        'NDVI': round(stats.get('NDVI', float('nan')), 4),
        'NDBI': round(stats.get('NDBI', float('nan')), 4),
        'BSI':  round(stats.get('BSI',  float('nan')), 4),
    })

df = pd.DataFrame(records).set_index('period')
print("\n--- 結果 ---")
print(df)

# グラフ出力
fig, ax = plt.subplots(figsize=(10, 5))
df.plot(ax=ax, marker='o')
ax.set_title('TSMC Kumamoto Plant - Construction Progress Indices (Polygon Mean)')
ax.set_ylabel('Index Value')
ax.set_xlabel('Period')
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax.legend()
plt.tight_layout()
plt.savefig('tsmc_indices.png', dpi=150)
print("\nグラフを tsmc_indices.png として保存しました。")

# GeoJSON出力
features = []
for record in records:
    feature = {
        "type": "Feature",
        "geometry": json.loads(shp.geometry.to_json())['features'][0]['geometry'],
        "properties": record
    }
    features.append(feature)

geojson_output = {
    "type": "FeatureCollection",
    "features": features
}

with open('tsmc_indices.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson_output, f, indent=2, ensure_ascii=False)
print("結果を tsmc_indices.geojson として保存しました。")
