"""Rank candidate farm sites by solar potential.

Illustrative sample: all data below is synthetic. It shows the shape of the
analysis (feature engineering -> random forest -> Seaborn comparison), not
real measurements.
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

rng = np.random.default_rng(7)

# 1. Synthetic training grid: geological + meteorological features per cell.
n = 600
cells = pd.DataFrame({
    "irradiance": rng.normal(5.6, 0.5, n),         # kWh/m2/day
    "cloud_cover": rng.uniform(10, 70, n),         # %
    "temperature": rng.normal(27, 3, n),           # deg C
    "rainfall": rng.uniform(300, 1200, n),         # mm/yr
    "slope": rng.gamma(2.0, 2.5, n),               # degrees
    "elevation": rng.normal(900, 120, n),          # m
})
cells["potential"] = (
    cells.irradiance * 0.92
    - cells.cloud_cover * 0.012
    - np.abs(cells.temperature - 25) * 0.015
    - cells.slope * 0.04
    + rng.normal(0, 0.08, n)
)

X, y = cells.drop(columns="potential"), cells["potential"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=7)

# 2. Random forest on the training grid.
model = RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=7)
model.fit(X_tr, y_tr)
print(f"held-out R^2: {r2_score(y_te, model.predict(X_te)):.2f}")

# 3. Score 15 candidate sites and rank them.
sites = X.sample(15, random_state=3).reset_index(drop=True)
sites.insert(0, "site", [f"Site {i:02d}" for i in range(1, 16)])
sites["predicted"] = model.predict(sites.drop(columns="site"))
sites = sites.sort_values("predicted", ascending=False)

importance = (
    pd.Series(model.feature_importances_, index=X.columns)
    .sort_values(ascending=False)
)

# 4. Plot: ranked sites + what drives the ranking.
INK, MUTED, BG, ACCENT = "#f3f5f8", "#7c8490", "#08090c", "#5b8def"
sns.set_theme(style="white", rc={
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "figure.facecolor": BG, "axes.facecolor": BG, "axes.edgecolor": BG,
    "text.color": INK, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": INK,
})

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(8, 5), gridspec_kw={"width_ratios": [1.7, 1], "wspace": 0.55}
)

shade = sns.blend_palette([ACCENT, "#2b3f6b"], n_colors=len(sites))
sns.barplot(data=sites, y="site", x="predicted", hue="site", palette=shade,
            legend=False, ax=ax1, width=0.72, linewidth=0)
ax1.set_xlim(0, sites.predicted.max() * 1.05)   # bars start at zero
ax1.set(xlabel="Predicted solar potential (relative)", ylabel="")
ax1.set_title("Candidate sites, ranked", loc="left", fontsize=11,
              fontweight="bold", color=INK, pad=10)

sns.barplot(x=importance.values, y=importance.index, color=ACCENT, ax=ax2, width=0.55, linewidth=0)
ax2.set(xlabel="Share of model decision", ylabel="")
ax2.set_title("What drives it", loc="left", fontsize=11,
              fontweight="bold", color=INK, pad=10)

for ax in (ax1, ax2):
    sns.despine(ax=ax, left=True, bottom=True)
    ax.tick_params(length=0, labelsize=8)
    ax.xaxis.grid(True, color="#ffffff", alpha=0.06)
    ax.set_axisbelow(True)
    ax.xaxis.label.set_size(8)

fig.text(0.04, 0.02, "Illustrative sample with synthetic data", fontsize=7, color=MUTED)
fig.savefig("solar_site_ranking.png", dpi=200, bbox_inches="tight",
            facecolor=BG, pad_inches=0.3)
