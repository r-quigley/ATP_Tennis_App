import dash
from dash import html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("Welcome to the ATP Tour Dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This app shows the ATP results for each ATP match from 2017 to 2021. '
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='It consists of three main pages: ATP Matches, which gives an overview of all ATP tournaments in the last five years, '
                                     'Top 10 Players, which gives an overview of the 2021 top 10 ATP ranked players, '
                                     'and Grand Slam, which gives an overview of the top ranked players performance in the the series.')
                    , className="mb-5")
        ]),

        dbc.Row([
            # 2 columns of width 6 with a border
            dbc.Col(dbc.Card(children=[html.H3(children='Go to the original tennis dataset for more data',
                                               className="text-center"),
                                       dbc.Button("ATP Data",
                                                  href="http://www.tennis-data.co.uk/alldata.php",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                               className="text-center"),
                                       dbc.Button("GitHub",
                                                  href="https://github.com/r-quigley/ATP_Tennis_App",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

        ], className="mb-5"),
        dbc.Row([
            dbc.Col(html.Img(src=app.get_asset_url('atploveitall.jpeg')), 
            width={"size": 6, "offset": 3})
        ]),
        html.A("ATP Unveils New Brand And ""Love It All"" Global Marketing Campaign.",
               href="https://www.atptour.com/en/news/atp-2019-brand-global-marketing-campaign")

    ])

])

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8098,debug=True)
