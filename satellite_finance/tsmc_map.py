import ee
import folium

# GEEの初期化
ee.Initialize(project='time-management-app-483902')

# TSMC熊本工場（菊陽町）の中心座標
tsmc_lat = 32.8803
tsmc_lon = 130.8244
roi = ee.Geometry.Point([tsmc_lon, tsmc_lat])

# 雲が少ないSentinel-2の期間中央値画像を取得する関数
def get_s2_median(start_date, end_date):
    collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    return collection.median()

# 1. 建設前（キャベツ畑時代）
img_2020 = get_s2_median('2020-03-01', '2020-05-31')

# 2. 造成前〜初期
img_2022 = get_s2_median('2022-09-01', '2022-11-30')

# 3. 建屋完成期
img_2024 = get_s2_median('2024-03-01', '2024-05-31')

# 4. 量産開始後
img_2025 = get_s2_median('2025-09-01', '2025-11-30')

# 可視化パラメータ（RGB: True Color）
vis_params = {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 3000,
    'gamma': 1.4
}

# FoliumにGEEのレイヤーを追加するためのカスタムメソッド
def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; Google Earth Engine',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

folium.Map.add_ee_layer = add_ee_layer

# マップの描画
m = folium.Map(location=[tsmc_lat, tsmc_lon], zoom_start=15)
m.add_ee_layer(img_2020, vis_params, '2020年春 (建設前)')
m.add_ee_layer(img_2022, vis_params, '2022年春 (造成期)')
m.add_ee_layer(img_2024, vis_params, '2024年春 (完成期)')
m.add_ee_layer(img_2025, vis_params, '2025年春 (量産開始後)')
folium.LayerControl().add_to(m)

m.save('tsmc_progress_map.html')
print("マップを tsmc_progress_map.html として出力しました。")
