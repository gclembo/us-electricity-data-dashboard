import requests
import json
import pandas as pd
from pathlib import Path

def run_etl_script():
    # get api key from file
    file_path = Path(__file__)
    folder_path = file_path.parent

    directory = {str(file.name) for file in folder_path.iterdir()}

    if "api_key.txt" in directory:
        with open(folder_path / "api_key.txt") as file:
            api_key = file.read()
    elif "api_key_template.txt" in directory:
        with open("api_key_template.txt") as file:
            api_key = file.read()
    else:
        print("failed to load api key")

    # Setup for connecting to api
    url="https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key=" + api_key

    header = {
        "frequency": "monthly",
        "data": [
            "generation"
        ],
        "facets": {
            "fueltypeid": [
                "ALL",
                "COL",
                "HYC",
                "NG",
                "NUC",
                "SUN",
                "WND"
            ],
            "location": [
                "US"
            ],
            "sectorid": [
                "99"
            ]
        },
        "sort": [
            {
                "column": "period",
                "direction": "desc"
            }
        ],
        "offset": 0,
        "length": 5000
    }

    # connect and extract data from eia api

    response = requests.get(url, headers={"X-Params": json.dumps(header)})

    # load into pandas

    json_data = json.loads(response.text)
    all_data = pd.DataFrame(json_data["response"]["data"])

    # data transformation
    all_data = all_data.drop(["location", "stateDescription", "sectorid", "sectorDescription"], axis=1)

    # correct types
    numeric = ["generation"]

    all_data[numeric] = all_data[numeric].astype(float)
    all_data["period"] = pd.to_datetime(all_data["period"])

    all_data["generation"] = all_data.groupby("fueltypeid")["generation"].bfill()

    # yearly data
    all_data["year"] = all_data["period"].dt.year
    yearly_data = all_data.drop(["period", "generation-units", "fuelTypeDescription"], axis=1)

    curr_date = max(all_data["period"])
    if curr_date.month == 12:
        year_until = curr_date.year
    else:
        year_until = curr_date.year - 1

    yearly_data = yearly_data.loc[yearly_data["year"] <= year_until]

    yearly_data = yearly_data.groupby(["year", "fueltypeid"]).sum(numeric_only=True).reset_index()


    # add month col
    all_data["month"] = all_data["period"].dt.month


    # save to csv


    project_folder = file_path.resolve().parent.parent
    data_folder = project_folder / "data"

    all_data_filename = "electricity.csv"
    yearly_data_filename = "yearly_data.csv"
    all_data.to_csv(data_folder / all_data_filename, index=False)
    yearly_data.to_csv(data_folder / yearly_data_filename, index=False)
    print("etl complete!")
