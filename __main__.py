import extractor 
import transformer
import loader
import plots
import calc_and_stats




def data_process_canada(file_name_canada_list: list, new_df_name: str) -> None:
    """
    This function processes Canadian data set. Also, it saves .csv file ready for further analysis.
    Args:
        file_name_canada_list: list of .csv files
        new_df_name: name of output .csv file
    Returns: 
        None
    """

    df_canada = extractor.extract_df(file_name_canada_list, 'Canada', 'preprocess')
    # print(df_canada.columns.tolist()) #print column headers and then choose which needed
    columns_canada = [ 'Released substance type','Released volume (m3)', 'Substance carried', 'Latitude', 'Longitude' , 'Year',  'What happened category']
    clean_df_canada = transformer.necessary_columns(df_canada,columns_canada)
    substance_carried_df = transformer.keep_values(clean_df_canada, column_name = 'Substance carried', value = 'Crude Oil', mode = 'keep') #keep incidents only when carried substance is crude oil

    relabled_df = substance_carried_df
    #Relabel columns which contain multiple causes of the incident
    values_list = ['Corrosion','Defect and Deterioration']
    new_labels_list = ['Corrosion and Cracking', 'Defect and Deterioration']
    for value, label in zip(values_list,new_labels_list):
        relabled_df = transformer.relabel(relabled_df,'What happened category',value,label) 

    loader.load(relabled_df,'data/final_df_canada.csv')

def data_process_usa(file_name_usa_list: list, new_df_name: str, before_year: str) -> None:
    """
    This function processes the USA data set. Also, it saves .csv file ready for further analysis.
    Args:
        file_name_usa_list: list of .csv files
        new_df_name: name of output .csv file
        before_year: 
    Returns: 
        None
    """
    df_usa = extractor.extract_df(file_name_usa_list, 'USA', 'preprocess')
    # print(df_usa.columns.tolist()) #print column headers and then choose which needed

    if before_year == '2002':
        usa_2002 = ['IDATE','COMM','LOSS']
        clean_df_usa = transformer.necessary_columns(df_usa,usa_2002)
        substance_carried_df = transformer.keep_values(clean_df_usa, column_name = 'COMM', value = 'CRUDE OIL', mode = 'keep') 
        substance_carried_df['IDATE'] =  substance_carried_df['IDATE'].apply(lambda val: str(val)[:4])
        final_df = substance_carried_df

    if before_year == '2010':
        usa_2010 = ['IYEAR','COMM','LOSS','LATITUDE','LONGITUDE']
        clean_df_usa = transformer.necessary_columns(df_usa,usa_2010)
        final_df = transformer.keep_values(clean_df_usa, column_name = 'COMM', value = 'CRUDE OIL', mode = 'keep') 

    if before_year == '2024':
        usa_2024 = ['IYEAR','COMMODITY_RELEASED_TYPE','CAUSE', 'LOCATION_LATITUDE','LOCATION_LONGITUDE','UNINTENTIONAL_RELEASE_BBLS']    
        clean_df_usa = transformer.necessary_columns(df_usa,usa_2024)
        #keep incidents only when carried substance is crude oil
        substance_carried_df = transformer.keep_values(clean_df_usa, column_name = 'COMMODITY_RELEASED_TYPE', value = 'CRUDE', mode = 'keep') 
        final_df = transformer.bar_to_lit_to_m3(substance_carried_df)

    loader.load(final_df,new_df_name)


def main():
    file_name_canada = 'data/pipeline-incidents-comprehensive-data.csv'
    file_name_usa_1986_2002 = 'data/accident_hazardous_liquid_1986_jan2002.txt'
    file_name_usa_2002_2009 = 'data/accident_hazardous_liquid_jan2002_dec2009.txt'
    file_name_usa_2010_2024 = 'data/accident_hazardous_liquid_jan2010_present.txt'

    final_data_canada = 'data/final_df_canada.csv'
    final_data_usa_1986_2002 = 'data/final_df_usa_1986_2001.csv'
    final_data_usa_2002_2009 = 'data/final_df_usa_2002_2009.csv'
    final_data_usa_2010_2024 = 'data/final_df_usa_2010_2024.csv'

    df_canada = extractor.extract_df([final_data_canada], 'Canada', 'analysis')
    df_usa_1986_2002 = extractor.extract_df([final_data_usa_1986_2002], 'USA', 'analysis')
    df_usa_2002_2009 = extractor.extract_df([final_data_usa_2002_2009], 'USA', 'analysis')
    df_usa_2010_2024 = extractor.extract_df([final_data_usa_2010_2024], 'USA', 'analysis')  


    labels = ['1986-2001','2002-2009', '2010-2024']
    calc_and_stats.boxes_distr([df_usa_1986_2002,df_usa_2002_2009,df_usa_2010_2024], ['IDATE', 'IYEAR', 'IYEAR'], labels, out_name = 'AllUSA') 


"""
To Do: 

1. Make transformer.py more versatile:
    A. Combine some of the functions, so everything can be called from __main__.py with one line
    B. Transfer data_process functions from __main__.py to transformer.py

2. Make Geospatial Plot more versatile: 
    A. Should not depend on the order of data frames    
    B. Plots should be available for both countries together as well as separate plots for each country              
                        
"""
   






 


    



     




main()
