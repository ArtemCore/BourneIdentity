import os
import sys
from typing import Any, Dict, List, Set

import numpy as np
import pandas as pd
from pandas import DataFrame

from reader import read_file_to_df

currentPath = os.getcwd()
chunk_size = 2


def howTo():
    print(
        "How to use: python main.py <input_file.csv> <input_file.csv> <input_file.json> ..."
    )


def run(args_to_process: List[str]):
    if args_to_process[0] in ["-h", "--help"]:
        return howTo()
    data_frames_list: List[DataFrame] = []
    for file in args_to_process:
        file_path: str = f"{currentPath}/{file}"
        df: DataFrame = read_file_to_df(file_path, chunksize=chunk_size)
        data_frames_list.append(df)
    should_print_jb: bool = process_df(data_frames_list)
    if should_print_jb:
        pass
        # print_jb()


def print_jb():
    with open(f"{currentPath}/jb.txt", "r") as jb:
        jb_lines_list = jb.readlines()
    for line in jb_lines_list:
        print(line.strip())


def process_df(data_frames_list: List[DataFrame]) -> bool:
    should_print_jb = False
    # concat all dataframes in one
    concatinated_df: DataFrame = pd.concat(data_frames_list).replace(
        {np.nan: None}
    )
    search_params: Dict[str, Set] = {"Full name": {"Jason Bourne",}}
    exclude_columns: List[str] = ["Time", "is_bourne", "file_name"]
    used_params: Dict[str, Set] = dict()

    while search_params:
        for column, values in search_params.items():
            # fill in a new column `is_bourne` in case if we have a match with values from search_params
            concatinated_df.loc[
                concatinated_df[column].isin(values), "is_bourne"
            ] = True
            # update used_params dict to skip searching by already used values
            used_params[column] = used_params.get(column, set()).union(values)
        # replace NaN with False
        concatinated_df.is_bourne = concatinated_df.is_bourne.fillna(
            False
        )
        # clear dict to restart cycle
        search_params.clear()
        # create new search dict {"<column_name>": ["<search_values>", ...]}
        new_search_params: Dict[str, Any] = concatinated_df.loc[
            concatinated_df.is_bourne
        ].to_dict("list")
        for column, values in new_search_params.items():
            # skip excluded columns
            if column in exclude_columns:
                continue
            # get search set (values minus already used values with None filter)
            if search_set := set(
                value
                for value in set(values).difference(used_params.get(column, set()))
                if value
            ):
                # fill in search params with a new  key pairs (key -> column name, value -> column values)
                search_params[column] = search_set
    # ort dataframe by datetime
    sorted_dataframe = concatinated_df.sort_values(by="Time")

    for _, row in sorted_dataframe.loc[sorted_dataframe.is_bourne].iterrows():
        should_print_jb = True
        print(row["Time"], row["Full name"], row["file_name"])
    return should_print_jb


if __name__ == "__main__":
    if args_to_process := sys.argv[1:]:  # exclude first argv (main.py)
        run(args_to_process)
    else:
        print("Not enough args. Please run `python main.py -h`")
