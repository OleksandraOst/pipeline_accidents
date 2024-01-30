import pandas as pd
from datetime import datetime

def necessary_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
   """
    This function allows to choose necessary columns and prepare data for the analysis.
    Args:
        df: data frame
        columns: list of necessary columns
    Returns: 
        clean_df: clean data frame
    """
   df = df[columns] 
   print("DATA FRAME COLUMNS",df)

   #Clean data from missing values and duplicates
   df = df.dropna()
   print("DATA FRAME DROPNA",df)
   clean_df = df.drop_duplicates()
   print("DATA FRAME DUPLICATES",df)

   return clean_df

def keep_values(clean_df: pd.DataFrame, column_name: str, value: str, mode: str) -> pd.DataFrame:
    """
    This function allows to keep values related to crude oil and filter rows with the data out of interest.
    Args:
        clean_df: data frame without duplicated and Nan values
        value: value to keep or filter
        mode: 'keep' or 'filter' data
    Returns: 
        modified_df: final data frame 
    """

    if mode == 'keep':
        modified_df = clean_df[clean_df[column_name].str.contains(value)]

    if mode == 'filter':
        #For example, filter cases where substance was not released because it causes less damage to the environment, injuries and financial loss.
        filter = clean_df[column_name].str.contains(value)
        modified_df = clean_df[~filter]

    return modified_df

def relabel(df: pd.DataFrame, column_name: str, value: str, new_value: str) -> pd.DataFrame:
    """
    This function allows to relable columns data in the data frame with certain conditions.
    Args:
        df: data frame
        column_name: name of the column in the data frame
        value: what value to search in the column
        new_value: set the new value
    Returns: 
        df: modified data frame
    """
    df.loc[df[column_name].str.contains(value, case=False), column_name] = new_value
    return df

def bar_to_lit_to_m3(df: pd.DataFrame)->pd.DataFrame:
    """
    This function converts barrels to liters and to cubic meters.
    Args:
        df: data frame
    Returns: 
        df: modified data frame
    """
    bar_to_lit = 159 #One barrel of oil contains 159 liters
    lit_to_m3 = 0.001#One liter is 0.001 cubic meter
    df['RELEASE LIT'] = df['UNINTENTIONAL_RELEASE_BBLS'].apply(lambda val: str(float(val)*bar_to_lit) )
    df['RELEASE M3'] = df['RELEASE LIT'].apply(lambda val: str(float(val)*lit_to_m3) )

    return df


    
   
