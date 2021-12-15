import altair as alt
import pandas as pd
import numpy as np
from vega_datasets import data

def plot1_line_graph(table, height = 400, width = 600, country = None):
    """
    Plot line graph for COVID-19 vaccination process. Global or by country.
    
    Parameters: 
    table: vaccination table
    height: the desired graph height
    width: the desired graph height
    country: the specific country to plot. Default = None, to plot global data.
    
    Returns: 
    A line graph with COVID-19 vaccination process
    """
    if country != None:
        country_table = table[table["country"]==country]
        output = alt.Chart(
            country_table,
            title = 'Number of total vaccinations in ' + country
        ).mark_line().encode(
            x='date:O',
            y=alt.Y('total_vaccinations:Q',title = "Total Vaccinations"),
            tooltip=[alt.Tooltip('date:O', title='Date'),
                     alt.Tooltip('country:N', title='Country'),
                     alt.Tooltip('total_vaccinations:Q', title='Total Vaccinations')]
        ).properties(
            height = height,
            width = width)
        return output
        
    all_country = table["country"].unique()
    input_dropdown = alt.binding_select(options = all_country, name = "Country: ")
    selection = alt.selection_single(fields=['country'],bind = input_dropdown)
    colors = alt.condition(selection,
                        alt.Color('country:N'),
                        alt.value('lightgray'))

    output = alt.Chart(table,
             title = 'Number of total vaccinations in each country'
             ).mark_line().encode(
        x='date:O',
        y=alt.Y('total_vaccinations:Q',title = "Total Vaccinations"),
        color=colors,
        tooltip=[alt.Tooltip('date:O', title='Date'),
                 alt.Tooltip('country:N', title='Country'),
                 alt.Tooltip('total_vaccinations:Q', title='Total Vaccinations')
        ]
    ).properties(
        height = height,
        width = width
    ).add_selection(
        selection
    ).interactive()
    
    return output
    
    
def plot2_barchart_top10(table):
    """
    Plot bar chart for top 10 countries of COVID-19 vaccination.
    
    Parameters: 
    table: vaccination table with data for top 10 country
    
    Returns: 
    A bar chart for top 10 countries of COVID-19 vaccination.
    """
    selBarCur = alt.selection_multi(name='selBarLegend',fields=['total_vaccinations'],bind='legend')
    hoverSel = alt.selection(name='hoverSel',type='single', nearest=True, 
                             on='mouseover',fields=['total_vaccinations'],empty='none')

    color = alt.Color('country:N',scale=alt.Scale(
        domain=list(table['country']),
        range=['#d62728','#9467bd','#e377c2','#ff7f0e','#1f77b4',
               '#8c564b','#17becf','#FF6666','#c49c94','#9edae5',
              '#c5b0d5','#dbbb88','#ff9896','#7f7f7f','#98df8a',
               '#2ca02c','#ffbb78','#bcbd22','#aec7e8','#f7b6d2']),
                      legend=alt.Legend(title='country',
                                        titleFontSize=12,
                                        titleOpacity=0.5,
                                        titlePadding=20,
                                        labelFontSize=15,
                                        rowPadding=5,
                                        labelOpacity=0.8,
                                        offset=150,orient='right'))

    bar = alt.Chart(table).mark_bar().encode(
        y=alt.X('total_vaccinations',axis=alt.Axis(title='Total Vaccinations')),
        x=alt.Y('country:N',sort=list(table),axis=alt.Axis(title='Country')),
        color='country',
        tooltip=['total_vaccinations']
    ).properties(
        width=600,
        title={
        "text": "COVID-19 Bar chart of the number of vaccinations of the top 10 countries overseas",
        "fontSize": 12,
        'offset':16
      }
    )

    return bar


def plot2_b_trend_line(table):
    """
    Plot trending line for top 10 countries of COVID-19 vaccination.
    
    Parameters: 
    table: vaccination table with data for top 10 country
    
    Returns: 
    A trending line for top 10 countries of COVID-19 vaccination.
    """
    
    trend_line = alt.Chart(table).mark_circle(
        opacity=0.8,
        stroke='black',
        strokeWidth=1
    ).encode(
        alt.X('date:O', axis=alt.Axis(labelAngle=0,title='Date',titleFontSize=16,titlePadding=20,grid=True,labelFontSize=14)),
        alt.Y('country:N',axis=alt.Axis(title='Country',titleFontSize=16,titleColor='#FF9988',titlePadding=20)),
        alt.Size('total_vaccinations:Q',
                 scale=alt.Scale(range=[0, 4000]),
                 legend=alt.Legend(title='Global total vaccination')
                ),
        alt.Color('country:N', legend=None)
    ).properties(
        width=1000,
        height=600,
        title= {
            "text": "COVID-19 trend line chart of the total number of vaccinations of the top 10 countries",
            "fontSize": 12,
            'offset':16
        }
    )
    return trend_line

