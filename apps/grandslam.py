#import packages to create app
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import numpy as np

grandslam = pd.read_csv('grandslam.csv')
tournament_names = grandslam['tournament'].unique()
cols = list(grandslam.columns)
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
    html.H1('Grand Slam Series Data from 2017 to 2021',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        Top Ranked Players of 2021 Performance in the Grand Slam 
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),     
    html.Div([
        html.Div([
            html.Label('Select Tournament'),
            dcc.Dropdown(id='tournament_dropdown',
                        options=[{'label': i, 'value': i}
                                for i in tournament_names],
                        value=tournament_names,
                        multi=True
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        
        ]),
        html.Div([
            dcc.Graph(
                id='gs_barfig'
            ),
            ],style={'width': '80%', 'margin-left': '10%','display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Graph(
                        id='gs_linefig'
                ),
            ],style={'width': '49%','display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                        id='gs_fig'
                ),
            ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
            ]),
    ])   

@app.callback(
    [Output(component_id='gs_barfig', component_property='figure'),
    Output(component_id='gs_linefig', component_property='figure'),
    Output(component_id='gs_fig', component_property='figure')],
    [Input(component_id='tournament_dropdown', component_property='value'),]
)

def update_graphs(selected_count):
    if not (selected_count):
        return dash.no_update
    data =[]
    for j in selected_count:
            data.append(grandslam[grandslam['tournament'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    
    gs_barfig = px.bar(df, x='winner', 
                       color='tournament',
                       hover_data=['loser','round', 'wrank', 'year'],
                       hover_name="winner", animation_frame = 'year',
                       labels={ 'wrank':'ATP Rank', 'loser': 'Loser',
                               'tournament': 'Tournament',
                               'winner':'Winner', 'year': 'Year', 'round': 'Round'})

    gs_barfig.update_yaxes(title='Total Number of Matches')


    #gs_linefig = px.line(df, x="winner", y="round",
                          #hover_data={'wrank', 'loser', 'year'},
                         # color='tournament', 
                          #hover_name="winner", 
                          #labels={'wrank':'ATP Rank','round': 'Round',
                                  #'tournament': 'Tournament', 'loser': 'Loser',
                                 # 'winner':'Winner',  
                                  #'year': 'Year'})

    gs_linefig = px.line(df, x="year", y="round",
                          hover_data={'wrank', 'loser', 'year'},
                         color='tournament', 
                          hover_name="winner", 
                          labels={'wrank':'ATP Rank','round': 'Round',
                                  'tournament': 'Tournament', 'loser': 'Loser',
                                 'winner':'Winner',  
                                  'year': 'Year'})

    gs_fig = px.scatter(df, x="s4win(%)", y="s4win",  
                        hover_data={'winner', 'round', 'loser', 'year', 'tournament'},
                        color='winner', symbol = 'winner',
                        hover_name="winner", 
                        labels={'s4win(%)': 'Set 4 Win Percentage', 
                                's4win': 'Set 4 Win Counts','tournament': 'Tournament',
                                'winner':'Winner', 'round': 'Round', 
                                'loser': 'Loser', 'year': 'Year'})

    gs_fig.update_traces(marker_size=12)


    return [gs_barfig, gs_linefig, gs_fig]


# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8079,debug=True)
