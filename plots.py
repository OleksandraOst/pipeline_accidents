import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')

def _incident_causes_plot(df: pd.DataFrame, country: str) -> None:
    """
    This function save plots of pipeline accidents causes.
    Args:
        df: data frame
        country: country where accident happened
    Returns: 
        None
    """

    if country == 'Canada': 
        data_causes = df['What happened category']

    if country == 'USA': 
        data_causes = df['CAUSE']

    fig, ax = plt.subplots()
    data_causes.value_counts().sort_values().plot(ax=ax, kind='barh', colormap='coolwarm')
    plt.xlabel('Number of incidents')
    plt.title('Incident cuases in '+country)
    plt.savefig('CausesHist'+country+'.png',bbox_inches='tight', dpi = 300)
    plt.close()
    

    labels, counts = np.unique(data_causes, return_counts=True)
    plt.pie(counts, labels = labels,autopct='%1.1f%%')
    plt.title('Incident cuases in '+country)
    plt.savefig('CausesPiechart'+country+'.png',bbox_inches='tight', dpi = 300)
    plt.close()
     

def _incidents_over_years(df: pd.DataFrame, country: str) -> None:
    """
    This function save plots of pipeline accidents over time.
    Args:
        df: data frame
        country: country where accident happened
    Returns: 
        None
    """
    if country == 'Canada':
        df = df.sort_values(['Year'], ascending=True)
        labels, counts = np.unique(df['Year'], return_counts=True)
    if country == 'USA':
        df = df.sort_values(['IYEAR'], ascending=True)
        labels, counts = np.unique(df['IYEAR'], return_counts=True)
 
    plt.bar(labels,counts,color='royalblue')


    for i in range(len(counts)):
        plt.text(labels[i], counts[i], str(counts[i]),ha = 'center')

    plt.xlabel('Year')
    plt.ylabel('Number of incidents')
    plt.title('Incident over years in '+country)
    plt.savefig('OverYears'+country+'.png',bbox_inches='tight', dpi = 300)
    plt.close()


def _cause_incidents_over_years(df: pd.DataFrame, country: str) -> None:
    """
    This function save plots of accident causes over years.
    Args:
        df: data frame
        country: country where accident happened
    Returns: 
        None
    """
    if country == 'Canada':
        df = df.sort_values(['Year'], ascending=True)
        corrosion_df = df[df['What happened category'].str.contains('Corrosion and Cracking')]
        all_labels, all_counts = np.unique(df['Year'], return_counts=True)
        cor_labels, cor_counts = np.unique(corrosion_df['Year'], return_counts=True)
    if country == 'USA':
        df = df.sort_values(['IYEAR'], ascending=True)
        corrosion_df = df[df['CAUSE'].str.contains('CORROSION')]
        all_labels, all_counts = np.unique(df['IYEAR'], return_counts=True)
        cor_labels, cor_counts = np.unique(corrosion_df['IYEAR'], return_counts=True)


    plt.bar(all_labels,all_counts, label = 'All reasons',color='royalblue')
    plt.bar(cor_labels,cor_counts, label = 'Corrosion and Cracking')
    plt.xlabel('Year')
    plt.ylabel('Number of incidents')
    plt.legend()
    plt.title('Causes of incident over years in '+country)
    plt.savefig('CausesOverYears'+country+'.png',bbox_inches='tight', dpi = 300)
    plt.close()
    

def incident_location(df_canada: pd.DataFrame, df_usa: pd.DataFrame):
    """
    This function creates plot of accident locations in Canada and the USA.
    Args:
        df_canada: data frame with incidents which happened in Canada
        df_usa: data frame with incidents which happened in the USA
    Returns: 
        None
    """
    values_canada = df_canada['Released volume (m3)'].tolist()
    values_usa = df_usa['RELEASE M3'].tolist()

    color_canada = [float(val) for val in values_canada]
    color_usa = [float(val) for val in values_usa]

    colors = [float(val) for val in (values_canada+values_usa)]

    fig = px.scatter_geo(df_canada,  scope='north america', lat = 'Latitude', lon = 'Longitude',
                   hover_name = 'Released substance type', 
                   symbol_sequence = ['square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'triangle-left', 'triangle-right', 'triangle-ne', 'arrow-bar-right'],
                     symbol = 'Released substance type',
                    color=color_canada, range_color=(min(colors),max(colors)),
                    color_continuous_scale=px.colors.sequential.Plasma)

    
    fig2 = px.scatter_geo(df_usa,  scope='north america', lat = 'LOCATION_LATITUDE', lon = 'LOCATION_LONGITUDE',
                hover_name = 'COMMODITY_RELEASED_TYPE',  symbol = 'COMMODITY_RELEASED_TYPE',
                color=color_usa, range_color=(min(colors),max(colors)),
                color_continuous_scale=px.colors.sequential.Plasma)
   
    
    fig.add_trace(fig2.data[0])
    for i, frame in enumerate(fig.frames):
        fig.frames[i].data += (fig2.frames[i].data[0],)
    fig.update_layout(coloraxis_colorbar_x=0.85, coloraxis_colorbar_y=0.51)
    fig.layout.coloraxis.colorbar.title = 'Volume Released (m3)'
    fig.show()
    
def make_plots(df: pd.DataFrame, country:str):
    _incident_causes_plot(df, country)
    _incidents_over_years(df, country)
    _cause_incidents_over_years(df,country)
  

