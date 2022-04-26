import os
from typing import Callable

import pandas as pd

def read_file_to_df(file_path: str, *args, **kwargs) -> pd.DataFrame:
    """
    simple file reader, try to determine file extension and read it
    :param file_path:
    :return:
    """
    filename: str = os.path.basename(file_path)
    file_extension = filename.split(".")[-1]
    if file_extension in [
        "csv",
        "json",
    ]:
        pd_file_reader: Callable = getattr(pd, f"read_{file_extension}")
        data_frame: pd.DataFrame = pd_file_reader(file_path, *args, **kwargs)
        data_frame["file_name"] = filename
    else:
        raise NotImplementedError(
            f"extension {file_extension} is not supported at the moment"
        )
    return data_frame
