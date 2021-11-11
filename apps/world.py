# dependencies 
import dash_html_components as html
from dash import dcc
import dash_table
from dash_table.Format import Format
from dash.dependencies import Input, Output
import plotly.express as px #plotly
import pandas as pd #pandas


from get_covid_data import get_world_covid_data #module data
from app import app #app
from .navbar import create_navbar #navbar


# -----------------
# Local object
# nav bar
nav = create_navbar()
world_data = get_world_covid_data()
# ---------------------

#-------------
#layout
layout = html.Div([
        nav,
        html.Div([
            dcc.Checklist(
                id='continent-checklist',
                options=[
                    {'label': 'Châu Á', 'value': 'Asia'},
                    {'label': 'Châu Âu', 'value': 'Europe'},
                    {'label': 'Châu Phi', 'value': 'Africa'},
                    {'label': 'Bắc Mỹ', 'value': 'North America'},
                    {'label': 'Nam Mỹ', 'value': 'South America'},
                    {'label': 'Châu Đại Dương', 'value': 'Oceania'},
                ],
                value=['Asia'],
                className='my_box_container',
                inputClassName='my_box_input',
                labelClassName='my_box_label'
            )
        ], id= "check-list-bar"),
        html.A("Nguồn: Our World in Data", href='https://github.com/owid/covid-19-data', target="_blank"),
        # Datatable
        html.Div([
            dash_table.DataTable(
                id='datatable-s2',
                style_data_conditional=[                
                    {
                        "if": {"state": "selected"},
                        "backgroundColor": "inherit !important",
                        "border": "inherit !important",
                    },
                    {'if': {'column_id': 'continent'},
                    'width': '10%', 'textAlign': 'center'},
                    {'if': {'column_id': 'location'},
                    'width': '18%', 'textAlign': 'center'},
                    {'if': {'column_id': 'total_cases'},
                    'width': '18%', 'textAlign': 'center'},
                    {'if': {'column_id': 'total_deaths'},
                    'width': '18%', 'textAlign': 'center'},
                    {'if': {'column_id': 'people_vaccinated'},
                    'width': '18%', 'textAlign': 'center'},
                    {'if': {'column_id': 'last_updated_date'},
                    'width': '18%', 'textAlign': 'center'},
                ],  
                columns=[
                    {"name": 'Châu lục', "id": 'continent',
                     "deletable": False, "selectable": False},
                    {"name": 'Quốc gia', "id": 'location',
                     "deletable": False, "selectable": False},
                    dict(id='total_cases', name='Số ca nhiễm', type='numeric', format=Format().group(True)) ,
                    dict(id='total_deaths', name='Tử vong', type='numeric', format=Format().group(True)) ,
                    dict(id='people_vaccinated', name='Đã tiêm vaccine', type='numeric', format=Format().group(True)) ,
                    {"name": 'Cập nhật', "id": 'last_updated_date',
                     "deletable": False, "selectable": False},
                ],
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                row_selectable="single",
                row_deletable=False,
                style_table={'height': '350px'},
                fixed_rows={'headers': True, 'data': 0},
                virtualization=True,
            )
        ]),
        html.Div([
            html.Div([
            dcc.Dropdown(id='bar-dropdown-s2',
                         options=[
                             {'label': 'Số ca nhiễm / triệu dân',
                              'value': 'total_cases_per_million'},
                             {'label': 'Ca tử vong / triệu dân',
                              'value': 'total_deaths_per_million'},
                             {'label': 'Đã tiêm vaccine (ít nhất 1 mũi) / triệu dân',
                              'value': 'people_vaccinated_per_hundred'},
                         ],
                         value='total_cases_per_million',
                         multi=False,
                         clearable=False
            ),
            dcc.Graph(id='barchart-s2')]),
            html.Div([
            html.Div(id='piechart-s2')
            ])
        ] , id= "chart-box"),

], className="main", id = "world-page")

