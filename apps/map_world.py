# dependencies 
import pandas as pd  # organize the data
import plotly.express as px
from dash import dash_table
from dash.dash_table.Format import Format
from dash import dcc  # create interactive components
from dash import html  # access html tags
from dash.dependencies import Input, Output


from get_covid_data import map_world_data
from app import app #app
from .navbar import create_navbar #navbar


nav = create_navbar()
# -----------------
#Handle the data
dff,cases,deaths=map_world_data()
# -----------------


#Map world layout
layout=html.Div([
    nav,
    html.Div([
    html.Div(id="mapw"),
    html.Div([
    html.Div(id="total",children=[
        html.Div("Thế Giới"),
        html.Div([
        html.Div([
        html.Div("Tổng số ca nhiễm: "),
        html.Div("{:,}".format(cases))
        ]),
        html.Div([
        html.Div("Tổng số ca tử vong: "),
        html.Div("{:,}".format(deaths))
        ])
        ])
    ], className= "totalDiv"),
    #data-table
    dash_table.DataTable(
        id='datatable-world',
        columns=[
            {"name":"Quốc gia","id":"Quốc gia"},
            dict(id='Số ca', name='Số ca', type='numeric', format=Format().group(True)), 
            dict(id='Tử vong', name='Tử vong', type='numeric', format=Format().group(True)), 
            dict(id='Tỉ lệ tử vong', name='Tỉ lệ tử vong', type='numeric',format=Format(precision=3)),     
        ],
        data=dff.to_dict('records'),
        style_data_conditional=[                
           {
               "if": {"state": "selected"},
               "backgroundColor": "inherit !important",
               "border": "inherit !important",
           },
            {'if': {'column_id': 'Quốc gia'},
            'width': '5%', 'textAlign': 'center'},],  
        fixed_rows={'headers': True, 'data': 0},
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        style_table={'height': '600px', 'overflowY': 'auto','border': '1px solid grey', "width": "500px"},
        style_data={ 'border': '1px solid grey' },
        style_header={
                        'backgroundColor': '#daf2e2',
                        'fontWeight': 'bold',
                        'fontSize'  : '18px'
            },
        style_as_list_view=True,
    )])
    ], id = "map_world"),
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
                        hover_data={'Số ca':True,'Tử vong':True,"id":False},hover_name="Quốc gia",
                        color_continuous_scale=px.colors.diverging.Tealrose,
                        color_continuous_midpoint=1000000,
                        range_color=[0,50000000],
                        template='plotly')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
