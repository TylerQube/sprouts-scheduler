import yaml
import pandas as pd
from shift import Shift


def load_yaml(path):
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    return data


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


def parse_shifts(yaml):
    shifts = []
    for initiative in yaml:
        shift_arr = yaml[initiative]
        for shift in shift_arr:
            # on-call shifts don't have days
            if "days" not in shift:
                new_shift = Shift(initiative, "n/a", shift["time"], shift["slots"])
                shifts.append(new_shift)
            else:
                for day in shift["days"]:
                    new_shift = Shift(initiative, day, shift["time"], shift["slots"])
                    shifts.append(new_shift)
    return shifts
