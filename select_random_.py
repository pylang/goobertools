"""Select a random item from a resource. Print each line in the file.

Resources include text/csv files or urls to Google Sheets.

"""
import csv
import json
import random
import urllib
import pathlib
import typing as typ
import collections as ct

import pandas as pd


def to_str_dictvalues(data: dict) -> str:
    """Yield a values of a dict."""
    yield from (", ".join(d.values()) for d in data)


def load_google_sheet_url(filepath: pathlib.Path) -> str:
    """Return a url."""
    if not filepath.exists():
        raise FileNotFoundError(f"The filepath to the default google url not found.  Got '{filepath}'.")

    with open(filepath, "r") as f:
        config = json.load(f)

    try:
        url = config["sheets"]["public"]["url"]
    except KeyError:
        raise KeyError(" Failed to load the url from the config.")
    else:
        print(" INFO: Success! Found Google Sheet url in config.")
        return url


def read_txt(filepath: pathlib.Path) -> str:
    """Yield listed items from a file."""
    with open(filepath, "r") as f:
        for line in f.readlines():
            if not line:
                continue
            line = line.strip("\n").lstrip("1. ").lstrip("- ")
            yield line
        

def read_csv(filepath: pathlib.Path) -> dict:
    """Yield (header, row) dict pairs from a csv."""
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            #print("row", row)
            if not row:
                continue
            yield dict(zip(header, row))


# FIX: not just url; resource of str | Path | StringIO
def read_google_sheets(url: str) -> pd.DataFrame:
    """"Return google spreadsheet as a DataFrame."""
    df_raw = pd.read_csv(url, "utf-8", engine="python")
    
    # Split sheets col of string into columns
    splitter = lambda x: pd.Series([i for i in x.split(',')])
    header = list(df_raw.columns.str.split(","))[0]
    df = df_raw.iloc[:, 0].apply(splitter)
    df.rename(columns=dict(enumerate(header)),inplace=True)
    #print(df, type(df), header)
    return df


# FIX: improve with following code; reads numeric cols as int not object (amend test_fixture_select_random.google_sheets)
# def read_google_sheets(url: str) -> pd.DataFrame:
#     """"Return google spreadsheet as a DataFrame."""
#     df_raw = pd.read_csv(url, "utf-8", engine="python", delimiter=",")
#     df_raw.columns.values[0] = ""
#     return df_raw


def read_google_sheets_to_dictrows(url: str) -> dict:
    """"Yield dicts of (header: row) from a google spreadsheet."""
    try:
        df = read_google_sheets(url)
    except (urllib.error.URLError):
        raise
    else:
        for row in df.iterrows():
            yield row[-1].to_dict()


def get_data_values_w_pandas(resource: typ.Union[str, pathlib.Path]) -> str:
    """Yield head-less data from a resource (a url str or file path)."""
    if resource is None:
        print(" Loading config file...")
        config_filepath = pathlib.Path("p/secrets/config_goob.json")
        try:
            resource = load_google_sheet_url(config_filepath)
        except KeyError:
            print(" FAILED: Unable to load config file.")
            raise

    yield from to_str_dictvalues(read_google_sheets_to_dictrows(resource))


def get_data_values_no_pandas(resource: typ.Union[str, pathlib.Path]) -> str:
    """Yield head-less data data from a resource without pandas."""
    print(f" Loading a file '{resource}'...")
    try:
        if resource.suffix == ".csv":
            data = to_str_dictvalues(read_csv(resource))
        elif resource.suffix == ".txt":
            data = read_txt(resource)
        else:
            raise TypeError
    except(AttributeError, TypeError):
        raise TypeError(f"Could not read the file of type {type(resource)}.  Try another resource.")
    else:
        yield from data


# Used with CLI
def shuffle_picks(data: ct.Iterator, seed=None) -> ct.namedtuple:
    """Yield a namedtuple of a random selection (item, remaining, total)."""
    random.seed(seed)
     
    data = list(data)
    length = len(data)
    PickResult = ct.namedtuple("PickResult", "item remaining total")
    
    random.shuffle(data)
    for i, row in enumerate(data):
        yield PickResult(item=row, remaining=length-i, total=length)
