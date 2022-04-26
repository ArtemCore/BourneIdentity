import os
import sys
from typing import Any, Dict, List, Set

import numpy as np
import pandas as pd

from reader import read_file_to_df

CURRENT_PATH = os.getcwd()
CHUNK_SIZE = 2  # number of rows to read


def howTo():
    print(
        "How to use: python main.py <input_file.csv> <input_file.csv> <input_file.json> ..."
    )


def run(args_to_process: List[str]):
    if args_to_process[0] in ["-h", "--help"]:
        return howTo()
    data_frames_list: List[pd.DataFrame] = []
    for file in args_to_process:
        file_path: str = f"{CURRENT_PATH}/{file}"
        df: pd.DataFrame = read_file_to_df(file_path, chunksize=CHUNK_SIZE)
        data_frames_list.append(df)
    result: List[str] = process_df(data_frames_list)
    for line in result:
        print(line)


def print_jb():
    with open(f"{CURRENT_PATH}/jb.txt", "r") as jb:
        jb_lines_list = jb.readlines()
    for line in jb_lines_list:
        print(line.strip())


def process_df(data_frames_list: List[pd.DataFrame]) -> List[str]:
    # concat all dataframes in one
    concatenated_df: pd.DataFrame = pd.concat(data_frames_list).replace({np.nan: None})
    search_params: Dict[str, Set] = {"Full name": {"Jason Bourne",}}
    exclude_columns: List[str] = ["Time", "is_bourne", "file_name"]
    used_params: Dict[str, Set] = dict()

    while search_params:
        for column, values in search_params.items():
            # fill in a new column `is_bourne` in case if we have a match with values from search_params
            concatenated_df.loc[
                concatenated_df[column].isin(values), "is_bourne"
            ] = True
            # update used_params dict to skip searching by already used values
            used_params[column] = used_params.get(column, set()).union(values)
        # replace NaN with False
        concatenated_df.is_bourne = concatenated_df.is_bourne.fillna(False)
        # clear dict to restart cycle
        search_params.clear()
        # create new search dict {"<column_name>": ["<search_values>", ...]}
        new_search_params: Dict[str, Any] = concatenated_df.loc[
            concatenated_df.is_bourne
        ].to_dict("list")
        for column, values in new_search_params.items():
            # skip excluded columns
            if column in exclude_columns:
                continue
            # get search set (values minus already used values with None filter)
            if search_set := set(
                value
                for value in set(values).difference(used_params.get(column, set()))
                if value is not None
            ):
                # fill in search params with a new  key pairs (key -> column name, value -> column values)
                search_params[column] = search_set
    # sort pd.DataFrame by datetime
    filtered_df = concatenated_df.sort_values(by="Time").loc[concatenated_df.is_bourne]
    result = [
        f"{time} {name} {file_name}"
        for time, name, file_name in zip(
            filtered_df["Time"], filtered_df["Full name"], filtered_df["file_name"]
        )
    ]
    return result


if __name__ == "__main__":
    if args_to_process := sys.argv[1:]:  # exclude first argv (main.py)
        run(args_to_process)
    else:
        print("Not enough args. Please run `python main.py -h`")