#-------------------
#checklist -> datatable
@app.callback(
    Output('datatable-s2', 'data'),
    Input('continent-checklist', 'value')
)
def update_datatable(continent_selected):
    if not continent_selected:
        continent_selected = ['Asia']
    df_filtered = world_data[world_data['continent'].isin(continent_selected)]

    # table-data
    data = df_filtered[['location', 'continent', 'total_cases', 'total_deaths',
                        'last_updated_date', 'people_vaccinated']].to_dict('records') 

    return data  

# ---------------
#checklist(selected_row) -> barchart(highlight)
@app.callback(
    [
        Output('barchart-s2', 'figure')
    ],
    [   Input('continent-checklist', 'value'), 
        Input('datatable-s2', 'derived_virtual_data'),
        Input('bar-dropdown-s2', 'value'),
        Input('datatable-s2', 'derived_virtual_selected_rows'),
    ]
)
def update_barchart(continent_selected, all_rows_data, barchart_xaxis, slctd_row_indices,):
    if not continent_selected:
        continent_selected = ['Oceania']
    df_table = pd.DataFrame(all_rows_data)
    country_list = df_table['location']
    barchart_data = world_data[world_data['location'].isin(country_list)]
    barchart_data.index = [i for i in range(len(barchart_data))]
    barchart = px.bar(
        data_frame=barchart_data,
        y='location', 
        x=barchart_xaxis,
        orientation='h',
        labels={"location":"Quốc gia",
                "total_cases_per_million":"Số ca nhiễm / triệu dân",
                "people_vaccinated_per_hundred" : "Đã tiêm vaccine (ít nhất 1 mũi) / triệu dân",
                "total_deaths_per_million":"Ca tử vong / triệu dân"},
        width= 800,
        height = 750,
    )
    barchart.update_layout(yaxis={'categoryorder':'total ascending'})
    if slctd_row_indices != None:
        colors = ['#eb1e33' if i in slctd_row_indices else '#056625'
                for i in range(len(barchart_data))]
        barchart.update_traces(marker_color=colors)

    return (barchart, )
#datatable -> piechart country
@app.callback(
       Output('piechart-s2', 'children'),
    [   Input('datatable-s2', 'derived_virtual_data'),
        Input('datatable-s2', 'derived_virtual_selected_rows'),
    ]
)
def piechart_update(all_rows_data, slctd_row_indices,):
    dff = pd.DataFrame(all_rows_data)
    if not slctd_row_indices:
        value = html.P("Chọn một quốc gia trên bảng")
    else: 
    
        country_name = dff.iloc[slctd_row_indices[0]]['location']
        
        country_data = world_data[world_data['location'] == country_name][['location', 'population', 'people_fully_vaccinated', 'people_vaccinated']]
        country_data.index = [0]
        country_data['not_vaccinated'] = country_data['population'] - country_data['people_fully_vaccinated'] - country_data['people_vaccinated']
        country_data = country_data.T.reset_index()
        piechart_data = country_data[2:]
        if piechart_data.loc[2, 0] == None or piechart_data.loc[3, 0] == None or piechart_data.loc[4, 0] == None:
            value = "Chưa đủ số liệu"
        elif piechart_data.loc[2, 0] > 0 and piechart_data.loc[3, 0] > 0 and piechart_data.loc[4, 0] > 0:
            piechart_data.replace(to_replace="not_vaccinated", value="Chưa tiêm", inplace=True)
            piechart_data.replace(to_replace="people_fully_vaccinated", value="Đã tiêm hai mũi", inplace=True)
            piechart_data.replace(to_replace="people_vaccinated", value="Đã tiêm 1 mũi", inplace=True)
            piechart_data.rename(columns={"index": "Trạng thái", 0: "Số người"}, inplace=True)
            value = dcc.Graph(
                    figure = px.pie(
                                        data_frame= piechart_data, names='Trạng thái', values='Số người',
                                        color='Trạng thái',
                                        hole=0.3, title=f"Tình hình tiêm vaccine ở {country_name}",
                                        color_discrete_map={
                                            'Chưa tiêm':'#58b093',
                                            'Đã tiêm hai mũi':'#056625',
                                            'Đã tiêm 1 mũi':'#84e83c',
                                        },
                                        width=650,
                                        height = 750,
                                    ),
                    )
        else: value = "Chưa đủ số liệu"

    return value

# -------------------------------
