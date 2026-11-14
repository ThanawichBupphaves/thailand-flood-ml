
import os, glob
import numpy as np, pandas as pd
import geopandas as gpd, rioxarray as rxr
import rasterio.features
from affine import Affine
from shapely import make_valid
import warnings; warnings.filterwarnings("ignore")

F = 10   # each 5 km rainfall cell is split into 10 x 10 fine cells (about 550 m)
ref = rxr.open_rasterio(sorted(glob.glob("data/chirps_th/*.tif"))[0]).squeeze()
H, W = ref.shape
fine_t = ref.rio.transform() * Affine.scale(1.0 / F, 1.0 / F)
shape = (H * F, W * F)
print("fine grid:", shape, flush=True)

df = pd.read_csv("gistda_scenes.csv")
df = df[(df["category"] == "pass") & df["zip_url"].notna()]

for year, grp in df.groupby("year"):
    count = np.zeros(shape, dtype=np.uint8)
    for i, row in enumerate(grp.itertuples(), 1):
        shp = glob.glob(f"data/gistda_shp/{row.scene}/*.shp")
        if not shp:
            print("no shp", row.scene, flush=True)
            continue
        try:
            g = gpd.read_file(shp[0], columns=[], encoding="cp874")
            if g.crs is not None and g.crs.to_epsg() != 4326:
                g = g.to_crs(4326)
            geoms = [make_valid(x) for x in g.geometry if x is not None and not x.is_empty]
            m = rasterio.features.rasterize([(x, 1) for x in geoms], out_shape=shape,
                                            transform=fine_t, fill=0, dtype="uint8")
            count += m
            print(int(year), i, "of", len(grp), row.scene, int(m.sum()), "fine cells", flush=True)
        except Exception as e:
            print("FAIL", row.scene, type(e).__name__, str(e)[:80], flush=True)
    np.save(f"data/flood_count_{int(year)}.npy", count)
    print("SAVED year", int(year), flush=True)
print("DONE", flush=True)
