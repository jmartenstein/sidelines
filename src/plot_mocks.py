import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from mock_draft_data import get_draft_dataframe, MOCK_REGISTRY, DEFAULT_ORDER
from utils import get_team_colors_map

def create_draft_heatmap():
    # 1. Prepare Data
    df = get_draft_dataframe()
    colors_map = get_team_colors_map()
    df = df.sort_values(by="date", ascending=False)
    
    # Calculate median pick for each player to sort X-axis
    player_medians = df.groupby('player')['pick'].median().sort_values()
    x_order = player_medians.index.tolist()

    # Aggregation
    df['consensus_count'] = df.groupby(['pick', 'team', 'player'])['player'].transform('count')
    df['expert_info'] = df.apply(lambda x: f"{x['author']} ({x['date']}){' - TRADE' if x['is_trade'] else ''}", axis=1)
    
    df_agg = df.groupby(['pick', 'team', 'player', 'position', 'is_trade', 'default_team', 'consensus_count']).agg({
        'expert_info': lambda x: "<br>• " + "<br>• ".join(dict.fromkeys(x))
    }).reset_index()

    df_agg['pick_label'] = df_agg['pick'].apply(lambda x: f"Pick #{x}")
    
    def get_team_color(team):
        return colors_map.get(team, {}).get("primary", "#555555")

    # 2. Create Visualization
    fig = go.Figure()

    # Plot all draft slots
    # We group by team just for organizational purposes in the hover/data
    for team in df_agg['team'].unique():
        team_df = df_agg[df_agg['team'] == team]
        
        for _, row in team_df.iterrows():
            border_width = 4 if row['consensus_count'] >= 7 else 1.5
            team_color = get_team_color(row['team'])
            
            line_style = dict(width=border_width, color="white") # High contrast border
            if row['is_trade']:
                line_style['dash'] = 'dot'

            fig.add_trace(go.Scatter(
                x=[row['player']],
                y=[row['pick_label']],
                mode='markers+text',
                name=team,
                marker=dict(
                    size=row['consensus_count'] * 6 + 25, 
                    color=team_color, # Fill color is Team Color
                    symbol='square',
                    line=line_style
                ),
                text=row['consensus_count'],
                textposition="middle center",
                textfont=dict(color='white', size=11, family="Arial Black"),
                customdata=[[row['consensus_count'], row['expert_info'], row['position'], row['team'], row['is_trade'], row['default_team']]],
                hovertemplate=(
                    "<b>%{x} (%{customdata[2]})</b><br>" +
                    "Team: <b>%{customdata[3]}</b>" + (" (TRADE UP)" if row['is_trade'] else "") + "<br>" +
                    "Default Owner: %{customdata[5]}<br>" +
                    "Consensus: %{customdata[0]} Experts<br>" +
                    "<br><b>Recent Expert Projections:</b>%{customdata[1]}<extra></extra>"
                ),
                showlegend=False
            ))

    # 3. Customize Layout
    y_labels = [f"Pick #{i}" for i in range(1, 16)][::-1]

    fig.update_layout(
        title={
            'text': "2026 NFL Mock Draft Board: Team Alignment & Expected Position",
            'y': 0.98, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        margin=dict(t=180, b=350, l=120, r=50),
        xaxis_title="Projected Player (Sorted by Median Pick Position)",
        yaxis_title="Draft Slot",
        yaxis={'categoryorder': 'array', 'categoryarray': y_labels},
        xaxis={'categoryorder': 'array', 'categoryarray': x_order},
        xaxis_tickangle=-45,
        plot_bgcolor='#fbfbfb',
        height=1200, width=1500,
        showlegend=False, # Removed duplicative legend
    )

    fig.update_xaxes(side="top", showgrid=True, gridwidth=1, gridcolor='#eeeeee')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#eeeeee')

    # 4. Sorted List Footer (Multi-Annotation for 2-column effect)
    sorted_registry = sorted(MOCK_REGISTRY.values(), key=lambda x: x['date'], reverse=True)
    mid = (len(sorted_registry) + 1) // 2
    col1, col2 = sorted_registry[:mid], sorted_registry[mid:]

    def format_col(items):
        return "<br>".join([f"• {v['date']} | <b>{v['author']}</b> ({v['source']})" for v in items])

    # Header
    fig.add_annotation(
        text="<b>DATA SOURCES (Sorted by Date)</b>",
        xref="paper", yref="paper",
        x=0.0, y=-0.18, showarrow=False, align="left", font=dict(size=12, color="#222")
    )

    # Column 1
    fig.add_annotation(
        text=format_col(col1),
        xref="paper", yref="paper",
        x=0.0, y=-0.28, showarrow=False, align="left", font=dict(size=11, color="#555")
    )

    # Column 2
    fig.add_annotation(
        text=format_col(col2),
        xref="paper", yref="paper",
        x=0.5, y=-0.28, showarrow=False, align="left", font=dict(size=11, color="#555")
    )

    # Note
    fig.add_annotation(
        text="<i>Note: Dotted borders indicate a projected pick trade. X-Axis is ordered by the median pick slot for each player.</i>",
        xref="paper", yref="paper",
        x=0.5, y=-0.38, showarrow=False, align="center", font=dict(size=10, color="gray")
    )

    return fig

if __name__ == "__main__":
    fig = create_draft_heatmap()
    fig.show()
