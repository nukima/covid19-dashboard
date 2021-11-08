from os import path
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to app pages
from apps import world, vietnam, map_vn,map_world


# first section layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[]),
    html.Div(
        [
        html.Div(
        [
            html.Div("Dự án được khởi tạo bởi nhóm 3"),
            html.Div("Thành viên: Dương Văn Giang, Nguyễn Kim Mạnh, Nguyễn Phương Nam"),
            html.Div("Source: https://github.com/nukima/covid19-dashboard.git")
        ])
        ]
    , id = "footer")
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
    if pathname == '/apps/map_world':
        return map_world.layout
    if pathname == '/apps/map_vn':
        return map_vn.layout    
    if pathname == '/':
        return map_world.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server()
