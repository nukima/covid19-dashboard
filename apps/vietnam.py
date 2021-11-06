# import dash
from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output
#plotly
import plotly.express as px
#pandas
import pandas as pd
#module data
from get_covid_data import *
#app
from app import app


# -----------------
# Get data
today, total_data_df, today_data_df, overview_7days_df, city_data_df = get_vietnam_covid_data()
time_series_vn = get_vietnam_covid_19_time_series()
dff = city_data_df[['name', 'death', 'cases']]
dff = pd.melt(dff, id_vars=['name'], value_vars=['death', 'cases'], var_name='status', value_name='test')
#-----------------
# tab style
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

#-------------
#layout
layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Số ca nhiễm', children=[
            dcc.Graph(
                id='linechart1-s3',
                figure=px.line(
                    data_frame=time_series_vn,
                    x='Ngày',
                    y='Số ca nhiễm',
                    template='seaborn',
                    height=650,
                )
            )
        ], style=tab_style, selected_style=tab_selected_style,
        ),
        dcc.Tab(label='Tử vong', children=[
            dcc.Graph(
                id='linechart2-s3',
                figure=px.line(
                    data_frame=time_series_vn,
                    x='Ngày',
                    y='Tử vong',
                    template='seaborn',
                    height=650,
                )
            )
        ], style=tab_style, selected_style=tab_selected_style
        ),
        dcc.Tab(label='Vaccine', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ], style=tab_style, selected_style=tab_selected_style
        ),
    ]),
    #Datatable
    html.Div([
            dash_table.DataTable(
                id='datatable-s2',
                style_data_conditional=[                
                {
                    "if": {"state": "selected"},
                    "backgroundColor": "inherit !important",
                    "border": "inherit !important",
                }],  
                data=city_data_df.to_dict('records'),
                columns=[
                    {"name": 'Thành phố', "id": 'name',
                     "deletable": False, "selectable": False},
                    {"name": 'Số ca nhiễm', "id": 'cases',
                     "deletable": False, "selectable": False},
                    {"name": 'Tử vong', "id": 'death',
                     "deletable": False, "selectable": False},
                    {"name": 'Ca nhiếm mới hôm nay', "id": 'casesToday',
                     "deletable": False, "selectable": False},
                    # {"name": 'Đã tiêm vaccine', "id": 'people_vaccinated',
                    #  "deletable": False, "selectable": False},
                    # {"name": 'Cập nhật', "id": 'last_updated_date',
                    #  "deletable": False, "selectable": False},
                ],
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                row_selectable="single",
                row_deletable=False,
                style_table={'height': '350px'},
                fixed_rows={'headers': True, 'data': 0},
                virtualization=True,
            ),
            f"Cập nhật ngày {today}",
    ]),
    # horizontal bar chart
    html.Div(
        id ='horizontal-barchart-s3',
        children=[
            dcc.Graph(
            figure=px.bar(
                data_frame=dff,
                x='test',
                y='name',
                color='status',
                orientation='h',
                title='City Viet Nam'
            )
        )
        ],
        
    )
    
], id = "vietnam-page")
#-------------
