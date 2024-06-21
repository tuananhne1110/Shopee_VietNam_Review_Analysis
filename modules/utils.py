import os
import re
import pandas as pd
import unicodedata

from os.path import isfile, join
from typing import List, Dict
import modules.user_object_defined as udt

def getAllFolderPath(ppath: str) -> (List[str]):
    """
    Hàm dùng để lấy tất cả các thư mục con của `ppath`

    Args:
        ppath (str): đường dẫn thư mục cha

    Returns:
        List[str]
    """
    return [re.sub("/+", "/", f"{ppath}/{name}/") for name in os.listdir(ppath)]
    
    
def getFilenames(pdirectoryPath: str) -> (List[str]):
    """
    Dùng để lấy tất các các filename nằm trong `pdirectoryPath`

    Args:
        pdirectoryPath (str): đường dẫn của thư mục cha

    Returns:
        List[str]: 
    """
    return [f for f in os.listdir(pdirectoryPath) if isfile(join(pdirectoryPath, f))]
    
    
def readReviews(pdirectoryPath: List[str]) -> (udt.Dataframe):
    """
    Dùng để đọc tất cả các review từ các file csv

    Args:
        pdirectoryPath (List[str]): đường dẫn của folder chứa các file csv

    Returns:
        [udt.Dataframe]: pandas dataframe gồm 2 feature là `raw_comment` và `rating`
    """
    reviews = pd.DataFrame()
    
    for path in pdirectoryPath:
        csv_paths = getFilenames(path) # lấy tất cả các file csv nằm trong path
        
        for csv_path in csv_paths:
            df = pd.read_csv(path + csv_path) # đọc file csv mới lên
            reviews = pd.concat([reviews, df], axis=0) # nối df với review
            
    '''Đổi tên cột comment thành raw_comment và reset index cho toàn bộ dataframe'''        
    return reviews.reset_index(drop=True)


def extract_columns(input_file: str, output_file: str, columns: List[str], rename_map: Dict[str, str] = None):
    """
    Extract specified columns from a CSV file and save them to a new CSV file.

    Args:
        input_file (str): The path to the input CSV file.
        output_file (str): The path to the output CSV file.
        columns (List[str]): The list of column names to extract.
    """
    # Read the original CSV file
    df = pd.read_csv(input_file, encoding= "utf-8-sig")
    
    # Select the specified columns
    df_selected = df[columns]
    
    # Rename columns if a rename map is provided
    if rename_map:
        df_selected = df_selected.rename(columns=rename_map)
    
    # Save the selected columns to a new CSV file
    df_selected.to_csv(output_file, index=False, encoding="utf-8-sig")


def buildDictionaryFromFile(ppath: str, psuffix: bool = False) -> (Dict[str, str]):
    """
    Dùng để xây dựng một từ điển tử filepath

    Args:
        ppath (str): đường dẫn file
        psuffix (bool): 

    Returns:
        [Dict[str, str]]: 
    """
    d = {}
    
    with open(ppath) as rows:
        if not psuffix:
            for row in rows:
                prefix, suffix = row.strip().split(',')
                prefix = unicodedata.normalize('NFD', prefix.strip())
                suffix = unicodedata.normalize('NFD', suffix.strip())
                d[prefix] = suffix
        else:
            for row in rows:
                prefix = unicodedata.normalize('NFD', row.strip())
                d[prefix] = True
                
    return d


def buildListFromFile(ppath: str) -> (List[str]):
    """
    Tạo List[str] chứa các từ trong ppath

    Args:
        ppath (str): đường dẫn đến file cần đọc

    Returns:
        (List[str]): 
    """
    d = []
    
    with open(ppath) as rows:
        for row in rows:
            row = unicodedata.normalize('NFD', row.strip())
            d.append(row)
            
    return d         
            