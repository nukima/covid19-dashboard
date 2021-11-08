import pandas as pd  # organize the data
import plotly.express as px
import dash
from dash import dash_table
from dash import dcc  # create interactive components
from dash import html  # access html tags
from dash.dependencies import Input, Output
from get_covid_data import map_world_data
#app
from app import app
#navbar
from .navbar import create_navbar

nav = create_navbar()
# -----------------
#Handle the data
dff,cases,deaths=map_world_data()
# -----------------


#Map world layout
layout=html.Div([
    #Place to put the 
    nav,
    html.Div(id="mapw"),
    html.Div(id="total",children=[
        html.Div("Tổng số ca nhiễm: "+str(cases)),
        html.Div("Tổng số ca tử vong: "+str(deaths)),
        
    ]),
    #Place to put the table
    dash_table.DataTable(
        id='datatable-world',
        columns=[
            {'name': i, 'id': i, 'deletable': False} for i in dff.columns
            # omit the id column
            if i != 'id' and i!="index"
        ],
        data=dff.to_dict('records'),
        # editable=False,
        style_data_conditional=[                
           {
               "if": {"state": "selected"},
               "backgroundColor": "inherit !important",
               "border": "inherit !important",
           }],  
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        # row_deletable=False,
        # selected_rows=[],
        # page_action='native',
        # page_current= 0,
        # page_size= 10,
        style_table={'height': '600px', 'overflowY': 'auto','border': '1px solid grey'},
        style_data={ 'border': '1px solid grey' },
        style_header={
                        # 'backgroundColor': '#CCE2CB',
                        'fontWeight': 'bold',
                        'fontSize'  : '18px'
            },
        style_as_list_view=True,
        # style_data_conditional=[
        #         {
        #             "cusor": "poiter",
        #             # 'backgroundColor': 'rgb(220, 220, 220)',
        #         }
        #     ],
    ),
])

# -----------------
#data table => map
@app.callback(
    Output('mapw', 'children'),
    [Input('datatable-world', 'derived_virtual_data'),
    Input('datatable-world', 'derived_virtual_selected_rows')]
)
def update_graphs(all_rows_data, slctd_row_indices):
    if slctd_row_indices is None:
        slctd_row_indices=[]
    dff2 = pd.DataFrame(all_rows_data)
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dff))]
    if "id" in dff2:
        return dcc.Graph(id='MW',figure=map_world(dff2).update_traces(marker_line_width=borders))


def map_world(dff2):
    """Return a graph about number of global covid-19 cases """

    fig=px.choropleth(data_frame=dff2,locations='id',locationmode='ISO-3',
                        color='Số ca',
                        hover_data=['Số ca','Tử vong'],hover_name="Quốc gia",
                        color_continuous_scale=px.colors.diverging.Tealrose,
                        color_continuous_midpoint=1000000,
                        range_color=[0,50000000],
                        template='plotly')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

#datatable highlight selected_row
# @app.callback(
#     Output('datatable-world', 'style_data_conditional'),
#     [Input('datatable-world', 'derived_viewport_selected_rows'),]
# )
# def highlight_selectedRow(chosen_rows):
#     style_data_conditional=[
#                 {
#                     'if': {'row_index': 'odd'},
#                     'backgroundColor': 'rgb(220, 220, 220)',
#                 },
#                 {
#                     'if': {'row_index': chosen_rows},
#                     'backgroundColor': 'rgb(220, 220, 220)'
#                 },
#             ]
#     return style_data_conditional


# -------------------------------
    