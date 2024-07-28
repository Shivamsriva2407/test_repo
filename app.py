import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import dash as dash
import dash_html_components as html
from dash import dcc
from dash.dcc import Input
from dash.html import Output

# external css stylesheet
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': "sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO",
        'crossorigin': 'anonymous'
    }
]

patients = pd.read_csv('IndividualDetails.csv')

Total = patients.shape[0]
Active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
Recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
Death = patients[patients['current_status'] == 'Deceased'].shape[0]

options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]


temp = patients.groupby('diagnosed_date')['id'].count().reset_index()
fig = px.line(temp,x=temp['diagnosed_date'],y=temp['id'])

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# starting the main code from here
app.layout = html.Div([
    html.H1("Corona Virus- India's persective", style={'color': '#ffffff', 'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Total Cases', className='text-light'),
                    html.H4(Total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Active', className='text-light'),
                    html.H4(Active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')

        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Recovered', className='text-light'),
                    html.H4(Recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Deaths', className='text-light'),
                    html.H4(Death, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3')

        #     Different row started
    ], className='row'),
    # second row
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='line',
                              figure=fig,
                              style={'width': '500px', 'height': '400px'})
                ],className='card-body')
            ],className='card')
        ],className='col-md-6'),
        html.Div([],className='col-md-6')
    ], className='row'),
    # third row
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    #      add drop down and the bar chart
                    dcc.Dropdown(id='picker', options=options, value='All'),
                    #  genrally dcc. Graph takes 2 argumment, id and figure, but we are plotting based on the dropdown, so will
                    # will create a function that will plot the graph
                    dcc.Graph(id='bar',style={'width': '1000px', 'height': '700px'})

                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row')
], className='container')


# @app.callback(Output('bar', 'figure'), Input('picker', 'value'))
@app.callback(dash.Output('bar','figure'),[dash.Input('picker','value')])
def update_graph(type):
    # plot graph

    if type=='All':
        pbar = patients['detected_state'].value_counts().reset_index()
        return {
            # data has trace inside it, so we have directly plotted trace in here
            'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
            'layout': go.Layout(title='State Total count')
        }
    else:
        temp = patients[patients['current_status'] == type]
        pbar = temp['detected_state'].value_counts().reset_index()
        return {
            'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
            'layout': go.Layout(title='State Total count')
        }

# @app.callback(dash.Output('line','figure'),[dash.Input()])
# def graph(text):
#     temp = patients.groupby('diagnosed_date')['id'].count().reset_index()
#     return {
#         'data':[go.Line(x=temp['diagnosed_date'],y=temp['id'])],
#         'layout':go.layout(title='Day by day analyis')
#     }

if __name__ == "__main__":
    app.run_server(debug=True)