def plot2_c_stacked_barh(table):
    """
    Plot stacked barh chart for top 10 countries of COVID-19 vaccination.
    
    Parameters: 
    table: vaccination table with data for top 10 country
    
    Returns: 
    A stacked barh chart for top 10 countries of COVID-19 vaccination.
    """
        
    stacked_barh = alt.Chart(table).mark_bar().encode(
        x=alt.X('sum(total_vaccinations)', 
                axis=alt.Axis(title='Global total vaccinations',
                              titleFontSize=16,titlePadding=20,grid=True,labelFontSize=14)),
        y=alt.Y('country',
                axis=alt.Axis(title='Country',
                              titleFontSize=16,titleColor='#FF9988',titlePadding=20)),
        color='date',
        order=alt.Order(
          # Sort the segments of the bars by this field
          'date',
          sort='ascending'
        )
    ).properties(
        width=800,
        height=600,
        title= {
            "text": "COVID-19 stacked bar chart of the total number of vaccinations of the top 10 countries",
            "fontSize": 12,
            'offset':16
        }
    )
    return stacked_barh


def plot3_geo_per100(table, column):
    """
    Plot a geographic graph showing key vaccination features for all the countries.
    
    Parameters: 
    table: vaccination table with country info as well as total_vaccinations, people_fully_vaccinated, 
            total_vaccinations_per_hundred, people_fully_vaccinated_per_hundred, vaccines
    column: the specific column that want to visualize on (total_vaccinations, people_fully_vaccinated, 
            total_vaccinations_per_hundred, people_fully_vaccinated_per_hundred)
    
    Returns: 
    A geographic graph showing key vaccination features as specified in the column parameter.
    """

    source = alt.topo_feature(data.world_110m.url, 'countries')
    geo = alt.Chart(source).mark_geoshape(
        stroke='black'
    ).encode(
        tooltip=[alt.Tooltip('name:O', title='country'),
                 alt.Tooltip(column+":Q", title = " ".join(column.split("_")))],
        color=alt.Color(column+":O",legend = None)
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(table, 'id', [column,'name'])
    ).project(
        'equirectangular'
    ).properties(
        width=600,
        height=400,
        title= {
            "text": "COVID-19 " + " ".join(column.split("_")),
            "fontSize": 14,
            'offset':10
        }
    )
    return geo


def plot4_compare_scatter(table):
    """
    Plot a scatter plot showing relationship between COVID19 comfirmed cases and the vaccination state.
    
    Parameters: 
    table: vaccination table with country info as well as comfirmed cases info
    
    Returns: 
    A scatter plot showing relationship between COVID19 comfirmed cases and the vaccination state.
    """
    scatter = alt.Chart(table).mark_point().encode(
        x = alt.X("Confirmed:Q", 
                axis=alt.Axis(title='Total Confirmed Cases',
                              titleFontSize=16,titlePadding=20,grid=True,labelFontSize=14)),
        y =alt.Y("total_vaccinations:Q", 
                axis=alt.Axis(title="Total Vaccinations",
                              titleFontSize=16,titlePadding=20,grid=True,labelFontSize=14)),
        size = alt.Size('people_fully_vaccinated_per_hundred:Q',
                 legend=alt.Legend(title='people fully vaccinated per hundred')
                ),
        tooltip = [alt.Tooltip('name:O', title='Country'),
               alt.Tooltip('Confirmed:O', title='Total confirmed cases'),
               alt.Tooltip("people_fully_vaccinated_per_hundred:Q", title = "people fully vaccinated per hundred"),
               alt.Tooltip("total_vaccinations:Q", title = "total vaccination"),
               "vaccines"]    
    ).properties(
        width=600,
        title={
        "text": "COVID-19 Total Vaccinations vs. Total Confirmed Cases",
        "fontSize": 16,
        'offset':16
        }
    ).interactive()
    return scatter