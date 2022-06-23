from http import server
import dash
from dash import dcc
# from dash import dcc
from dash import html
# from dash import html
import pandas as pd
import plotly.graph_objects as go
from pymongo import MongoClient
import plotly.express as px
import urllib.parse
username = urllib.parse.quote_plus('kris')
password = urllib.parse.quote_plus('@Krishna8')

app = dash.Dash(__name__)
server = app.server
client = MongoClient(
    'mongodb+srv://%s:%s@cluster0.0vg1ud3.mongodb.net/' % (username, password))
db = client.fyproj
collection = db.ques
print("connection_created")
cursor = collection.find()
data = pd.DataFrame(list(cursor))
# del data['Unnamed: 0']
del data['_id']
cols = []
for i in data.columns:
    cols.append({'label': i, 'value': i})
print(len(cols))
print(cols)

app.layout = html.Div([
    html.Div([
        html.Div(
            [
                html.H1(children='Admin Dashboard',
                        className='twelve columns offset-by-two.columns', style={'color': '#999999'})
            ], id='title', className="row"
        ),
        html.Hr(),
        html.Div([html.H4("Questionnaire Statistics")],
                 className='twelve columns', style={'color': '#999999'}),
        html.Div([dcc.Dropdown(
            id='dropdown',
            options=cols,
            value='interferes_with_work')], className='twelve columns', style={'margin-bottom': '10px'}),
        html.Div(
            [
                html.Div([
                    dcc.Graph(id='v_line')
                ], className='six columns'
                ),

                html.Div(
                    [dcc.Graph(id='bar')
                     ], className="six columns"
                )
            ], className="row"
        ),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id='colorbar')
                     ], className="twelve columns"
                )
            ], className="row"
        ),
    ], className='ten columns offset-by-one')
], style={'background-color': '#2c2c2e'})


@app.callback(dash.dependencies.Output('v_line', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def update_graph(selector):
    df = data[selector].value_counts()
    print(type(df))
    figure = px.pie(values=df, names=df.index, color_discrete_sequence=px.colors.qualitative.Pastel,
                    title="Percentage Distribution of Answers")
    return figure


@app.callback(dash.dependencies.Output('bar', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def update_graph_2(selector):
    df = data[selector].value_counts()
    print(type(df))
    figure = px.bar(x=df.index, y=df, color=df.index, title="Count Plot of Answers",
                    color_discrete_sequence=px.colors.qualitative.Plotly)
    return figure


@app.callback(dash.dependencies.Output('colorbar', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def update_graph_2(selector):
    dfl0 = data[data['predicted_level'] == '[0]'][selector].value_counts()
    dfl1 = data[data['predicted_level'] == '[1]'][selector].value_counts()
    dfl2 = data[data['predicted_level'] == '[2]'][selector].value_counts()
    figure = go.Figure(data=[
        go.Bar(name='Level 0', x=dfl0.index, y=dfl0),
        go.Bar(name='Level 1', x=dfl1.index, y=dfl1),
        go.Bar(name='Level 2', x=dfl2.index, y=dfl2),
    ],
        layout=go.Layout(
        title=go.layout.Title(text="Predicted Levels by Answers")
    ))
    return figure


if __name__ == '__main__':
    server.run(debug=True)
