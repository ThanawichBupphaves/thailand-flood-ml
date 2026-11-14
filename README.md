# Can rainfall, terrain and rivers explain unusual flooding in Thailand?

**Thanawich (Ice) Bupphaves** · CLMT 5120 Machine Learning and AI for Climate Science and Solutions · Columbia University · Fall 2026

Flooding in Thailand repeats in the same places almost every year. This project asks a harder question than "where does it flood?":
**how much more or less does each 5 km square flood than its usual pattern in a given rainy season, and can rainfall, terrain and river information explain that difference in a season or region the model has never seen?**

> Status: in progress. Results and figures will be filled in by 21 December 2026.

---

## Key results (to be filled in)

| Held-out test | Best baseline (RMSE) | Best model (RMSE) | Skill vs baseline |
|---|---|---|---|
| Season 2024 | | | |
| Season 2025 | | | |
| Season 2026 | | | |
| Held-out regions | | | |

One-paragraph takeaway: _to be written._

---

## Data

| Data | Source | Used for | Size |
|---|---|---|---|
| Flood extent maps (376 radar passes, Jul 2024 to Oct 2026) | [GISTDA disaster portal](https://disaster.gistda.or.th/) | The label (flooded fraction) | ~ GB |
| Daily rainfall, CHIRPS v3 (0.05°) | [Climate Hazards Center, UCSB](https://data.chc.ucsb.edu/products/CHIRPS/v3.0/) | Rainfall features | ~ GB |
| Elevation, Copernicus DEM 30 m | Microsoft Planetary Computer | Terrain features | |
| Permanent water, JRC Global Surface Water | Microsoft Planetary Computer | Removing rivers and lakes from the label | |
| Rivers and basins, HydroRIVERS / HydroBASINS | [HydroSHEDS](https://www.hydrosheds.org/) | Distance to river, upstream rain, region groups | ~ 1 GB |

Data snapshot date: _to be filled in when the data are frozen._

---

## How to reproduce

There are two ways to run this work.

**A. Quick (about 5 minutes):** start from the small model table that is committed in `data_small/`, and run notebooks 04 to 06. No large downloads.

**B. Full (several hours):** re-download all raw data and rebuild everything from notebook 01.

### 1. Get the code and set up the environment

```bash
git clone https://github.com/<your-username>/thailand-flood-ml.git
cd thailand-flood-ml
python3.11 -m venv ~/flood-env
source ~/flood-env/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name flood-env --display-name "Python (flood)"
```

### 2. Tell the code where the big data should go (full run only)

Raw data is several GB and is not stored in this repo. By default it goes to `/data9/G5120/work/tb3203/flood_data`. To use another folder:

```bash
export FLOOD_DATA_DIR=/path/to/flood_data
```

### 3. Run the notebooks in order

| Notebook | What it does | Run time | Needs raw data? |
|---|---|---|---|
| `00_setup_check.ipynb` | Checks packages, folders and disk space | < 1 min | No |
| `01_download_data.ipynb` | Downloads GISTDA, CHIRPS, HydroSHEDS, DEM, JRC | hours | Yes |
| `02_build_labels.ipynb` | Turns flood maps into the flooded fraction per 5 km square and season | | Yes |
| `03_build_features.ipynb` | Builds the model table: one row per square and season | | Yes |
| `04_baselines_and_validation.ipynb` | Baselines under season and region hold-out; leakage demo | | No |
| `05_models.ipynb` | Ridge and random forest with tuning inside the training folds | | No |
| `06_uncertainty_and_interpretation.ipynb` | Uncertainty, permutation importance, error maps, failure cases | | No |
| `07_extensions.ipynb` (optional) | Gradient boosting (quantile, monotonic), two-step model | | No |

Figures in the paper are saved to `figures/` and tables to `results/`.

---

## Repository layout

```
thailand-flood-ml/
├── README.md              you are here
├── requirements.txt       packages needed
├── config.py              all paths and settings in one place
├── src/flood_utils.py     small shared helpers (scores, plots)
├── notebooks/             00 to 07, run in order
├── scripts/               long download jobs that can run in the background
├── data_small/            small committed files (model table, dated file lists)
├── results/               CSV tables used in the paper
├── figures/               PNG figures used in the paper
└── paper/                 final paper (PDF)
```

---

## Method in one picture (to be filled in)

_Flowchart: flood maps → flooded fraction label · rainfall, terrain, rivers → features · baselines and models · season and region hold-out._

---

## Limitations

To be completed. The main ones known so far:
- Only three seasons of flood maps exist (the GISTDA archive starts in July 2024).
- Each map covers one satellite strip, so an area with no flooding on the map may be dry **or simply unobserved**.
- Maps show flood extent, not depth. Drainage, canals, pumping and reservoir releases are not modelled.
- **A low prediction must not be read as "safe".** It may only mean the area was rarely observed.

---

## Acknowledgements and citation

Flood maps: Geo-Informatics and Space Technology Development Agency (GISTDA), Thailand. Rainfall: Funk et al., CHIRPS. Rivers and basins: Lehner & Grill (2013), HydroSHEDS. Elevation: Copernicus DEM. Surface water: Pekel et al. (2016), JRC Global Surface Water.

Course: CLMT 5120, Prof. Daniel Westervelt, Columbia University.
