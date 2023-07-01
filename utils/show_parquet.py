import sys

import pandas as pd


def show_parquet(path: str):
    df = pd.read_parquet(path=path)
    print(df)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        show_parquet(sys.argv[1])
    else:
        print("missing path")
        exit(1)
