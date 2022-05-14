#import packages to create app
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import numpy as np

top10 = pd.read_csv('top10.csv')
player_names = top10['winner'].unique()
cols = list(top10.columns)
#needed only if running this as a single page app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#e9eef5',
    'text': '#1c1cbd'
}
# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Top 10 ATP Ranked Players Data',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        Players Ranking Movement from 2017 to 2021 
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),     
    html.Div([
        html.Div([
            html.Label('Select Player'),
            dcc.Dropdown(id='player_dropdown',
                        options=[{'label': i, 'value': i}
                                for i in player_names],
                        value=player_names,
                        multi=True
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Select Number of Matches Won'),
                dcc.RangeSlider(id='win_range',
                    min=1,
                    max=226,
                    value=[1,226],
                    step= 1,
                    marks={
                        1: '1win',
                        68: '60wins',
                        120: '120wins',
                        180: '180wins',
                        226: '240wins'
                    },
                              ),
            ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
        ]),
        html.Div([
            dcc.Graph(
                id='linefig'
            ),
            ],style={'width': '80%', 'margin-left': '10%','display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Graph(
                        id='barfig'
                ),
            ],style={'width': '49%','display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='dotfig'
                ),
            ],style={'width': '49%', 'display': 'inline-block'}),
            ]),
    ])   

@app.callback(
    [Output(component_id='linefig', component_property='figure'),
    Output(component_id='barfig', component_property='figure'),
    Output(component_id='dotfig', component_property='figure')],
    [Input(component_id='player_dropdown', component_property='value'),
    Input(component_id='win_range', component_property='value')]
)

def update_graph(selected_count,erangevalue):
    if not (selected_count or erangevalue):
        return dash.no_update
    d = top10[(top10['win_counts'] >= erangevalue[0]) & (top10['win_counts'] <= erangevalue[1])]
    data =[]
    for j in selected_count:
            data.append(d[d['winner'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    linefig = px.line(df, x="date", y='wrank',
              hover_data={'wpts','tournament', 'series'},
              color='winner', 
              hover_name="winner", 
              title="Top 10 ATP Ranked Players of 2021",
              labels={'wrank':'ATP Rank','wpts': 'ATP Points',
                    'tournament': 'Tournament', 'series':'Series',
                    'winner':'Winner', 'surface': 'Surface', 'date': 'Date'})

    linefig.update_yaxes(range=[10, 0])
    linefig.update_xaxes(
        dtick="M4",
        tickformat="%b-""%y",
        ticklabelmode="period")

    dotfig = px.scatter(df, x="s1win(%)", y="s1win", facet_col = 'best_of', 
                        hover_data={'tournament', 'loser', 'year'},
                        color='winner', title='Percentage of Match Winners Winning Sets 1 & 4',
                        hover_name="winner", 
                        labels={'s1win(%)': 'Set1 Win (%)', 
                                's1win': 'Set 1 Win Counts',
                                'tournament': 'Tournament', 'best_of': 'Best of',
                                'winner':'Winner', 'round': 'Round', 
                                'loser': 'Loser', 'year': 'Year'})
    
    dotfig.update_traces(marker_size=10)

    barfig = px.bar(df, y="wpts", x='round',
                    color='winner', hover_name="winner",
                    title = 'ATP Points vs Rounds',
                    hover_data=['year','tournament', 'surface', 'series'],
                    labels={'wpts': 'ATP Points', 'round': 'Round',
                            'tournament': 'Tournament', 'series':'Series',
                            'winner':'Winner', 'surface': 'Surface', 'year': 'Year'})


    return [linefig, dotfig, barfig]