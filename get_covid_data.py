# This Python file uses the following encoding: utf-8
import numpy as np
from numpy import NaN
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
import json

def map_world_data():
    url="https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases2_v1/FeatureServer/2/query?where=1%3D1&outFields=Country_Region,Confirmed,Deaths,Mortality_Rate,ISO3&returnGeometry=false&outSR=4326&f=json"
    rq=requests.get(url).text
    data=json.loads(rq)
    df=pd.json_normalize(data["features"])
    df.rename(columns={'attributes.Country_Region': 'Quốc gia', 'attributes.Confirmed': 'Số ca','attributes.Deaths':'Tử vong','attributes.Mortality_Rate':'Tỉ lệ tử vong','attributes.ISO3':'id'}, inplace=True)
    df['Tỉ lệ tử vong'] = df['Tỉ lệ tử vong'].map('{:,.2f}'.format)
    df.set_index('id', inplace=True, drop=False)
    dff=df.sort_values(by=['Số ca'],ascending=False)
    cases=dff['Số ca'].sum()
    deaths=dff['Tử vong'].sum() 
    return dff,cases,deaths

def map_vn_data():
    today, total_data_df, today_data_df, overview_7days_df, city_data_df=get_vietnam_covid_data()
    url="https://raw.githubusercontent.com/namnguyen215/dataset/main/vn_location.json"
    rq=requests.get(url).text
    data=json.loads(rq)
    vn_location=pd.json_normalize(data)
    df=city_data_df
    df.loc[df['name']=="Bà Rịa – Vũng Tàu","name"]="Bà Rịa - Vũng Tàu"
    dff=pd.merge(df,vn_location)
    nocases=[]
    for x in dff['cases']:
        if(x == 0):
            nocases.append(0)
        else:
            nocases.append(np.log2(x))
    cases=dff['cases'].sum()
    deaths=dff['death'].sum()    
    casesToday=dff['casesToday'].sum()
    dff.rename(columns={"name":"Tỉnh thành","cases":"Số ca","death":"Tử vong","casesToday":"Số ca hôm nay"}, inplace=True)
    return dff,nocases,cases,deaths,today,casesToday
    
def get_world_covid_data():
    """
    Return a dataframe of COVID data of 215 countries
    """
    # Source: Our World In Data: "https://github.com/owid/covid-19-data"
    data_requests = requests.get(
        'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.json')

    world_data = dict(data_requests.json())
    df = pd.DataFrame(world_data).T
    df = df[['location', 'continent', 'total_cases', 'total_deaths',
               'last_updated_date', 'people_vaccinated', 'total_cases_per_million', 'total_deaths_per_million', 'people_vaccinated_per_hundred', 'population', 'people_fully_vaccinated']]
    df.dropna(axis=0, thresh=6, inplace=True)
    return df


def get_vietnam_covid_data():
    """
        Return COVID data of VietNam, world:
            (str)today = today's date\n
            (df)total_data_df: 'death', 'treating', 'cases', 'recovered'  (today_data_df.internal['death'])\n
            (df)today_data_df: 'death', 'treating', 'cases', 'recovered'\n
            (df)overview_7days_df: 'date', 'death', 'treating', 'cases', 'recovered', 'avgCases7day', 'avgRecovered7day', 'avgDeath7day'\n
            (df)city_data_df: 'name','death', 'treating', 'cases', 'recovered', 'casesToday'
    """

    #Source: "https://covid19.gov.vn/"
    response = requests.get("https://static.pipezero.com/covid/data.json")
    vietnam_covid_data_dict = response.json()

    total_data_df = pd.DataFrame(vietnam_covid_data_dict['total'])
    today_data_df = pd.DataFrame(vietnam_covid_data_dict['today'])
    overview_7days_df = pd.DataFrame(vietnam_covid_data_dict['overview'])
    today = overview_7days_df.iloc[-1]['date']
    city_data_df = pd.DataFrame(vietnam_covid_data_dict['locations'])
    city_data_df = city_data_df[['name', 'cases', 'death', 'casesToday']]

    return today, total_data_df, today_data_df, overview_7days_df, city_data_df


