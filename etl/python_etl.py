import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ------------------ 1. Load dataset ------------------
csv_path = "layoffs.csv"
df = pd.read_csv(csv_path)

n_rows = len(df)

# ------------------ 2. Transform-like steps ------------------
df['date'] = pd.to_datetime(df['date'])
df['date_key'] = df['date'].dt.strftime('%Y%m%d').astype(int)

# Location split: keep as-is for demo
df['location_clean'] = df['location'].fillna(df['country'])

# Funds raised clean
df['funds_raised'] = (
    df['funds_raised'].astype(str)
        .str.replace(r'[\$,]', '', regex=True)
        .str.replace('None', '')
        .replace('', pd.NA)
        .astype(float)
)

# perc_laid_off clean
df['perc_laid_off_num'] = (
    df['percentage_laid_off'].astype(str)
        .str.replace('%', '')
        .replace('None', pd.NA)
        .astype(float)
)

# -------------- 3. Dimension counts ----------------
cnt_date = df['date_key'].nunique()
cnt_company = df['company'].nunique()
cnt_location = df['location_clean'].nunique()
cnt_fact = n_rows

# -------------- 4. Sankey diagram ------------------
labels = [
    "layoffs.csv",            # 0
    "Transform ETL",          # 1
    "dim_date",               # 2
    "dim_company",            # 3
    "dim_location",           # 4
    "fact_layoffs"            # 5
]

# Define flows (source_idx, target_idx, value)
sources = [0, 1, 1, 1, 1]
targets = [1, 2, 3, 4, 5]
values  = [n_rows, cnt_date, cnt_company, cnt_location, cnt_fact]

sankey_fig = go.Figure(go.Sankey(
    node=dict(label=labels, pad=20, thickness=20),
    link=dict(source=sources, target=targets, value=values)
))
sankey_fig.update_layout(title_text="ETL Flow: From CSV to Star Schema", height=500)

# -------------- 5. Bar chart of dimension sizes ----
bar_fig = px.bar(
    x=["dim_date", "dim_company", "dim_location", "fact_layoffs"],
    y=[cnt_date, cnt_company, cnt_location, cnt_fact],
    log_y=True,
    labels={'x':'Table', 'y':'Row count (log)'},
    text=[cnt_date, cnt_company, cnt_location, cnt_fact],
    title="Ukuran Tabel Hasil ETL (log scale)"
)
bar_fig.update_traces(textposition='outside')

# -------------- 6. Combine into single HTML ---------
subfig = make_subplots(
    rows=2, cols=1,
    specs=[[{"type":"domain"}],
           [{"type":"xy"}]],
    subplot_titles=("Sankey ETL Flow", "Row Count per Table")
)
for t in sankey_fig.data:
    subfig.add_trace(t, row=1, col=1)
for t in bar_fig.data:
    subfig.add_trace(t, row=2, col=1)

subfig.update_layout(height=800, showlegend=False,
                     title_text="Visualisasi Desain & ETL Star‑Schema Layoffs")

html_out = "etl_star_schema_visual.html"
subfig.write_html(html_out, include_plotlyjs="cdn")
html_out
