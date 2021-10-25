import dash
from dash import dcc  # create interactive components
from dash import html  # access html tags
from dash.dependencies import Input, Output

#app
from app import app
#map
from apps import map_world
from apps import map_vn
layout=html.Div([
    dcc.RadioItems(
        id='user-choice',
        options=[
            {'label': 'Thế Giới', 'value': 'world'},
            {'label': 'Việt Nam', 'value': 'vn'}
        ],
        value='world',
        labelStyle={'display': 'inline-block'}
    ),
    html.Div(id='page_content', children=[])
])

# -----------------
#Radio button => map
@app.callback(
    [Output('page_content','children')],
    [Input('user-choice','value')] 
)
def update_content(choice):
    if(choice=='world'):
        return map_world.layout
    elif(choice=='vn'):
        return map_vn.layout