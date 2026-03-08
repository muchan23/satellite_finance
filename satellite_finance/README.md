# TSMC Kumamoto Plant - Construction Progress Analysis

Satellite-based analysis of TSMC's Kumamoto plant (Kikuyo Town) construction progress using Google Earth Engine (GEE) and Sentinel-2 imagery.

## Overview

This project tracks land cover changes around the TSMC Kumamoto factory site across four key periods — from farmland (2020) through mass production (2025) — using spectral indices derived from Sentinel-2 satellite data.

## Analysis Periods

| Period | Date Range | Description |
|---|---|---|
| 2020 Spring | 2020-03-01 – 2020-05-31 | Before construction (cabbage fields) |
| 2022 Autumn | 2022-09-01 – 2022-11-30 | Land grading phase |
| 2024 Spring | 2024-03-01 – 2024-05-31 | Building completion |
| 2025 Autumn | 2025-09-01 – 2025-11-30 | After mass production begins |

## Spectral Indices

| Index | Formula | Interpretation |
|---|---|---|
| **NDVI** | (NIR - RED) / (NIR + RED) | Vegetation: higher = more green cover |
| **NDBI** | (SWIR - NIR) / (SWIR + NIR) | Built-up area: higher = more artificial surfaces |
| **BSI** | ((SWIR + RED) - (NIR + BLUE)) / ((SWIR + RED) + (NIR + BLUE)) | Bare soil: higher = more exposed ground |

## Files

```
satellite_finance/
├── analyze_indices.py       # Compute NDVI/NDBI/BSI and export GeoJSON + PNG
├── export_geotiff.py        # Export Sentinel-2 RGB images to Google Drive as GeoTIFF
├── tsmc_map.py              # Generate interactive Folium map (HTML)
├── test/                    # Shapefile defining the ROI polygon
│   ├── test.shp
│   └── ...
├── tsmc_indices.geojson     # Output: indices per period with ROI geometry
├── tsmc_indices.png         # Output: time-series chart of indices
└── tsmc_progress_map.html   # Output: interactive map with layer toggle
```

## Results

| Period | NDVI | NDBI | BSI |
|---|---|---|---|
| 2020 Spring (before construction) | 0.5243 | -0.0457 | -0.0173 |
| 2022 Autumn (grading) | 0.3754 | 0.0016 | 0.0249 |
| 2024 Spring (building complete) | 0.3543 | -0.0250 | 0.0065 |
| 2025 Autumn (mass production) | 0.1987 | 0.0108 | 0.0584 |

**Key observations:**
- NDVI dropped from 0.52 → 0.20, confirming the loss of agricultural land
- BSI increased steadily, reflecting land clearing and construction activity
- NDBI rose gradually, indicating growth in built-up surfaces

## Requirements

```
earthengine-api
geopandas
pandas
matplotlib
folium
```

Install dependencies:

```bash
pip install earthengine-api geopandas pandas matplotlib folium
```

## Usage

Authenticate with Google Earth Engine before running:

```bash
earthengine authenticate
```

Run each script from inside the `satellite_finance/` directory:

```bash
# Compute indices and export GeoJSON
python analyze_indices.py

# Export GeoTIFF images to Google Drive
python export_geotiff.py

# Generate interactive HTML map
python tsmc_map.py
```

## Data Source

- **Satellite**: Sentinel-2 SR Harmonized (`COPERNICUS/S2_SR_HARMONIZED`)
- **Platform**: Google Earth Engine
- **Resolution**: 10m
- **Cloud filter**: < 20% cloud cover, median composite
