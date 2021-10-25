import pandas as pd  # organize the data
import plotly.express as px
import dash
from dash import dash_table
from dash import dcc  # create interactive components
from dash import html  # access html tags
from dash.dependencies import Input, Output

#app
from app import app

# -----------------
#Handle the data
df=pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv')
dff=df[['iso_code','location','total_cases','people_fully_vaccinated_per_hundred']].copy().sort_values(by=['total_cases'],ascending=False)
dff.reset_index(inplace=True)
dff=dff.rename(columns = {'iso_code':'id','people_fully_vaccinated_per_hundred':'Vaccinated rate','total_cases':'Cases'}, inplace = False)
dff.set_index('id', inplace=True, drop=False)
totaldf=dff.loc[dff['id'].str.startswith('OWID')]
dff = dff.drop(dff.loc[dff['id'].str.startswith('OWID')].index)
# -----------------


#Map world layout
layout=html.Div([
    #Place to put the map
    html.Div(id="mapw"),
    #Place to put the table
    dash_table.DataTable(
        id='datatable-world',
        columns=[
            {'name': i, 'id': i, 'deletable': False} for i in dff.columns
            # omit the id column
            if i != 'id' and i!="index"
        ],
        data=dff.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=False,
        selected_rows=[],
        page_action='native',
        page_current= 0,
        page_size= 10,
        style_header={
                        'backgroundColor': '#CCE2CB',
                        'fontWeight': 'bold'
            },
        style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
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
                        color='Cases',
                        hover_data=['location','Cases','Vaccinated rate'],
                        color_continuous_scale="mint",
                        color_continuous_midpoint=1000000,
                        range_color=[0,50000000],
                        labels={'WORLD COVID-19 CASES MAP'},
                        template='plotly')
    return fig


# -------------------------------
    