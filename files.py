from typing import Dict, Tuple
import pandas as pd
from io import BytesIO

# Load the first tabular attachment if present (csv/xlsx/parquet)

def load_first_table(files: Dict[str, bytes]) -> Tuple[str, pd.DataFrame | None]:
    for name, blob in files.items():
        lower = name.lower()
        bio = BytesIO(blob)
        try:
            if lower.endswith('.csv'):
                return name, pd.read_csv(bio)
            if lower.endswith('.tsv') or lower.endswith('.txt'):
                return name, pd.read_csv(bio, sep='\t')
            if lower.endswith('.parquet'):
                return name, pd.read_parquet(bio)
            if lower.endswith('.xlsx'):
                return name, pd.read_excel(bio)
        except Exception:
            continue
    return "", None
