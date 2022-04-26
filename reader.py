import os
from typing import Callable, List

import pandas as pd


def read_file_to_df(file_path: str, *args, **kwargs) -> pd.DataFrame:
    """
    simple file reader, try to determine file extension and read it via pandas
    :param file_path:
    :return: pd.DataFrame
    """
    filename: str = os.path.basename(file_path)
    file_extension = filename.split(".")[-1]
    if file_extension not in [
        "csv",
        "json",
    ]:
        raise NotImplementedError(
            f"extension {file_extension} is not supported at the moment"
        )
    if file_extension == "csv":
        kwargs["skipinitialspace"] = True
    if file_extension == "json":  # assume we always have jsonl
        kwargs["lines"] = True
    pd_file_reader: Callable = getattr(pd, f"read_{file_extension}")

    df_list: List[pd.DataFrame] = []
    for chunk in pd_file_reader(file_path, *args, **kwargs):
        df_list.append(chunk)
    data_frame: pd.DataFrame = pd.concat(df_list)
    data_frame["file_name"] = filename

    return data_frame
