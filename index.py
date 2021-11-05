from os import path
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to app pages
from apps import world, vietnam, maps


# first section layout
app.layout = html.Div([
    html.H1("Covid19 Thông Tin" , id = "title"),
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Home', href='/',
                 style={'font-weight': 'bold'}),
        dcc.Link('World', href='/apps/world',
                 style={'font-weight': 'bold'}),
        dcc.Link('Việt Nam', href='/apps/vietnam',
                 style={'font-weight': 'bold'}),
    ], className="row", id = "menu"),
    html.Div(id='page-content', children=[])
])


#------------------
#callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/world':
        return world.layout
    if pathname == '/apps/vietnam':
        return vietnam.layout
    if pathname == '/':
        return maps.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)
