
import os, glob
import numpy as np, pandas as pd
import geopandas as gpd, rioxarray as rxr, shapely
import rasterio.features
from affine import Affine
from shapely import make_valid
import warnings; warnings.filterwarnings("ignore")

F = 10
ref = rxr.open_rasterio(sorted(glob.glob("data/chirps_th/*.tif"))[0]).squeeze()
H, W = ref.shape
fine_t = ref.rio.transform() * Affine.scale(1.0 / F, 1.0 / F)
shape = (H * F, W * F)

df = pd.read_csv("gistda_scenes.csv", parse_dates=["date"])
df = df[(df["category"] == "pass") & df["zip_url"].notna()]
md = df["date"].dt.strftime("%m-%d")
df = df[(md >= "08-04") & (md <= "10-21")]

log = []
for year, grp in df.groupby("year"):
    flood = np.zeros(shape, dtype=np.uint8)
    hull = np.zeros(shape, dtype=np.uint8)
    for i, row in enumerate(grp.itertuples(), 1):
        shp = glob.glob(f"data/gistda_shp/{row.scene}/*.shp")
        if not shp:
            continue
        try:
            g = gpd.read_file(shp[0], columns=[], encoding="cp874")
            if g.crs is not None and g.crs.to_epsg() != 4326:
                g = g.to_crs(4326)
            geoms = [make_valid(x) for x in g.geometry if x is not None and not x.is_empty]
            if not geoms:
                continue
            m = rasterio.features.rasterize([(x, 1) for x in geoms], out_shape=shape,
                                            transform=fine_t, fill=0, dtype="uint8")
            h = shapely.GeometryCollection(geoms).convex_hull
            mh = rasterio.features.rasterize([(h, 1)], out_shape=shape,
                                             transform=fine_t, fill=0, dtype="uint8")
            flood += m
            hull += mh
            log.append(dict(year=int(year), scene=row.scene, date=row.date, sat=row.sat,
                            fine_cells=int(m.sum()), hull_cells=int(mh.sum())))
            print(int(year), i, "of", len(grp), row.scene, int(m.sum()), int(mh.sum()), flush=True)
        except Exception as e:
            print("FAIL", row.scene, type(e).__name__, str(e)[:80], flush=True)
    np.save(f"data/win_flood_count_{int(year)}.npy", flood)
    np.save(f"data/win_hull_count_{int(year)}.npy", hull)
    print("SAVED year", int(year), flush=True)
pd.DataFrame(log).to_csv("window_passes.csv", index=False)
print("DONE", flush=True)