def get_hanoi_covid_data():
    """
        Return a dataframe COVID data of Hanoi ('locations' - 'positive cases')
    """
    lst = []
    page = requests.get("https://covidmaps.hanoi.gov.vn/")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="list-statistic2")
    elements = results.find_all("div", class_="item-box")
    for element in elements:
        tmp = {}
        location = element.find("div", class_="title-region")
        numbers = element.find("div", class_="val-region")
        tmp["location"] = location.text.strip()
        tmp["positive"] = int(numbers.text.strip())
        lst.append(tmp)
    df = pd.DataFrame.from_records(lst)

    return df


def get_vaccine_data_vietnam_city():
    """
        Return a dataframe Vaccine data Vietnam city
        Source: "https://vnexpress.net/covid-19/vaccine"
    """
    response = requests.get(
        "https://vnexpress.net/microservice/sheet/type/vaccine_data_vietnam_city")
    data_text = response.text
    buf = io.StringIO(data_text)
    df = pd.read_csv(buf, delimiter=",")
    vietnam_vaccine_city = df[['fK', 'Tổng số dân trên 18 tuổi', 'Số người tiêm liều 1', 'Số người tiêm liều 2 ', 'Tỷ lệ tiêm', 'Tỷ lệ tiêm đủ liều']]

    vietnam_vaccine_city['Tỷ lệ tiêm'].replace(",", ".", inplace = True, regex = True)
    vietnam_vaccine_city['Tỷ lệ tiêm'] = pd.to_numeric(vietnam_vaccine_city['Tỷ lệ tiêm'])
    vietnam_vaccine_city['Tỷ lệ tiêm đủ liều'].replace(",", ".", inplace = True, regex = True)
    vietnam_vaccine_city['Tỷ lệ tiêm đủ liều'] = pd.to_numeric(vietnam_vaccine_city['Tỷ lệ tiêm đủ liều'])

    vietnam_vaccine_city['Tỷ lệ tiêm 1 mũi'] = vietnam_vaccine_city['Tỷ lệ tiêm'] - vietnam_vaccine_city['Tỷ lệ tiêm đủ liều']
    vietnam_vaccine_city['Tỷ lệ chưa tiêm'] = 100.0 - vietnam_vaccine_city['Tỷ lệ tiêm']
    return vietnam_vaccine_city




def get_vaccine_data_vietnam():
    """
        Return a dataframe Vaccine to Vietnam
        df.loc[df["Ngày"][:] == "9/10"]
    """
    response = requests.get(
        "https://vnexpress.net/microservice/sheet/type/vaccine_data_vietnam")
    data_text = response.text
    buf = io.StringIO(data_text)
    df = pd.read_csv(buf, delimiter=",")
    vaccine_data_vietnam = df[['Ngày', 'Tổng số người đã tiêm']]
    vaccine_data_vietnam.dropna(axis=0, thresh=2, inplace=True)
    date = pd.date_range("2021-03-07", periods=len(vaccine_data_vietnam), freq="D")
    vaccine_data_vietnam['Thời gian'] = date
    return vaccine_data_vietnam

def get_vietnam_covid_19_time_series():
    '''
        Return a dataframe. Confirmed and Deaths of Vietnam from 22/1/2020
        Source: "https://github.com/CSSEGISandData/COVID-19"
    '''
    today, total_data_df, today_data_df, overview_7days_df, city_data_df = get_vietnam_covid_data()
    # confirmed 
    response = requests.get(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    data_text = response.text
    buf = io.StringIO(data_text)
    df = pd.read_csv(buf, delimiter=",")
    time_series_confirmed_vn = df.iloc[275][4:]
    #deaths
    response = requests.get(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
    data_text = response.text
    buf = io.StringIO(data_text)
    df = pd.read_csv(buf, delimiter=",")
    time_series_deaths_vn = df.iloc[275][4:]
    #merge two series

    time_series_vn = pd.DataFrame(data=[], index=[])
    date = pd.Series(time_series_confirmed_vn.index, name='Ngày')
    date = pd.to_datetime(date)
    time_series_vn['Ngày'] = date.array
    time_series_vn['Số ca nhiễm'] = time_series_confirmed_vn.array
    time_series_vn['Tử vong'] = time_series_deaths_vn.array

    return time_series_vn



if __name__ == "__main__":
    msg = 'hello'