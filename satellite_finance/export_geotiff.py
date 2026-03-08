import ee

ee.Initialize(project='time-management-app-483902')

# 座標とバッファ（メートル）
lat = 32.886086283776294
lon = 130.84312137370827
buffer_m = 1000  # 周囲1km

roi = ee.Geometry.Point([lon, lat]).buffer(buffer_m)

def get_s2_median(start_date, end_date):
    return ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .median() \
        .select(['B4', 'B3', 'B2'])  # RGB

images = {
    '2020_spring': get_s2_median('2020-03-01', '2020-05-31'),
    '2022_autumn': get_s2_median('2022-09-01', '2022-11-30'),
    '2024_spring': get_s2_median('2024-03-01', '2024-05-31'),
    '2025_autumn': get_s2_median('2025-09-01', '2025-11-30'),
}

for name, image in images.items():
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=f'tsmc_{name}',
        folder='tsmc_geotiff',
        fileNamePrefix=f'tsmc_{name}',
        region=roi,
        scale=10,  # Sentinel-2の解像度（10m）
        crs='EPSG:4326',
        fileFormat='GeoTIFF',
        maxPixels=1e9,
    )
    task.start()
    print(f"Export started: tsmc_{name} (task id: {task.id})")

print("\nGoogle Drive の 'tsmc_geotiff' フォルダに保存されます。")
print("完了まで数分かかります。GEEのタスクページで確認できます：")
print("https://code.earthengine.google.com/tasks")
