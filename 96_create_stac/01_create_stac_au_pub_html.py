from datetime import datetime, timezone
import pystac
from rio_stac import create_stac_item
import glob
import rsgislib.tools.filetools
import tqdm

STAC_URL = "https://users.aber.ac.uk/pfb/gmw_stac"
BASE_URL = "https://users.aber.ac.uk/pfb/gmw_stac/gmw_hab_v30_tiles/"

# 1. Define the Catalog / Collection
collection = pystac.Collection(
    id="gmw-habitat-mask",
    description="Global Mangrove Watch (GMW) baseline habitat mask layers.",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent(bboxes=[[-180.0, -90.0, 180.0, 90.0]]),
        temporal=pystac.TemporalExtent(
            intervals=[
                [
                    datetime(1985, 1, 1, tzinfo=timezone.utc),
                    datetime(2025, 12, 31, tzinfo=timezone.utc),
                ]
            ]
        ),
    ),
    license="CC-BY-4.0",
)

# 2. Build STAC Items for each COG using rio-stac
cog_paths = glob.glob("gmw_hab_v30_tiles/*.tif")

for img_path in tqdm.tqdm(cog_paths):
    img_name = rsgislib.tools.filetools.get_file_basename(img_path)
    http_url = f"{BASE_URL}/{img_name}.tif"
    vsi_url = f"/vsicurl/{http_url}"

    item = create_stac_item(
        source=vsi_url,
        id=img_name,
        asset_name="gmw_habitat_mask",
        asset_roles=["data", "mask"],
        asset_media_type=pystac.MediaType.COG,
        with_proj=True,
        with_raster=True,
    )
    
    # Overwrite the asset href from /vsicurl/ to the public HTTPS URL
    item.assets["gmw_habitat_mask"].href = http_url
    collection.add_item(item)

# 3. Write static catalog to disk or cloud bucket
catalog = pystac.Catalog(
    id="gmw-catalog", description="Remote STAC Catalog for Global Mangrove Watch"
)
catalog.add_child(collection)



# Set root destination to a local directory for upload
output_dir = "./gmw_stac_catalog"
catalog.normalize_hrefs(STAC_URL)  # Root URL if hosted together
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED, dest_href=output_dir)

print(f"STAC catalog written to {output_dir}")

