import duckdb
import pandas as pd
from typing import Dict, Any
from .plotting import scatter_with_regression

# Counts & delay slope on the Indian High Court judgement dataset via DuckDB (S3 public bucket)

def analyze_courts(bucket_prefix: str = 's3://indian-high-court-judgments', court="33_10") -> Dict[str, Any]:
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs; INSTALL parquet; LOAD parquet;")
    meta_path = f"{bucket_prefix}/metadata/parquet/year=*/court=*/bench=*/metadata.parquet?s3_region=ap-south-1"

    total = con.execute(f"SELECT COUNT(*)
