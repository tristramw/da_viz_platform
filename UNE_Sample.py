import numpy as np
import pandas as pd



import dash

import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


df = pd.read_csv('Sheet 1-Table 1.csv')


levels = df['Clevel3 Description'].unique()  #names of areas of UNE
classifications = df['CLASSIFICATION'].unique() #job classifactions

app = dash.Dash()

app.layout = html.Div([
                html.Div([
                    dcc.Dropdown(id ='Dropdown',
                                options = [{'label': i, 'value' : i} for i in levels],
                                value = levels[0])
                ]),
                html.Div([
                    dcc.Graph(id ='ClassPieChart')
                ]),
                html.Div([
                    dcc.Graph(id = 'GenderPieChart')
                ]),
                html.Div([
                    dcc.Graph(id = 'HoursHist')
                ])
])

@app.callback(Output('ClassPieChart','figure'),
        [Input('Dropdown', 'value')])
def update_Class_graph(level):  #Pie graph showing classifications with each level
    dff = df[df['Clevel3 Description']==level] #filtered data Frame
    labels = classifications #labels are names of classifications
    values = [len(dff[dff['CLASSIFICATION'] == i]) for i in classifications]
    #values are numbers within each classification, within each level
    data_zeros = []

    for i in range(len(labels) - 1):  #remove from plot where values are 0
        if values[i] == 0:
            data_zeros.append(i)

    new_labels = np.delete(labels, data_zeros)  # new labels without zero values
    new_values = np.delete(values, data_zeros)

    data = [go.Pie(labels = new_labels, values = new_values)]
    layout = go.Layout(title = 'Breakdown of Classifications within {}'.format(level))

    return {'data': data, 'layout': layout}




@app.callback(
      Output('GenderPieChart', 'figure'),
       [Input('Dropdown', 'value')])
def update_Gender_graph(level): #pie chart showing gender division within levels
    dff = df[df['Clevel3 Description']==level] #filtered DF
    labels = ['M', 'F']
    values = [dff[dff['GENDER']=='M'].count()['GENDER'],
                dff[dff['GENDER']=='F'].count()['GENDER']]
    data = [go.Pie(labels=labels, values=values)]
    layout = go.Layout( title = 'gender difference in Level {}'.format(level))
    return {'data': data, 'layout': layout}


@app.callback(Output('HoursHist', 'figure'), [Input('Dropdown', 'value')])
def update_histogram(level): #histogram showing FTE within levels, for Male/Female
    dff = df[df['Clevel3 Description']==level] #filtered DF
    Male = go.Histogram(x = dff[dff['GENDER']=='M']['Person FTE'], #hist for males
    opacity = 0.75, name = 'Male')
    Female = go.Histogram(x = dff[dff['GENDER']=='F']['Person FTE'], #hist for females
    opacity = 0.75, name='Female')

    data = [Male, Female]
    layout = go.Layout(title = 'Fraction of FTE for M and F in {}'.format(level))
    return {'data': data, 'layout': layout}


if __name__ == '__main__':
    app.run_server()
