import pandas as pd  
import numpy as np  
import sys

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
import plotly.graph_objs as go


df = pd.read_csv('GS_all_GSIDs_Company_names.csv')
df.drop(['Unnamed: 0'],axis = 1,inplace = True)

company_groups = df.groupby(['company_name']).groups#['userid'].value_counts()
key1 = 'Apple Inc'
date = df.iloc[company_groups[key1]]['date']

df['year'] = pd.DatetimeIndex(df['date']).year
company_2017_growthscores = df.groupby(['year','company_name'])['growthScore'].mean()
cg = company_2017_growthscores[2017]. sort_values(ascending = False)[:5]
cgg = pd.DataFrame(cg)
cgg['company_name'] = cgg.index
cgg = cgg[['company_name','growthScore']]
cgg = cgg.round(3)
company_2017_multiplescore = df.groupby(['year','company_name'])['multipleScore'].mean()
cm = company_2017_multiplescore[2017]. sort_values(ascending = True)[:5]
cmm = pd.DataFrame(cm)
cmm['company_name'] = cmm.index
cmm = cmm[['company_name','multipleScore']]
cmm = cmm.round(3)
company_2017_financialreturnscore = df.groupby(['year','company_name'])['financialReturnsScore'].mean()
cf = company_2017_financialreturnscore[2017]. sort_values(ascending = False)[:5]
cff = pd.DataFrame(cf)
cff['company_name'] = cff.index
cff = cff[['company_name','financialReturnsScore']]
cff = cff.round(3)


app = dash.Dash()
colors = {
    'background': '#111111',
    'text': 'Teal'
}

def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app.layout = html.Div([
    
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Explore', children=[
                    html.Div([
                        html.H1('Examine Stock',style={
                                'textAlign': 'center',
                                'color': colors['text']
                        }),
                        dcc.Dropdown(
                            id='my-dropdown',
                            options=[{'label': i, 'value': i} for i in list(df['company_name'].drop_duplicates())],
                            value='Carnival Corp'
                        ),
                        dcc.Graph(id='my-graph1',
                                 figure={
                                'layout': {
                                    'height': 600
                                }
                        }),
                    ])
                ]),
                dcc.Tab(label='Analyze', children=[
                    html.Div([
                        html.Div([
                            html.H1('Compare Stocks',style={
                                    'textAlign': 'center',
                                    'color': colors['text'],
                                    'font' : 'Helvetica Light'
                                }),
                            dcc.Dropdown(
                                id='company_1',
                                options=[{'label': i, 'value': i} for i in list(df['company_name'].drop_duplicates())],
                                value='Carnival Corp'
                            ),
                            dcc.Dropdown(
                                id='company_2',
                                options=[{'label': i, 'value': i} for i in list(df['company_name'].drop_duplicates())],
                                value='Tesla Inc',
                            ),
                            dcc.Dropdown(
                                id='company_3',
                                options=[{'label': i, 'value': i} for i in list(df['company_name'].drop_duplicates())],
                                value='Apple Inc',
                            ),
                            dcc.Dropdown(
                                id='company_4',
                                options=[{'label': i, 'value': i} for i in list(df['company_name'].drop_duplicates())],
                                value='Target Corp',
                            ),
                            dcc.RadioItems(
                                        id='my_button',
                                        options = [{'label': 'Integrated Score', 'value': 'integratedScore'},
                                        {'label': 'Growth Score', 'value': 'growthScore'},
                                        {'label': 'Multiple Score', 'value': 'multipleScore'},
                                        {'label': 'Financial Returns Score', 'value': 'financialReturnsScore'}],
                                        labelStyle={'display': 'inline-block', 'font' : 'Helvetica Light'},
                                value = 'integratedScore'
                                    ),
                        ]),
                        dcc.Graph(id='my-graph2',
                                 figure={
                                'layout': {
                                    'height': 600
                                }
                        }),
                    ])
                ]),
                dcc.Tab(label='Our Picks', children=[
                    html.Div([
                        html.Div([
                            html.H1('Recommended Stocks',style={
                                    'textAlign': 'center',
                                    'color': colors['text'],
                                    'font' : 'Times New Roman'
                            }),

                            
                            html.H2('High Growth',style={
                                    'textAlign': 'Center',
                                    'color': colors['text'],
                                    'font' : 'Times New Roman'
                            }),

                            generate_table(cgg),
                            
                            html.P("The first category focuses on investments that have high upside in the near future,\
                                   but also come with a substantial amount of risk. We placed more importance on growth and overlooked \
                                   the multiple factor when developing our algorithm to choose the set of investments that could have\
                                   rapid progress in the short term."
                                ,style={
                                        'textAlign': 'Center',
                                        'font' : 'Times New Roman'
                                }
                            ),
                            
                            html.P(cg.index.values + " " + " . " + " "
                                  ,style={
                                        'textAlign': 'Center',
                                        'font' : 'Times New Roman'
                                }),

                            html.H2('Great Value',style={
                                    'textAlign': 'Center',
                                    'color': colors['text'],
                                    'font' : 'Times New Roman'
                            }),
                            
                            generate_table(cmm),

                            html.P("These stocks are diamonds in the rough. They are not valued at the price they deserve",
                                style={
                                        'textAlign': 'Center',
                                        'font' : 'Times New Roman'
                                }),
                            html.P(cm.index.values + " " + " . " + " ",
                                   style={
                                        'textAlign': 'Center',
                                        'font' : 'Times New Roman'
                                }),


                            html.H2('Consistent Returns',style={
                                    'textAlign': 'Center',
                                    'color': colors['text'],
                                    'font' : 'Times New Roman'
                            }),

                            generate_table(cff),

                            html.P("These stocks are reliable blue chips. You can expect them to keep paying dividends. Pensioners or people making a living off of capital gains should take note of these stocks",
                            style={
                                    'textAlign': 'Center',
                                    'font' : 'Times New Roman'
                            }),
                            html.P(cf.index.values + " " + " . " + " "
                                  ,style={
                                        'textAlign': 'Center',
                                        'font' : 'Times New Roman'
                                })


                        ],className='container', style={'maxWidth': '1000px'}),
                    ],className='container', style={'maxWidth': '1000px'})
                ], style={'maxWidth': '1500px','font': 'Times New Roman'})
                
            ], style={'maxWidth': '1500px','font': 'Times New Roman'})
            
    ], style={'maxWidth': '1500px','font': 'Times New Roman'})

