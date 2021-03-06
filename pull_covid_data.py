import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import sys

current_date = datetime.now().date()

# read in latest covid data
covid_data = pd.read_csv('covid_19_data.csv')
covid_data['Confirmed'] = (covid_data['Confirmed']).astype(int)


# temp explicit subsets
covid_us = covid_data.where(covid_data['Country/Region']=='US')
covid_china = covid_data.where(covid_data['Country/Region']=='Mainland China')
covid_italy = covid_data.where(covid_data['Country/Region']=='Italy')
covid_s_korea = covid_data.where(covid_data['Country/Region']=='South Korea')
covid_germany = covid_data.where(covid_data['Country/Region']=='Germany')
covid_iran = covid_data.where(covid_data['Country/Region']=='Iran')
covid_spain = covid_data.where(covid_data['Country/Region']=='Spain')
covid_france = covid_data.where(covid_data['Country/Region']=='France')
covid_swiss = covid_data.where(covid_data['Country/Region']=='Switzerland')
covid_uk = covid_data.where(covid_data['Country/Region']=='UK')

# Create array of all countries in data
cntry_array = covid_data["Country/Region"].unique()
#TODO: For every country in array, compute average daily percent change in cases, then plot top 10 by Avg Daily % Chg

def group_daily(df):
    daily = df.groupby(['ObservationDate'], as_index=False).agg({"Confirmed": "sum", "Deaths": "sum", "Recovered": "sum"})
    daily_confirmed = df.groupby(['ObservationDate']).agg({"Confirmed": "sum"})

    return daily, daily_confirmed

#TODO: dynamically assign DF names for each country
daily_overall, daily_confirmed_overall = group_daily(covid_data)
daily_us, daily_confirmed_us = group_daily(covid_us)
daily_china, daily_confirmed_china = group_daily(covid_china)
daily_italy, daily_confirmed_italy = group_daily(covid_italy)
daily_s_korea, daily_confirmed_s_korea = group_daily(covid_s_korea)
daily_germany, daily_confirmed_germany = group_daily(covid_germany)
daily_iran, daily_confirmed_iran= group_daily(covid_iran)
daily_france, daily_confirmed_france = group_daily(covid_france)
daily_spain, daily_confirmed_spain = group_daily(covid_spain)
daily_swiss, daily_confirmed_swiss = group_daily(covid_swiss)
daily_uk, daily_confirmed_uk = group_daily(covid_uk)

# Avg Daily Case growth globally and by country
def daily_percent_change(df):

    case_pct_change = df.pct_change()
    case_pct_change['Confirmed_Perc_Chg'] = case_pct_change['Confirmed'].astype(float).map("{:.2%}".format)

    return case_pct_change

global_case_pct_change = daily_percent_change(daily_confirmed_overall)
global_case_pct_change['Country']='Global'
us_case_pct_change = daily_percent_change(daily_confirmed_us)
us_case_pct_change['Country']='US'
china_case_pct_change = daily_percent_change(daily_confirmed_china)
china_case_pct_change['Country']='Mainland China'
italy_case_pct_change = daily_percent_change(daily_confirmed_italy)
italy_case_pct_change['Country']='Italy'
s_korea_case_pct_change = daily_percent_change(daily_confirmed_s_korea)
s_korea_case_pct_change['Country']='South Korea'

germany_case_pct_change = daily_percent_change(daily_confirmed_germany)
germany_case_pct_change['Country']='Germany'

iran_case_pct_change = daily_percent_change(daily_confirmed_iran)
iran_case_pct_change['Country']='Iran'

france_case_pct_change = daily_percent_change(daily_confirmed_france)
france_case_pct_change['Country']='France'

spain_case_pct_change = daily_percent_change(daily_confirmed_spain)
spain_case_pct_change['Country']='Spain'

swiss_case_pct_change = daily_percent_change(daily_confirmed_swiss)
swiss_case_pct_change['Country']='Switzerland'

uk_case_pct_change = daily_percent_change(daily_confirmed_uk)
uk_case_pct_change['Country']='UK'


# Stack all percent change data
pdList = [global_case_pct_change, us_case_pct_change, china_case_pct_change, italy_case_pct_change, s_korea_case_pct_change, 
germany_case_pct_change, iran_case_pct_change,france_case_pct_change,spain_case_pct_change,swiss_case_pct_change, uk_case_pct_change]
perc_chg_stacked = pd.concat(pdList)

perc_chg_avg = perc_chg_stacked.groupby('Country')['Confirmed'].mean()
print(perc_chg_avg.head(20))
#def avg_daily_perc_chg(df):

perc_chg_stacked.to_csv('perc_chg_stacked.csv')

# Compute Daily Deaths and Daily Cases for Country/State
covid_data2 = covid_data
covid_data2.set_index(['Country/Region','Province/State','ObservationDate'], inplace=True)
covid_data2.sort_index(inplace=True)
covid_data2['DailyDeaths'] = np.nan
covid_data2['DailyConfirmed'] = np.nan 

for idx in covid_data2.index.levels[0]:
    covid_data2.DailyDeaths[idx] = covid_data2.Deaths[idx].diff()
    covid_data2.DailyConfirmed[idx] = covid_data2.Confirmed[idx].diff()

covid_data2.to_csv('covid_19_data_rev.csv')


sys.exit()



def plot_perc_chg_bars(df, country):

    fig = px.bar(df, x=df.index, y= 'Confirmed_Perc_Chg', text="Confirmed_Perc_Chg")

    fig.update_layout(
        title="{0} Daily % Change in Confirmed Cases".format(country),

        xaxis_title="Date",
        yaxis_title="% Change",
        font=dict(
            size=15,
        )
    )

    fig.show()

plot_perc_chg_bars(global_case_pct_change, "Global")
plot_perc_chg_bars(us_case_pct_change, "US")
plot_perc_chg_bars(china_case_pct_change, "China")
plot_perc_chg_bars(italy_case_pct_change, "Italy")
plot_perc_chg_bars(s_korea_case_pct_change, "South Korea")


#TODO average daily case growth for all countries

def plot_time_series(df, title):
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
                    x=df.ObservationDate,
                    y=df['Confirmed'],
                    name="Confirmed",
                    line=dict(
                        color="deepskyblue",
                        width=5
                    ),
                    opacity=0.8))

    fig2.add_trace(go.Scatter(
                    x=df.ObservationDate,
                    y=df['Deaths'],
                    name="Deaths",
                    line=dict(
                        color="darkred",
                        width=5
                    ),
                    opacity=0.8))

    fig2.add_trace(go.Scatter(
                    x=df.ObservationDate,
                    y=df['Recovered'],
                    name="Recovered",
                    line=dict(
                        color="lightgreen",
                        width=5
                    ),
                    opacity=0.8))

    fig2.update_layout(title_text=title)
    fig2.show()

plot_time_series(daily_overall, "Global COVID-19 Data")
plot_time_series(daily_us, "US COVID-19 Data")
plot_time_series(daily_china, "China COVID-19 Data")
plot_time_series(daily_italy, "Italy COVID-19 Data")
plot_time_series(daily_s_korea, "South Korea COVID-19 Data")