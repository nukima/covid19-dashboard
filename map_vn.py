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


# -----------------
#Handle the data
df,nocases=map_vn_data()
# -----------------


layout=html.Div([
    html.Div(id="mapv"),
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
        # editable=False,
        filter_action="native",
        # sort_action="native",
        # sort_mode='multi',
        # row_selectable='multi',
        # row_deletable=False,
        # selected_rows=[],
        # page_action='native',
        # page_current= 0,
        # page_size= 10,
        # style_header={
        #                 'backgroundColor': '#CCE2CB',
        #                 'fontWeight': 'bold'
        #     },
        # style_data_conditional=[
        #         {
        #             'if': {'row_index': 'odd'},
        #             'backgroundColor': 'rgb(220, 220, 220)',
        #         }
        #     ],
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
                        'fontSize'  : '18px',
                        # 'backgroundColor': '#fafafa'
                    },
         style_as_list_view=True,
        # style_data_conditional=[
        #         {
        #             # 'if': {'row_index': 'odd'},
        #             'backgroundColor': 'rgb(220, 220, 220)',
        #         }
        #     ],
    )
])

@app.callback(
    Output('mapv', 'children'),
    Input('datatable-vietnam', 'derived_virtual_selected_rows')
)

def update_graphs(slctd_row_indices):
    zoom_idx=5
    if slctd_row_indices is None:
        slctd_row_indices=[]
    id=0
    if len(slctd_row_indices)>0:
        id=slctd_row_indices[-1]
        zoom_idx=7
    return dcc.Graph(id='MVN',figure=map_vietnam(id,zoom_idx))

def map_vietnam(id,zoom_idx):
    fig = px.scatter_mapbox(df, lat="lat", lon="lng",hover_data={"cases":True,"casesToday":True,"lat":False,"lng":False},hover_name="name", size=nocases,color="cases",
                            color_continuous_scale=px.colors.diverging.Tealrose, zoom=zoom_idx,
                            center={"lat":df.at[id,"lat"],"lon":df.at[id,"lng"]})
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(clickmode="select")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# #datatable highlight selected_row
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

# if __name__ == '__main__':
#     app.run_server(debug=True)