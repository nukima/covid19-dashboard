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
vietnam_vaccine_city = get_vaccine_data_vietnam_city()
#linechart1
linechart_data_1 = time_series_vn[['Ngày', 'Số ca nhiễm']]
linechart_data_1['MA50'] = linechart_data_1['Số ca nhiễm'].rolling(window=50).mean()
linechart_data_1['MA200'] = linechart_data_1['Số ca nhiễm'].rolling(window=200).mean()
linechart_data_1 = pd.melt(linechart_data_1, id_vars=['Ngày'], value_vars=['Số ca nhiễm', 'MA50', 'MA200'], var_name='Chú thích', value_name='Số ca')
#horizion data
dff = city_data_df[['name', 'death', 'cases']]
dff = pd.melt(dff, id_vars=['name'], value_vars=['death', 'cases'], var_name='status', value_name='test')
#-----------------
# tab style
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '2px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '2px solid #d6d6d6',
    'borderBottom': '2px solid #d6d6d6',
    'backgroundColor': '#056625',
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
                    data_frame=linechart_data_1,
                    x='Ngày',
                    y='Số ca',
                    color='Chú thích',
                    title='Số liệu thống kê',
                    template='ggplot2',
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
                    title='Số liệu thống kê',
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
    html.Div([
            dash_table.DataTable(
                id='datatable-s3',
                style_data_conditional=[                
                    {
                        "if": {"state": "selected"},
                        "backgroundColor": "inherit !important",
                        "border": "inherit !important",
                    },
                    {'if': {'column_id': 'fK'},
                    'width': '15%', 'textAlign': 'center'},
                    {'if': {'column_id': 'Tổng số dân trên 18 tuổi'},
                    'width': '17%', 'textAlign': 'center'},
                    {'if': {'column_id': 'Số người tiêm liều 1'},
                    'width': '17%', 'textAlign': 'center'},
                    {'if': {'column_id': 'Số người tiêm liều 2 '},
                    'width': '17%', 'textAlign': 'center'},
                    {'if': {'column_id': 'Tỷ lệ tiêm'},
                    'width': '17%', 'textAlign': 'center'},
                    {'if': {'column_id': 'Tỷ lệ tiêm đủ liều'},
                    'width': '17%', 'textAlign': 'center'},
                ],  
                data=vietnam_vaccine_city.to_dict('records'),
                columns=[
                    {"name": 'Thành phố', "id": 'fK',
                     "deletable": False, "selectable": False},
                    {"name": 'Dân số >= 18 tuổi', "id": 'Tổng số dân trên 18 tuổi',
                     "deletable": False, "selectable": False},
                    {"name": 'Đã tiêm liều 1', "id": 'Số người tiêm liều 1',
                     "deletable": False, "selectable": False},
                    {"name": 'Đã tiêm liều 2 ', "id": 'Số người tiêm liều 2 ',
                     "deletable": False, "selectable": False},
                    {"name": 'Tỷ lệ tiêm (%)', "id": 'Tỷ lệ tiêm',
                     "deletable": False, "selectable": False},
                    {"name": 'Tỷ lệ tiêm đủ liều (%)', "id": 'Tỷ lệ tiêm đủ liều',
                     "deletable": False, "selectable": False},
                ],
                page_action='none',
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                row_selectable="multi",
                row_deletable=False,
                style_table={'height': '650'},
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
                title='City Viet Nam',
                height= 650,
            ),
            
        )
        ],
        
    )])
    
], id = "vietnam-page")
#-------------
