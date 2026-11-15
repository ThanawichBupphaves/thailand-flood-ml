"""
Project settings in one place.

Every notebook starts with `from config import *`, so a path or a date
only has to be changed here. If you clone this repo on another machine,
the only line you should need to edit is DATA_DIR.
"""
from pathlib import Path
import os

# ---------------------------------------------------------------------------
# Where things live
# ---------------------------------------------------------------------------
REPO_DIR = Path(__file__).resolve().parent

# Big raw data (GBs) lives OUTSIDE the repo, on the 50 GB work disk.
# Override with an environment variable if you run this somewhere else:
#   export FLOOD_DATA_DIR=/path/to/flood_data
DATA_DIR = Path(os.environ.get("FLOOD_DATA_DIR",
                               "/data9/CLMT5120/work/tb3203/flood_data"))

RAW_GISTDA = DATA_DIR / "gistda_shp"        # 376 flood-map shapefiles
RAW_CHIRPS = DATA_DIR / "chirps_th"         # daily CHIRPS GeoTIFFs
RAW_HYDRO = DATA_DIR / "hydrosheds"         # HydroRIVERS + HydroBASINS
RAW_DEM = DATA_DIR / "dem"                  # Copernicus DEM tiles / mosaic
RAW_JRC = DATA_DIR / "jrc_gsw"              # JRC Global Surface Water
INTERIM = DATA_DIR / "interim"              # gridded arrays, stacks (.npy, .nc)

# Small files that ARE committed to git, so anyone can rerun the modelling
# notebooks without downloading the raw data.
SMALL_DIR = REPO_DIR / "data_small"
RESULTS_DIR = REPO_DIR / "results"          # tables (CSV) used in the paper
FIG_DIR = REPO_DIR / "figures"              # figures (PNG) used in the paper

# ---------------------------------------------------------------------------
# Study design (matches the approved proposal)
# ---------------------------------------------------------------------------
YEARS = [2024, 2025, 2026]
FLOOD_WINDOW = ("08-04", "10-21")           # 4 Aug to 21 Oct each year
RAIN_WINDOW = ("05-01", "09-30")            # CHIRPS season used for features

GRID_RES_DEG = 0.05                          # CHIRPS grid, ~5.5 km
FINE_FACTOR = 10                             # 10 x 10 fine cells per square (~550 m)
MIN_PASSES_FLOODED = 2                       # fine cell flooded if >= 2 passes saw water
MIN_COVER_PASSES = 5                         # keep squares seen >= 5 times every season

RANDOM_STATE = 42                            # one seed for everything

GISTDA_SNAPSHOT = "2026-11-14"               # data freeze date (notebook 01)

for _d in (SMALL_DIR, RESULTS_DIR, FIG_DIR):
    _d.mkdir(exist_ok=True)
