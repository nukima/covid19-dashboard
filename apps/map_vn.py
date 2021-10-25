import pandas as pd  # organize the data
import plotly.express as px
import requests
import dash
from dash import dash_table
from dash import dcc  # create interactive components
from dash import html  # access html tags
from dash.dependencies import Input, Output

#app
from app import app


# -----------------
#Handle the data
df=pd.read_html('https://www.statista.com/statistics/1103568/vietnam-coronavirus-cases-by-region/')[0]
vietnam_geojson = requests.get("https://data.opendevelopmentmekong.net/geoserver/ODMekong/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=ODMekong%3Aa4eb41a4-d806-4d20-b8aa-4835055a94c8&outputFormat=application%2Fjson").json()
df.loc[df['Characteristic']=='Ho Chi Minh City','Characteristic']='TP. Ho Chi Minh'
df.loc[df['Characteristic']=='Phu-Tho','Characteristic']='Phu Tho'
df.loc[df['Characteristic']=='Thua Thien Hue','Characteristic']='Thua Thien - Hue'
df.loc[df['Characteristic']=='Ben tre','Characteristic']='Ben Tre'
df['id'] = df['Characteristic']
df=df.rename(columns = {'Characteristic':'Tỉnh Thành','Number of cases':'Số ca'}, inplace = False)
df.set_index('id', inplace=True, drop=False)
# -----------------


layout=html.Div([
    html.Div(id="mapv"),
    dash_table.DataTable(
        id='datatable-vietnam',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in df.columns
            # omit the id column
            if i != 'id' and i!="index"
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        row_deletable=True,
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

@app.callback(
    Output('mapv', 'children'),
    [Input('datatable-vietnam', 'derived_virtual_data'),
    Input('datatable-vietnam', 'derived_virtual_selected_rows')]
)

def update_graphs(all_rows_data, slctd_row_indices):
    if slctd_row_indices is None:
        slctd_row_indices=[]
    dff2 = pd.DataFrame(all_rows_data)
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(df))]
    if "id" in dff2:
        return dcc.Graph(id='MVN',figure=map_vietnam(dff2).update_traces(marker_line_width=borders))
def map_vietnam(dff2):
    """Return a graph about number of covid-19 cases in Vietnam"""
    #Plot the graph
    fig=px.choropleth(data_frame=dff2,
                        geojson=vietnam_geojson,locations='Tỉnh Thành',featureidkey="properties.Name_EN",
                        # lat=10.762622,lon=106.660172,
                        color='Số ca',
                        hover_data=['Số ca'],
                        color_continuous_scale="mint",
                        scope="asia",
                        labels={'VIETNAM COVID-19 CASES MAP'},
                        template='plotly')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

#datatable highlight selected_row
@app.callback(
    Output('datatable-vietnam', 'style_data_conditional'),
    [Input('datatable-vietnam', 'derived_viewport_selected_rows'),]
)
def highlight_selectedRow(chosen_rows):
    style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                },
                {
                    'if': {'row_index': chosen_rows},
                    'backgroundColor': '#D4F0F0'
                },
            ]
    return style_data_conditional

if __name__ == '__main__':
    app.run_server(debug=True)