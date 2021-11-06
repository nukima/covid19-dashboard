# import dash
from dash.html.Br import Br
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
world_data = get_world_covid_data()
# ---------------------

#world layout
layout = html.Div([
    # World Section 
    # html.Div([
        # dropdown continent
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
        # Datatable
        html.Div([
            dash_table.DataTable(
                id='datatable-s2',
                style_data_conditional=[                
                {
                    "if": {"state": "selected"},
                    "backgroundColor": "inherit !important",
                    "border": "inherit !important",
                }],  
                # data=[{}],
                columns=[
                    {"name": 'Châu lục', "id": 'continent',
                     "deletable": False, "selectable": False},
                    {"name": 'Quốc gia', "id": 'location',
                     "deletable": False, "selectable": False},
                    {"name": 'Số ca nhiễm', "id": 'total_cases',
                     "deletable": False, "selectable": False},
                    {"name": 'Tử vong', "id": 'total_deaths',
                     "deletable": False, "selectable": False},
                    {"name": 'Đã tiêm vaccine', "id": 'people_vaccinated',
                     "deletable": False, "selectable": False},
                    {"name": 'Cập nhật', "id": 'last_updated_date',
                     "deletable": False, "selectable": False},
                ],
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                row_selectable="single",
                row_deletable=False,
                style_table={'height': '350px'},
                # page_action="native",
                # page_current=0,
                # page_size=7,
                fixed_rows={'headers': True, 'data': 0},
                virtualization=True,
                # style_cell={'textAlign': 'left'},
                # style_cell_conditional=[
                #     {'if': {'column_id': 'location'},
                #      'width': '10%', 'textAlign': 'center'},
                #     {'if': {'column_id': 'continent'},
                #      'width': '5%', 'textAlign': 'center'},
                #     {'if': {'column_id': 'total_cases'},
                #      'width': '25%', 'textAlign': 'center'},
                #     {'if': {'column_id': 'total_deaths'},
                #      'width': '25%', 'textAlign': 'center'},
                #     {'if': {'column_id': 'last_updated_date'},
                #      'width': '10%', 'textAlign': 'center'},
                #     {'if': {'column_id': 'people_vaccinated'},
                #      'width': '25%', 'textAlign': 'center'},
                # ],
                # style_header={
                #     'backgroundColor': '#CCE2CB',
                #     'color': 'black',
                #     'fontWeight': 'bold'
                # }
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
            # dcc.Graph(id='barchart-s2'),
            # html.Div(id='piechart-s2'),
        ] , id= "chart-box"),

    # ])

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
        template='seaborn',
        width= 500
    )
    barchart.update_layout(yaxis={'categoryorder':'total ascending'})
    if slctd_row_indices != None:
        colors = ['#FF0000' if i in slctd_row_indices else '#0074D9'
                for i in range(len(barchart_data))]
        barchart.update_traces(marker_color=colors)

    return (barchart, )
#datatable highlight selected_row -> piechart country
@app.callback(
    # [   Output('datatable-s2', 'style_data_conditional'), 
       Output('piechart-s2', 'children'),
    # [   Input('datatable-s2', 'derived_viewport_selected_rows'),
    [   Input('datatable-s2', 'derived_virtual_data'),
        Input('datatable-s2', 'derived_virtual_selected_rows'),
    ]
)
def highlight_selectedRow(all_rows_data, slctd_row_indices,):
#     #highlight selected row datatable
    # if chosen_rows != None:
        # style_data_conditional=[
        #         {
        #             'if': {'row_index': 'odd'},
        #             'backgroundColor': 'rgb(220, 220, 220)',
        #         },
        #         {
        #             'if': {'row_index': chosen_rows},
        #             'backgroundColor': '#D4F0F0'
        #         },
        #     ]
    # else:
        # style_data_conditional=[
        #         {
        #             'if': {'row_index': 'odd'},
        #             'backgroundColor': 'rgb(220, 220, 220)',
        #         },
        #     ]
    #---------------
    #piechart
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
            piechart_data.replace(to_replace="not_vaccinated", value="Chưa tiêm vaccine", inplace=True)
            piechart_data.replace(to_replace="people_fully_vaccinated", value="Đã tiêm hai mũi", inplace=True)
            piechart_data.replace(to_replace="people_vaccinated", value="Đã tiêm 1 mũi vaccine", inplace=True)
            piechart_data.rename(columns={"index": "Trạng thái", 0: "Số người"}, inplace=True)
            value = dcc.Graph(
                    figure = px.pie(
                                    data_frame= piechart_data, names='Trạng thái', values='Số người',
                                    hole=0.3, title=f"Tình trạng tiêm vaccine ở {country_name}", template='seaborn'
                                    ),
                    style={'width': '500px'})
        else: value = "Chưa đủ số liệu"

    return value

# -------------------------------
