#import packages to create app

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import numpy as np

from app import app

tennis = pd.read_csv('tennis.csv')
#get unique series
series = tennis['series'].unique()
loc_data = tennis
cols=list(loc_data.columns)
sur = list(tennis['surface'].unique())

# needed only if running this as a single page app

#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#e9eef5',
    'text': '#1c1cbd'
}
color_discrete_map = {'ATP250': '#636EFA', 'Masters 1000': '#EF553B', 'Grand Slam': '#00CC96',
    'ATP500': '#AB63FA', 'Masters Cup': '#FFA15A'}


# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('ATP Tour Results Data',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        ATP Players Ranking & Points from 2017 to 2021 
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),     
    html.Div([
        html.Div([
            html.Label('Select Series'),
            dcc.Dropdown(id='series_dropdown',
                        options=[{'label': i, 'value': i}
                                for i in series],
                        value=['ATP250','Masters 1000','Grand Slam','ATP500','Masters Cup'],
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
                )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ]),
    dcc.Graph(
        id='RankVsPoints'
    ),
    html.Div([
    html.Label('Select Court Surface'),
      dcc.Dropdown(id='y_dropdown',
                  options=[{'label': i, 'value': i}
                          for i in sur],
                  value= sur,
                  multi=True
      )],style={'width': '49%'}),
    html.Div([
        html.Div([
            dcc.Graph(
                id='SetsVsSurface'
            )
        ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='RankVsWinCounts',
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ])

])

@app.callback(
    Output(component_id='RankVsPoints', component_property='figure'),
    [Input(component_id='series_dropdown', component_property='value'),
    Input(component_id='win_range', component_property='value')]
)
def update_graph(selected_series,rangevalue):
    if not selected_series:
        return dash.no_update
    data =[]
    d = loc_data[(loc_data['win_counts'] >= rangevalue[0]) & (loc_data['win_counts'] <= rangevalue[1])]
    for j in selected_series:
            data.append(d[d['series'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    scat_fig = px.scatter(data_frame=df, x="wrank", y="wpts",
                size="best_of", 
                color="series",hover_name="winner",
                hover_data=['round', 'tournament', 'loser'],
                # create column for each series
                facet_col='series', 
               #add frame by year to create animation grouped by winner
               animation_frame="year",animation_group="winner",
               #specify formating of markers and axes
               size_max=10, range_x=[-500,1000], range_y=[-2000,15000],
                # change labels
                labels={'wrank':'ATP Rank','year':'Year','wpts':'ATP Points',
                        'tournament':'Tournament','series':'Series','winner':'Player',
                        'best_of':'Best_of','round':'Round','loser':'Loser'})
    # split facet column title
    scat_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    # 45 angle of tick 
    #scat_fig.update_xaxes(tickangle=45)
    scat_fig.update_layout(showlegend=False)

    return scat_fig

@app.callback(
    [Output(component_id='RankVsWinCounts', component_property='figure'),
    Output(component_id='SetsVsSurface', component_property='figure')],
    [Input(component_id='series_dropdown', component_property='value'),
    Input(component_id='win_range', component_property='value'),
    Input(component_id='y_dropdown', component_property='value')]
)
def update_line(selected_surface,rangevalue,yvar):
    if not (selected_surface or rangevalue or yvar):
        return dash.no_update
    d = loc_data[(loc_data['win_counts'] >= rangevalue[0]) & (loc_data['win_counts'] <= rangevalue[1])]
    data =[]
    data2 = []
    for j in selected_surface:
            data.append(d[d['series'] == j])
    dk = pd.DataFrame(np.concatenate(data), columns=cols)
    
    for k in yvar:
            data2.append(dk[dk['surface'] == k])
    df = pd.DataFrame(np.concatenate(data2), columns=cols)
    df=df.infer_objects()

    linesfig = px.histogram(df, x="court", color="surface",
                            #  set y axis as index or total number of matches
                            # hover_data=['court'],
                            #hover_name="winner",
                            animation_frame="year",
                            title='Match Court vs Surface',
                            labels= {'surface': 'Surface', 'court': 'Court',  
                                     'year': 'Year'},
                            color_discrete_sequence=["#479ded", "#7a660a", "#71f545"],
                            orientation="v",opacity = 0.7)

    # Change the axis titles
    linesfig.update_layout({'xaxis': {'title': {'text': 'Court'}},
                'yaxis': {'title': {'text': 'Total Number of Matches'}}})


    #linesfig.update_xaxes(
  #  dtick="M4",
    #tickformat="%b-""%y",
   # ticklabelmode="period")
    #linesfig.update_layout(showlegend=False)
    
    sc_fig = px.scatter(df, x="win_counts", y='wrank',
                        hover_data=['round', 'wpts','tournament', 'year', 'surface'],
                        color='series', hover_name="winner", 
                        title="Ranks vs Match Win Counts",
                        range_x=[0,250],
                        labels={'wrank':'ATP Rank','year':'Year','wpts': 'ATP Points',
                                'tournament': 'Tournament', 'series':'Series',
                                'winner':'Winner', 'win_counts': 'Match Win Counts', 
                                'round': 'Round', 'surface': 'Surface'})

    sc_fig.update_traces(marker_size=8)
    sc_fig.update_yaxes(range=[20, 0])
 
    return [sc_fig, linesfig]

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8097,debug=True)
