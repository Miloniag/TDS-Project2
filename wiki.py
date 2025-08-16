import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from .plotting import scatter_with_regression

HEADERS = {"User-Agent": "tds-analyst-agent/1.0"}

# Robust wiki table scraping + Q/A for the highest-grossing films page

def answer_highest_grossing_films(url: str) -> Dict[str, Any]:
    html = requests.get(url, headers=HEADERS, timeout=30).text
    soup = BeautifulSoup(html, 'html.parser')
    tables = pd.read_html(html)

    # Try to locate the main table with a "Rank" column
    main = None
    for t in tables:
        cols = [c.lower() for c in t.columns]
        if any('rank' in str(c).lower() for c in t.columns) and any('title' in str(c).lower() for c in t.columns):
            main = t
            break
    if main is None:
        # fallback: first table
        main = tables[0]

    # Normalize columns
    main.columns = [str(c).strip() for c in main.columns]

    # Q1: How many $2 bn movies released before 2000?
    # Find release year column heuristically
    year_col = None
    for c in main.columns:
        cl = c.lower()
        if 'year' in cl or 'release' in cl:
            year_col = c
            break
    if year_col is None:
        # try parsing from Title column if includes year in parentheses
        def infer_year(x):
            import re
            m = re.search(r'(19|20)\d{2}', str(x))
            return int(m.group()) if m else None
        main['__year'] = main.iloc[:, 1].map(infer_year) if main.shape[1] > 1 else main.iloc[:, 0].map(infer_year)
        year_col = '__year'

    # revenue column detection (US$ billions or similar)
    rev_col = None
    for c in main.columns:
        if 'gross' in c.lower() or 'revenue' in c.lower() or 'box office' in c.lower():
            rev_col = c
            break

    def to_billions(val):
        s = str(val)
        s = s.replace(',', '')
        if '$' in s and 'billion' in s.lower():
            import re
            m = re.search(r'(\d+\.?\d*)', s)
            return float(m.group(1)) if m else None
        # if number looks like absolute USD
        try:
            x = float(s)
            return x / 1e9 if x > 1e6 else x
        except Exception:
            return None

    if rev_col is not None:
        main['__rev_b'] = main[rev_col].map(to_billions)
    else:
        main['__rev_b'] = None

    main['__year'] = pd.to_numeric(main[year_col], errors='coerce')

    q1 = int(((main['__rev_b'] >= 2.0) & (main['__year'] < 2000)).fillna(False).sum())

    # Q2: earliest film grossing over $1.5bn
    idx = (main['__rev_b'] >= 1.5)
    earliest_title = None
    if idx.any():
        sub = main[idx].sort_values('__year', ascending=True)
        # pick title-like column
        title_col = None
        for c in main.columns:
            if 'title' in c.lower() or 'film' in c.lower():
                title_col = c; break
        if title_col is None:
            title_col = main.columns[0]
        earliest_title = str(sub.iloc[0][title_col]) if not sub.empty else None

    # Q3/4: correlation + plot using Rank vs Peak (if available)
    # locate rank & peak columns
    rank_col = next((c for c in main.columns if 'rank' in c.lower()), None)
    peak_col = next((c for c in main.columns if 'peak' in c.lower()), None)
    corr = None
    plot_uri = None
    if rank_col and peak_col:
        sr = pd.to_numeric(main[rank_col], errors='coerce')
        sp = pd.to_numeric(main[peak_col], errors='coerce')
        df = pd.DataFrame({"Rank": sr, "Peak": sp}).dropna()
        if len(df) >= 2:
            corr = float(df["Rank"].corr(df["Peak"]))
            plot_uri = scatter_with_regression(df["Rank"], df["Peak"], "Rank", "Peak", "Rank vs Peak")

    return {
        "two_billion_before_2000": q1,
        "earliest_over_1_5b": earliest_title,
        "rank_peak_corr": corr,
        "rank_peak_plot": plot_uri,
    }
