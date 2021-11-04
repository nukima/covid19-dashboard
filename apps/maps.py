import dash
from dash import dcc  # create interactive components
from dash import html  # access html tags
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
#map
import map_vn, map_world
#app
from app import app
# layout=html.Div([
#     html.Div([dcc.RadioItems(
#         id='user-choice',
#         options=[
#             {'label': 'Thế Giới', 'value': 'world'},
#             {'label': 'Việt Nam', 'value': 'vn'}
#         ],
#         value='world',
#         labelStyle={'display': 'inline-block'}
#     )], id= "menu-inside-home"),
#     html.Div(id='page_content', children=[])
# ])
layout=html.Div([
    html.Div([
        html.Div("Thế Giới", id = "menu-inside-home-world"),
        html.Div("Việt nam", id = "menu-inside-home-vietnam")
    ],id= "menu-inside-home"),
    html.Div(id='home-content', children=[])
], id = "homamainlayout")
# -----------------
#Radio button => map
# @app.callback(
#     Output('page_content','children'),
#     Input('user-choice','value') 
# )
# def update_content(choice):
#     if(choice=='world'):
#         return map_world.layout
#     elif(choice=='vn'):
#         return map_vn.layout

control = 1


@app.callback(
    Output('homamainlayout','children'),
    Input('menu-inside-home-vietnam','n_clicks'),
    Input('menu-inside-home-world','n_clicks'),
)
def display(btn1, btn2):
    ctx = dash.callback_context
    if(ctx.triggered[0]['prop_id'].split('.')[0] == "menu-inside-home-vietnam"):
        return  html.Div([
                    html.Div([
                        html.Div("Thế Giới", id = "menu-inside-home-world", className="home-btn"),
                        html.Div("Việt nam", id = "menu-inside-home-vietnam", className="home-btn-chose")
                    ],id= "menu-inside-home"),
                    html.Div(id='home-content', children=[map_vn.layout])
                ], id = "homamainlayout")
    else:
        return  html.Div([
                    html.Div([
                        html.Div("Thế Giới", id = "menu-inside-home-world", className="home-btn-chose" ),
                        html.Div("Việt nam", id = "menu-inside-home-vietnam", className="home-btn")
                    ],id= "menu-inside-home"),
                    html.Div(id='home-content', children=[map_world.layout])
                ], id = "homamainlayout")

    

# @app.callback(
#     Output('page_content','children'),
#     [Input('menu-inside-home-vietnam','n_clicks') ],
#     prevent_initial_call=True
# )
# def clicks(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         return map_vn.layout