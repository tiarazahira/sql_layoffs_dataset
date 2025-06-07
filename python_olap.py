import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

csv_path = "layoffs.csv"
df = pd.read_csv(csv_path)

df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['quarter'] = df['date'].dt.to_period('Q').astype(str)
df['total_laid_off'] = df['total_laid_off'].fillna(0)

# Heatmap data
heat_df = df.groupby(['country', 'year'])['total_laid_off'].sum().unstack(fill_value=0)
top_countries = heat_df.sum(axis=1).nlargest(15).index
heat_df = heat_df.loc[top_countries]

heat_fig = go.Figure(
    data=go.Heatmap(
        z=heat_df.values,
        x=[str(c) for c in heat_df.columns],
        y=heat_df.index.tolist(),
        colorscale='Viridis',
        colorbar=dict(title="Total layoffs")
    )
)
heat_fig.update_layout(title="Heat‑map: Total Layoffs by Country × Year")

# 3D scatter
df_2024 = df[df['year'] == 2024]
ind_q = df_2024.groupby(['industry', 'quarter'])['total_laid_off'].sum().reset_index()
top_ind = ind_q.groupby('industry')['total_laid_off'].sum().nlargest(10).index
ind_q = ind_q[ind_q['industry'].isin(top_ind)]

scatter3d_fig = px.scatter_3d(
    ind_q,
    x='industry',
    y='quarter',
    z='total_laid_off',
    color='industry',
    size='total_laid_off',
    size_max=28
)
scatter3d_fig.update_layout(title="3D Scatter: Layoffs per Industry & Quarter (2024)")

# Rolling 12 month AI
ai_df = df[df['industry'] == 'AI']
monthly_ai = ai_df.groupby(ai_df['date'].dt.to_period('M'))['total_laid_off'].sum().sort_index()
rolling12 = monthly_ai.rolling(12).sum().dropna()
rolling12.index = rolling12.index.to_timestamp()

line_fig = px.line(
    rolling12,
    labels={'value':'Total layoffs (12‑month rolling sum)', 'index':'Date'}
)
line_fig.update_layout(title="Rolling 12‑Month Layoffs in AI Industry")

# Combine into single HTML
subfig = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "heatmap", "colspan": 2}, None],
           [{"type": "scatter3d"}, {"type": "xy"}]],
    subplot_titles=("Heat‑map Country×Year",
                    "3D Industry×Quarter (2024)",
                    "Rolling 12‑Month AI")
)

subfig.add_trace(heat_fig.data[0], row=1, col=1)
for trace in scatter3d_fig.data:
    subfig.add_trace(trace, row=2, col=1)
for trace in line_fig.data:
    subfig.add_trace(trace, row=2, col=2)

subfig.update_layout(height=900, showlegend=False,
                     title_text="Visualisasi Kubus PHK Teknologi")

html_path = "layoffs_cube_visual.html"
subfig.write_html(html_path, include_plotlyjs="cdn")

html_path
