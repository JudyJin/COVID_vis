import altair as alt
import pandas as pd
import numpy as np


def clean_table_fillna(table):
    """
    Fill the NaN value with the previous possible value for certain columns
    
    Parameters: 
    table: vaccination table
    
    Returns: 
    a new vaccination table 
    """
    table[["total_vaccinations",
             "people_vaccinated",
             "people_fully_vaccinated",
             "total_vaccinations_per_hundred",
             "people_vaccinated_per_hundred",
             "people_fully_vaccinated_per_hundred"
            ]] = table[["total_vaccinations",
                              "people_vaccinated",
                              "people_fully_vaccinated",
                              "total_vaccinations_per_hundred",
                              "people_vaccinated_per_hundred",
                              "people_fully_vaccinated_per_hundred"]].fillna(method = "ffill")
    return table

def top10(table):
    """
    Extract the country and total vaccinations column, respectively
    Find the 10 countries with the most number of vaccinations
    
    Parameters: 
    table: vaccination table
    
    Returns: 
    a new vaccination table with top 10 countries
    """
    vaccination_selector = table[['country','total_vaccinations']]
    vaccination_selector = vaccination_selector.groupby('country').sum().reset_index()
    vaccination_data = vaccination_selector.sort_values(by=['total_vaccinations'],
                                                        ascending=False).head(10)
    return vaccination_data

def top10_detail(table):
    """
    Find the 10 countries with the most number of vaccinations as well 
    as their detailed information 
    
    Parameters: 
    table: vaccination table
    
    Returns: 
    a new vaccination table with top 10 countries and their details.
    """
    new_df = table.copy()
    new_df = new_df[['country','date','total_vaccinations']]
    new_df = new_df.fillna(0)
    new_df.head()
    new_df = new_df.groupby("country").agg({"total_vaccinations":"sum"}).reset_index()
    new_df = new_df.sort_values("total_vaccinations",ascending=False)
    countries = new_df.head(10)[['country']]
    # new_countries
    new_countries = [c[0] for c in countries.values.tolist()]
    vaccination_df = table[table['country'].isin(new_countries)]
    return vaccination_df

def geo_vac(country, vaccination):
    """
    Join country code and vaccination information
    
    Parameters: 
    country: country data
    vaccination: vaccination table
    
    Returns: 
    A new vaccination table with country code and 
    the specfic columns we need for follwing plotting.
    """
    
    # change alpha3 to capital letter
    country["alpha3"] = country["alpha3"].apply(lambda x: str.upper(x))
    # group by iso, find useful info
    vaccination = vaccination.groupby("iso_code").max()[["country",
                                                         "total_vaccinations",
                                                         "people_fully_vaccinated",
                                                         "total_vaccinations_per_hundred",
                                                         "people_fully_vaccinated_per_hundred",
                                                        "vaccines"]]
    country_vac = country.join(vaccination,on = "alpha3")
    country_vac = country_vac.fillna(0)
    return country_vac