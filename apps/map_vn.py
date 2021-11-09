import pandas as pd  # organize the data
import plotly.express as px
import requests
import dash
from dash import dash_table
from dash import dcc  # create interactive components
from dash import html  # access html tags
from dash.dependencies import Input, Output
from get_covid_data import map_vn_data
#app
from app import app
#navbar
from .navbar import create_navbar

nav = create_navbar()

# -----------------
#Handle the data
df,nocases,cases,deaths,today=map_vn_data()
# -----------------


layout=html.Div([
    nav,
    html.Div([
    html.Div(id="mapv"),
    html.Div([
    html.Div(id="total",children=[
        html.Div("Việt Nam"),
        html.Div([
        html.Div([
        html.Div("Tổng số ca nhiễm: "),
        html.Div("{:,}".format(cases))
        ]),
        html.Div([
        html.Div("Tổng số ca tử vong: "),
        html.Div("{:,}".format(deaths))
        ]),
        ]
        ),
        html.Div(["(Số liệu được cập nhật ngày "+today+")"],style={"fontFamily":"italic"})
    ], className= "totalDiv"),
    dash_table.DataTable(
        id='datatable-vietnam',
        columns=[
            {'name': i, 'id': i, 'deletable': False} for i in df.columns
            # omit the id column
            if i != 'id' and i!="index" and i not in ["treating","recovered","lat","lng"]
        ],
        style_data_conditional=[                
        {
            "if": {"state": "selected"},
            "backgroundColor": "inherit !important",
            "border": "inherit !important",
        }],  
        data=df.to_dict('records'),
        fixed_rows={'headers': True, 'data': 0},
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=False,
        style_table={'height': '600px', 'overflowY': 'auto', "width": "500px"},
        style_header={
                        'backgroundColor': '#daf2e2',
                        'fontWeight': 'bold',
                        'fontSize'  : '18px',
                    },
         style_as_list_view=True,
    )])], id = "map_vn")
])

@app.callback(
    Output('mapv', 'children'),
    Input('datatable-vietnam', 'derived_virtual_selected_rows')
)

def update_graphs(slctd_row_indices):
    centerlat=16.06944
    centerlon=108.20972
    zoom_idx=5
    if slctd_row_indices is None:
        slctd_row_indices=[]
    id=0
    if len(slctd_row_indices)>0:
        id=slctd_row_indices[-1]
        zoom_idx=9
        centerlat=df.at[id,"lat"]
        centerlon=df.at[id,"lng"]  
    return dcc.Graph(id='MVN',figure=map_vietnam(id,zoom_idx,centerlat,centerlon))

def map_vietnam(id,zoom_idx,centerlat,centerlon):
    fig = px.scatter_mapbox(df, lat="lat", lon="lng",hover_data={"Số ca":True,"Số ca hôm nay":True,"lat":False,"lng":False},hover_name="Tỉnh thành", size=nocases,color="Số ca",
                            color_continuous_scale=px.colors.diverging.Temps,
                            zoom=zoom_idx, opacity=0.9,
                            center={"lat":centerlat,"lon":centerlon})
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(clickmode="select")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

