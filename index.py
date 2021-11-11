# dependencies 
from dash import dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to app pages
from apps import world, vietnam, map_vn,map_world


# layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[]),
    html.Div(
        [
        html.Div(
        [
            html.Div("Dự án được khởi tạo bởi nhóm 3"),
            html.Div("Thành viên: Dương Văn Giang, Nguyễn Kim Mạnh, Nguyễn Phương Nam"),
            html.A("Source Code: Github", href='https://github.com/nukima/covid19-dashboard.git', target="_blank"),
        ])
        ]
    , id = "footer")
])


#------------------
# navbar-callback
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
    app.run_server(debug=False)