@app.callback(Output('my-graph1', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    
    trace0 = go.Scatter(
        x = df.iloc[company_groups[key1]]['date'],
        y = df.iloc[company_groups[selected_dropdown_value]]['growthScore'],
        mode = 'lines',
        name = 'growthScore'
    )
    trace1 = go.Scatter(
        x = df.iloc[company_groups[key1]]['date'],
        y = df.iloc[company_groups[selected_dropdown_value]]['multipleScore'],
        mode = 'lines',
        name = 'multipleScore'
    )
    trace2 = go.Scatter(
        x = df.iloc[company_groups[key1]]['date'],
        y = df.iloc[company_groups[selected_dropdown_value]]['financialReturnsScore'],
        mode = 'lines',
        name = 'financialReturnsScore'
    )
    trace3 = go.Scatter(
        x = df.iloc[company_groups[key1]]['date'],
        y = df.iloc[company_groups[selected_dropdown_value]]['integratedScore'],
        mode = 'lines',
        name = 'integratedScore'
    )

    data = [trace0, trace1, trace2, trace3]


    return {
        'data': data
    }


@app.callback(dash.dependencies.Output('my-graph2', 'figure'),
    [dash.dependencies.Input('company_1', 'value'),
     dash.dependencies.Input('company_2', 'value'),
     dash.dependencies.Input('company_3', 'value'),
     dash.dependencies.Input('company_4', 'value'),
     dash.dependencies.Input('my_button', 'value')])
def update_graph2(company_1_name, company_2_name,
                 company_3_name, company_4_name,
                 my_button_value):
    
    trace0 = go.Scatter(
        x = df.iloc[company_groups[key1]]['date'],
        y = df.iloc[company_groups[company_1_name]][my_button_value],
        mode = 'lines',
        name = company_1_name
    )
    trace1 = go.Scatter(
        x = df.iloc[company_groups[key1]]['date'],
        y = df.iloc[company_groups[company_2_name]][my_button_value],
        mode = 'lines',
        name = company_2_name
    )
    trace2 = go.Scatter(
        x = df.iloc[company_groups[key1]]['date'],
        y = df.iloc[company_groups[company_3_name]][my_button_value],
        mode = 'lines',
        name = company_3_name
    )
    trace3 = go.Scatter(
        x = df.iloc[company_groups[key1]]['date'],
        y = df.iloc[company_groups[company_4_name]][my_button_value],
        mode = 'lines',
        name = company_4_name
    )

    data = [trace0, trace1, trace2, trace3]


    return {
        'data': data
    }

if __name__ == '__main__':
    app.run_server()
