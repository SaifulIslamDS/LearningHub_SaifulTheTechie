"""Shared chart style for the Phase 2 scripts (a colour-blind-checked palette and quiet axes).

    from chart_style import PALETTE, apply_style, save
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")            # draw to files (works without a screen); remove to show windows
import matplotlib.pyplot as plt  # noqa: E402

# Categorical colours, always used in this order (validated for colour-vision deficiency)
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
BLUE_RAMP = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]   # light -> dark, for magnitude
INK, INK_2, MUTED, SURFACE = "#0b0b0b", "#52514e", "#898781", "#fcfcfb"
CHARTS = Path(__file__).parent / "charts"


def apply_style():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": MUTED, "axes.labelcolor": INK_2, "xtick.color": INK_2, "ytick.color": INK_2,
        "text.color": INK, "axes.titlecolor": INK, "axes.titleweight": "bold", "axes.titlesize": 13,
        "axes.titlelocation": "left", "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": 0.8, "axes.axisbelow": True,
        "axes.prop_cycle": plt.cycler(color=PALETTE), "lines.linewidth": 2, "font.size": 11,
        "legend.frameon": False, "figure.dpi": 110,
    })


def save(fig, name: str):
    CHARTS.mkdir(exist_ok=True)
    path = CHARTS / name
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"saved charts/{name}")
