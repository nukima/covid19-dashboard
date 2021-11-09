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
#navbar
from .navbar import create_navbar

nav = create_navbar()

# -----------------
# Get data
today, total_data_df, today_data_df, overview_7days_df, city_data_df = get_vietnam_covid_data()
time_series_vn = get_vietnam_covid_19_time_series()
vietnam_vaccine_city = get_vaccine_data_vietnam_city()
vaccine_data_vietnam = get_vaccine_data_vietnam()
#linechart1-data
linechart_data_1 = time_series_vn[['Ngày', 'Số ca nhiễm']]
linechart_data_1['MA50'] = linechart_data_1['Số ca nhiễm'].rolling(window=50).mean()
linechart_data_1['MA200'] = linechart_data_1['Số ca nhiễm'].rolling(window=200).mean()
linechart_data_1 = pd.melt(linechart_data_1, id_vars=['Ngày'], value_vars=['Số ca nhiễm', 'MA50', 'MA200'], var_name='Chú thích', value_name='Số ca')
#linechart2-data
linechart_data_2 = time_series_vn[['Ngày', 'Tử vong']]
linechart_data_2['MA50'] = linechart_data_2['Tử vong'].rolling(window=50).mean()
linechart_data_2['MA200'] = linechart_data_2['Tử vong'].rolling(window=200).mean()
linechart_data_2 = pd.melt(linechart_data_2, id_vars=['Ngày'], value_vars=['Tử vong', 'MA50', 'MA200'], var_name='Chú thích', value_name='Số ca')
#linechart3-data
vaccine_data_vietnam['MA50'] = vaccine_data_vietnam['Tổng số người đã tiêm'].rolling(window=50).mean()
vaccine_data_vietnam['MA100'] = vaccine_data_vietnam['Tổng số người đã tiêm'].rolling(window=100).mean()
vaccine_data_vietnam = pd.melt(vaccine_data_vietnam, id_vars=['Thời gian'], value_vars=['Tổng số người đã tiêm', 'MA50', 'MA100'], var_name='Chú thích', value_name='Số người')

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
    nav,
    dcc.Tabs([
        #linechart so ca nhiem
        dcc.Tab(label='Số ca nhiễm', children=[
            dcc.Graph(
                id='linechart1-s3',
                figure=px.line(
                    data_frame=linechart_data_1,
                    x='Ngày',
                    y='Số ca',
                    color='Chú thích',
                    color_discrete_map={
                        'MA200':'#147082',
                        'Số ca nhiễm':'#095422',
                        'MA50':'#84e83c',
                    },
                    title='Số liệu thống kê',
                )
            ),
            html.A("Nguồn: JHU CSSE COVID-19 Data", href='https://github.com/CSSEGISandData/COVID-19', target="_blank"),
        ], style=tab_style, selected_style=tab_selected_style,
        ),
        #linechart so ca tu vong
        dcc.Tab(label='Tử vong', children=[
            dcc.Graph(
                id='linechart2-s3',
                figure=px.line(
                    data_frame=linechart_data_2,
                    x='Ngày',
                    y='Số ca',
                    color='Chú thích',
                    color_discrete_map={
                        'MA200':'#147082',
                        'Tử vong':'#095422',
                        'MA50':'#84e83c',
                    },
                    title='Số liệu thống kê',
                )
            ),
            html.A("Nguồn: JHU CSSE COVID-19 Data", href='https://github.com/CSSEGISandData/COVID-19', target="_blank"),
        ], style=tab_style, selected_style=tab_selected_style
        ),
        #linechart vaccine
        dcc.Tab(label='Vaccine', children=[
            dcc.Graph(
                id='linechart3-s3',
                figure=px.line(
                    data_frame=vaccine_data_vietnam,
                    x='Thời gian',
                    y='Số người',
                    color='Chú thích',
                    color_discrete_map={
                        'MA100':'#147082',
                        'Tổng số người đã tiêm':'#095422',
                        'MA50':'#84e83c',
                    },
                    title='Số liệu thống kê',
                )
            ),
            html.A("Nguồn: Bộ Y Tế", href='https://vnexpress.net/covid-19/vaccine', target="_blank"),
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
            html.A("Nguồn: Bộ Y tế", href='https://vnexpress.net/covid-19/vaccine', target="_blank"),
    ]),
    # horizontal bar chart
    html.Div(
        id ='horizontal-barchart-s3',
        children=[],        
    )])
    
], id = "vietnam-page")
#-------------
#callback
@app.callback(
    Output('horizontal-barchart-s3', 'children'),
    [   
        Input('datatable-s3', 'derived_virtual_data'),
        Input('datatable-s3', 'derived_virtual_selected_rows'),
    ]
)
def update_horizontal_barchart(all_rows_data, slctd_row_indices,):
    dff = pd.DataFrame(all_rows_data)
    if not slctd_row_indices:
        slctd_row_indices = dff.index 
    
    city_name = dff.iloc[slctd_row_indices, :]['fK']
    h_barchart_data = vietnam_vaccine_city[vietnam_vaccine_city['fK'].isin(city_name)][['fK','Tỷ lệ tiêm đủ liều', 'Tỷ lệ chưa tiêm', 'Tỷ lệ tiêm 1 mũi']]
    h_barchart_data = pd.melt(h_barchart_data, id_vars=['fK'], value_vars=['Tỷ lệ tiêm đủ liều', 'Tỷ lệ tiêm 1 mũi','Tỷ lệ chưa tiêm' ], var_name='Chú thích', value_name='Tỷ lệ %')
    return dcc.Graph(
            figure=px.bar(
                data_frame=h_barchart_data,
                x='Tỷ lệ %',
                y='fK',
                color='Chú thích',
                color_discrete_map={
                    'Tỷ lệ chưa tiêm':'#147082',
                    'Tỷ lệ tiêm đủ liều':'#095422',
                    'Tỷ lệ tiêm 1 mũi':'#84e83c',
                },
                orientation='h',
                title='Tình trạng tiêm vaccine của các tỉnh/thành phố trong bảng bên',
                labels={'fK':'Tỉnh/Thành phố'},
                height= 650,
                ),            
            )

    

