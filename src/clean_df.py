
import pandas as pd

def rename_headers(df: pd.DataFrame, headers: list) -> pd.DataFrame:
    """
        Replace the first three columns of a DataFrame with provided headers.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        headers (list): List of new column names to replace the first N columns.
    
    Returns:
        pd.DataFrame: The DataFrame with renamed headers.
    
    Raises:
    ValueError: If DataFrame has fewer columns than the length of headers.
    """
    
    df = df.copy()
    num_headers = len(headers)
    # Ensure there are at least 4 columns
    if df.shape[1] < num_headers:
        raise ValueError(f"DataFrame must have at least {num_headers} columns to rename.")
    
    # Replace the first three columns
    df.columns = headers + list(df.columns[num_headers:])
    
    return df



def remove_double_braces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes all instances of '{{' and '}}' from all string columns in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: A new DataFrame with '{{' and '}}' removed from string columns.
    """
    df_clean = df.copy()
    
    for col in df_clean.select_dtypes(include='object').columns:
        df_clean[col] = df_clean[col].str.replace(r'\{\{|\}\}', '', regex=True)
    
    return df_clean