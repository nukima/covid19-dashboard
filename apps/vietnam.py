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
#-----------------

layout = html.Div([
    dcc.Dropdown(id='linechart-dropdown-s3',
                         options=[
                             {'label': 'Từ trước đến nay',
                              'value': 'total_cases_per_million'},
                             {'label': '7 ngày gần đây',
                              'value': 'total_deaths_per_million'},
                         ],
                         value='total_cases_per_million',
                         multi=False,
                         clearable=False,
    ),
    dcc.Graph(
        id='linechart-s3',
    ),

    
])

#-------------
@app.callback(
    Output('linechart-s3', 'figure'),
    Input('linechart-dropdown-s3', 'value'),
)
def update_linechart(value):
    linechart = px.line(
            data_frame=time_series_vn,
            x='Ngày',
            y='Số ca',
            color='Chú thích',
            markers=True,
            template='seaborn',
            height=650,
        )
    return linechart