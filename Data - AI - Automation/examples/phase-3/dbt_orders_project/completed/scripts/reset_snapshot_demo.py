from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
shutil.copy2(root / "seeds_baseline" / "customers_2025.csv", root / "seeds" / "customers_2025.csv")
print("customers_2025.csv reset to deterministic baseline")
