import pandas as pd

def load(final_df: pd.DataFrame, file_name: str) -> None:
    """
    This function write final data frame to csv.
    Args:
        final_df: data frame
        file_name: name of the csv to write.
    Returns: 
        None
    """
    
    final_df.to_csv(file_name, index=False)

    return


