"""
Small helper functions shared by the notebooks.

Rule of thumb: if a few lines of code appear in two notebooks, they move
here. Anything that is part of the *story* stays in the notebook so a
reader can follow it.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Scores
# ---------------------------------------------------------------------------
def rmse(truth, pred):
    """Root mean squared error, ignoring NaNs."""
    truth, pred = np.asarray(truth, float), np.asarray(pred, float)
    ok = ~(np.isnan(truth) | np.isnan(pred))
    return float(np.sqrt(np.mean((truth[ok] - pred[ok]) ** 2)))


def skill_vs(truth, pred, baseline_pred):
    """Skill score relative to a baseline: 1 - MSE_model / MSE_baseline.

    1 = perfect, 0 = no better than the baseline, < 0 = worse than it.
    """
    return 1 - rmse(truth, pred) ** 2 / rmse(truth, baseline_pred) ** 2


def mean_bias(truth, pred):
    """Average of (prediction - truth). Negative = model predicts too little flooding."""
    truth, pred = np.asarray(truth, float), np.asarray(pred, float)
    ok = ~(np.isnan(truth) | np.isnan(pred))
    return float(np.mean(pred[ok] - truth[ok]))


def score_table(truth, preds: dict, baseline_key: str):
    """One row per model: RMSE, bias, and skill vs the chosen baseline."""
    rows = []
    for name, p in preds.items():
        rows.append({"model": name,
                     "RMSE": rmse(truth, p),
                     "bias": mean_bias(truth, p),
                     f"skill_vs_{baseline_key}": skill_vs(truth, p, preds[baseline_key])})
    return pd.DataFrame(rows).set_index("model").round(4)


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------
def map_cells(df, col, ax=None, title=None, cmap="viridis", vmin=None, vmax=None, s=4):
    """Quick map of one column of a per-square table (needs 'lon' and 'lat')."""
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 7))
    sc = ax.scatter(df["lon"], df["lat"], c=df[col], s=s, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_aspect("equal")
    ax.set_title(title or col)
    ax.set_xlabel("longitude"); ax.set_ylabel("latitude")
    plt.colorbar(sc, ax=ax, shrink=0.7)
    return ax


def savefig(fig, name, fig_dir):
    """Save a figure as PNG (for the paper) with consistent settings."""
    path = fig_dir / f"{name}.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    print("saved", path)
