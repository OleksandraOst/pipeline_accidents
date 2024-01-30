import pandas as pd

def extract_df(files_list: list, country: str, mode: str) -> pd.DataFrame:
   """
    This function extract data. 
    Concatenation of data frames for one country  is done if multiple data frames available.
    Args:
        files_list: list of data set file names
        country: country where accident happened
        mode: 'preprocess' for preprocessing of data, or 'analysis' for data set ready for the analysis
    Returns: 
        extract_df: data frame (concatenated if multiple data frames available)
    """
   if mode == 'preprocess':
      if len(files_list) > 1:
            df_list = []
            for file in files_list:
               if country == 'USA': 
                  df = pd.read_csv(file, sep='\t', encoding = "ISO-8859-1")
               if country == 'Canada': 
                  df = pd.read_csv(file, encoding = "ISO-8859-1")
               df_list.append(df)

            extract_df = pd.concat(df_list,ignore_index=True)
      
      else: 
         if country == 'USA': 
            extract_df = pd.read_csv(files_list[0], sep='\t', encoding = "ISO-8859-1")
         if country == 'Canada': 
            extract_df = pd.read_csv(files_list[0], encoding = "ISO-8859-1")

   if mode == 'analysis':
      extract_df = pd.read_csv(files_list[0], encoding = "ISO-8859-1")
   

   return extract_df

     

 