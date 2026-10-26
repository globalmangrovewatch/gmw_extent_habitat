import pystac
import rasterio
import odc.stac

catalog_url = "/data/GlobalMangroveWatch/gmw_hab_extent/stac/gmw_stac_catalog/catalog.json"
catalog = pystac.Catalog.from_file(catalog_url)

# Target filter bounding box: [minx, miny, maxx, maxy]
target_bbox = [104.5, 8.5, 105.5, 10.0]


def intersects(bbox1, bbox2):
    # bbox format: [minx, miny, maxx, maxy]
    return not (
        bbox1[2] < bbox2[0]  # item max x < target min x
        or bbox1[0] > bbox2[2]  # item min x > target max x
        or bbox1[3] < bbox2[1]  # item max y < target min y
        or bbox1[1] > bbox2[3]  # item min y > target max y
    )


# Recursively retrieve items from the collection
matched_items = [
    item
    for item in catalog.get_items(recursive=True)
    if intersects(item.bbox, target_bbox)
]

print(f"Matched {len(matched_items)} items within bounding box.")

# GDAL tuning for HTTP range-request reading
gdal_env = {
    "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
    "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".tif,.tiff",
    "VSI_CACHE": "TRUE",
    "VSI_CACHE_SIZE": "50000000",  # 50 MB
}

with rasterio.Env(**gdal_env):
    ds = odc.stac.load(
        matched_items,
        bands=["gmw_habitat_mask"],
        crs="EPSG:4326",
        resolution=0.00025,
        bbox=target_bbox,  # Example AOI (e.g., Southern Vietnam / Mekong)
        chunks={"x": 2048, "y": 2048},
        resampling="nearest",
    )

print(ds)