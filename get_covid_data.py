# This Python file uses the following encoding: utf-8
from numpy import NaN
import pandas as pd
import requests
from bs4 import BeautifulSoup

def map_world_data():
    df=pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv')
    dff=df[['iso_code','location','total_cases','people_fully_vaccinated_per_hundred']].copy().sort_values(by=['total_cases'],ascending=False)
    dff.reset_index(inplace=True)
    dff=dff.rename(columns = {'iso_code':'id','location':'Quốc gia','people_fully_vaccinated_per_hundred':'Tỉ lệ tiên vắc-xin','total_cases':'Số ca'}, inplace = False)
    dff.set_index('id', inplace=True, drop=False)
    totaldf=dff.loc[dff['id'].str.startswith('OWID')]
    dff = dff.drop(dff.loc[dff['id'].str.startswith('OWID')].index)
    return dff

def map_vn_data():
    df=pd.read_html('https://www.statista.com/statistics/1103568/vietnam-coronavirus-cases-by-region/')[0]
    vietnam_geojson = requests.get("https://data.opendevelopmentmekong.net/geoserver/ODMekong/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=ODMekong%3Aa4eb41a4-d806-4d20-b8aa-4835055a94c8&outputFormat=application%2Fjson").json()
    df.loc[df['Characteristic']=='Ho Chi Minh City','Characteristic']='TP. Ho Chi Minh'
    df.loc[df['Characteristic']=='Phu-Tho','Characteristic']='Phu Tho'
    df.loc[df['Characteristic']=='Thua Thien Hue','Characteristic']='Thua Thien - Hue'
    df.loc[df['Characteristic']=='Ben tre','Characteristic']='Ben Tre'
    df['id'] = df['Characteristic']
    df=df.rename(columns = {'Characteristic':'Tỉnh Thành','Number of cases':'Số ca'}, inplace = False)
    df.set_index('id', inplace=True, drop=False)
    return df,vietnam_geojson

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
    """
    response = requests.get(
        "https://vnexpress.net/microservice/sheet/type/vaccine_data_map")
    data_text = response.text
    buf = io.StringIO(data_text)
    df = pd.read_csv(buf, delimiter=",")

    return df


def get_vaccine_to_vietnam():
    """
        Return a dataframe Vaccine to Vietnam
    """
    response = requests.get(
        "https://vnexpress.net/microservice/sheet/type/vaccine_to_vietnam")
    data_text = response.text
    buf = io.StringIO(data_text)
    df = pd.read_csv(buf, delimiter=",")

    return df


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

    return df


def main():
    return


if __name__ == "__main__":
    main()
