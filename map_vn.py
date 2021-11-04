import pandas as pd  # organize the data
import plotly.express as px
from dash import dash_table
from dash import dcc  # create interactive components
from dash import html  # access html tags
from dash.dependencies import Input, Output
from get_covid_data import get_vietnam_covid_data
import numpy as np
#app
from app import app


# -----------------
#Handle the data
today, total_data_df, today_data_df, overview_7days_df, city_data_df=get_vietnam_covid_data()
vn_location=pd.read_json("covid19-dashboard/vn_location.json")
df=city_data_df
dff=pd.merge(df,vn_location)
# print(dff)
nocases=[]
for x in dff['cases']:
    if(x == 0):
        nocases.append(0)
    else:
        nocases.append(np.log2(x))
# -----------------

def map_vietnam(dff):
    """Return a graph about number of covid-19 cases in Vietnam"""
    #Plot the graph
    fig = px.scatter_mapbox(dff, lat="lat", lon="lng",hover_data={"cases":True,"casesToday":True,"lat":False,"lng":False},hover_name="name", size=nocases,color="cases",
                            color_continuous_scale=px.colors.diverging.Tealrose, zoom=5)
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(clickmode="select")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
layout=html.Div([
    html.Div(id="mapv",children=[dcc.Graph(id='MVN',figure=map_vietnam(dff))]),
    dash_table.DataTable(
        id='datatable-vietnam',
        columns=[
            {'name': i, 'id': i, 'deletable': False} for i in df.columns
            # omit the id column
            if i != 'id' and i!="index"
        ],
        data=df.to_dict('records'),
        style_data_conditional=[                
            {
                "if": {"state": "selected"},
                "backgroundColor": "inherit !important",
                "border": "inherit !important",
            }],  
        # editable=False,
        # filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=False,
        # selected_rows=[],
        # page_action='native',
        # page_current= 0,
        # page_size= 10,
        style_table={'height': '600px', 'overflowY': 'auto', "width": "400px"},
        style_header={
                        # 'backgroundColor': '#CCE2CB',
                        'fontWeight': 'bold',
                        'fontSize'  : '18px'
                    },
         style_as_list_view=True,
        # style_data_conditional=[
        #         {
        #             # 'if': {'row_index': 'odd'},
        #             'backgroundColor': 'rgb(220, 220, 220)',
        #         }
        #     ],
    ),
])

# @app.callback(
#     Output('mapv', 'children'),
#     [Input('datatable-vietnam', 'derived_virtual_data'),
#     Input('datatable-vietnam', 'derived_virtual_selected_rows')]
# )

# def update_graphs(all_rows_data, slctd_row_indices):
#     if slctd_row_indices is None:
#         slctd_row_indices=[]
#     dff2 = pd.DataFrame(all_rows_data)
#     if "id" in dff2:
#         return dcc.Graph(id='MVN',figure=map_vietnam(dff2))

# def map_vietnam(dff):
#     """Return a graph about number of covid-19 cases in Vietnam"""
#     #Plot the graph
#     fig = px.scatter_mapbox(dff, lat="lat", lon="lng",hover_data={"cases":True,"casesToday":True,"lat":False,"lng":False},hover_name="name", size=nocases,color="cases",
#                             color_continuous_scale=px.colors.diverging.Tealrose, zoom=5)
#     fig.update_layout(mapbox_style="carto-positron")
#     fig.update_layout(clickmode="select")
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     return fig

#datatable highlight selected_row
# @app.callback(
#     Output('datatable-vietnam', 'style_data_conditional'),
#     [Input('datatable-vietnam', 'derived_viewport_selected_rows'),]
# )
# def highlight_selectedRow(chosen_rows):
#     style_data_conditional=[
#                 {
#                     'if': {'row_index': 'odd'},
#                     'backgroundColor': 'rgb(220, 220, 220)',
#                 },
#                 {
#                     'if': {'row_index': chosen_rows},
#                     'backgroundColor': '#D4F0F0'
#                 },
#             ]
#     return style_data_conditional