import yaml
import pandas as pd
from shift import Shift

def get_file():
    while True:
        print("Please specify a CSV file containing volunteer form responses:")
        fname = input()
        print()
        try:
            file = pd.read_csv(fname)
            return file
        except Exception:
            print("File not found, please try again")