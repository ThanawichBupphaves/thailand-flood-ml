
import os, time, datetime as dt, requests
import rioxarray as rxr
from concurrent.futures import ThreadPoolExecutor

YEARS = [2024, 2025, 2026]
START_MD, END_MD = (5, 1), (9, 30)
BOX = dict(minx=97.3, miny=5.6, maxx=105.7, maxy=20.5)   # Thailand
OUT, TMP = "data/chirps_th", "data/tmp_chirps"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)

def all_days():
    for y in YEARS:
        d, end = dt.date(y, *START_MD), dt.date(y, *END_MD)
        while d <= end:
            yield d
            d += dt.timedelta(days=1)

def pull(d):
    tag = d.strftime("%Y.%m.%d")
    out = f"{OUT}/chirps_th_{tag}.tif"
    if os.path.exists(out):
        return "skip"
    url = f"https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/sat/{d.year}/chirps-v3.0.sat.{tag}.tif"
    tmp = f"{TMP}/{tag}.tif"
    err = "unknown"
    for attempt in range(3):
        try:
            with requests.get(url, timeout=120, stream=True) as r:
                if r.status_code != 200:
                    return f"HTTP {r.status_code}"
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
            da = rxr.open_rasterio(tmp, masked=True).squeeze()
            da = da.where(da >= 0)
            da.rio.clip_box(**BOX).rio.to_raster(out)
            da.close()
            os.remove(tmp)
            return "ok"
        except Exception as e:
            err = type(e).__name__
            if os.path.exists(tmp):
                os.remove(tmp)
            time.sleep(5)
    return "FAIL " + err

if __name__ == "__main__":
    days = list(all_days())
    counts = {}
    with ThreadPoolExecutor(4) as ex:
        for i, res in enumerate(ex.map(pull, days), 1):
            counts[res] = counts.get(res, 0) + 1
            if i % 20 == 0 or i == len(days):
                print(i, "of", len(days), counts, flush=True)
    print("DONE", counts, flush=True)
