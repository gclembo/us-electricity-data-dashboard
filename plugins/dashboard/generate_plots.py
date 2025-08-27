import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime

def run_plot_script():
    # get data
    file_path = Path(__file__)
    project_folder = file_path.resolve().parent.parent
    data_folder = project_folder / "data"
    plots_folder = project_folder / "dashboard/plots"

    all_data_filename = "electricity.csv"
    electricity_data = pd.read_csv(data_folder / all_data_filename, parse_dates=["period"])

    yearly_data_filename = "yearly_data.csv"
    yearly_data = pd.read_csv(data_folder / yearly_data_filename)

    monthly_forecast_filename = "monthly_forecast.csv"
    monthly_forecast_data = pd.read_csv(data_folder / monthly_forecast_filename, parse_dates=["period"])

    plot_folder_name = "plots"
    # plot 1: monthly generation
    types_data_all = electricity_data[electricity_data["fueltypeid"] != "ALL"]
    palette = {
        "WND": "#9467bd",
        "SUN": "#ffd92f",
        "HYC": "#1f77b4",
        "NUC": "#2ca02c",
        "NG": "#ff7f0e",
        "COL": "#8c564b"
    }

    label_map = {
        "WND": "Wind",
        "SUN": "Solar",
        "HYC": "Conventional Hydroelectric",
        "NUC": "Nuclear",
        "NG": "Natural Gas",
        "COL": "Coal"
    }

    plt.figure(1, figsize=(11, 5))
    ax = sns.lineplot(data=types_data_all, x="period", y="generation",
                    hue="fueltypeid", palette=palette, errorbar=('ci', False))

    handles, old_labels = ax.get_legend_handles_labels()
    labels = [label_map[name] for name in old_labels]

    plt.legend(bbox_to_anchor=(1, 1), title="Energy Source", handles=handles, labels=labels)
    plt.title("US Electricity Generation by Main Sources")
    plt.ylabel("Total Generation (thousand megawatthours)")
    plt.xlabel("Month")
    caption = "Data From the U.S. Energy Information Administration \n(https://www.eia.gov/)"
    plt.figtext(0.9, -0.05, caption, ha="right")
    plt.savefig(plots_folder / "monthly-generation.png", bbox_inches = "tight")

    # Plot 2: average generation per month
    plt.figure(2, figsize=(6, 4))
    types_data_year = yearly_data[yearly_data["fueltypeid"] != "ALL"]
    ax = sns.lineplot(data=types_data_year, x="year", y="generation",
                    hue="fueltypeid", palette=palette, errorbar=('ci', False))

    handles, old_labels = ax.get_legend_handles_labels()
    labels = [label_map[name] for name in old_labels]

    plt.legend(bbox_to_anchor=(1, 1), title="Energy Source", handles=handles, labels=labels)
    plt.title("US Electricity Generation by Source")
    plt.ylabel("Average Generation per Month (thousand megawatthours)")
    plt.xlabel("Year")
    plt.figtext(0.9, -0.1, caption, ha="right")
    plt.savefig(plots_folder / "yearly_generation_avg.png", bbox_inches = "tight")

    # Plot 3: Average Generation By Month
    plt.figure(3, figsize=(6, 4))
    sns.barplot(electricity_data[electricity_data["fueltypeid"] == "ALL"], x="month", y="generation", errorbar=None)
    plt.title("US Electricity Generation Monthly Averages")
    plt.ylabel("Average Generation (thousand megawatthours)")
    plt.xlabel("Month")
    plt.figtext(0.9, -0.1, caption, ha="right")
    plt.savefig(plots_folder / "monthly_avg.png", bbox_inches = "tight")

    # Plot 4: Projection
    curr_date = types_data_all["period"].max()
    curr_year = curr_date.year
    curr_month = curr_date.month
    past_date = datetime(curr_year - 3, curr_month, 1)

    plt.figure(4, figsize=(11, 5))
    before = types_data_all.loc[types_data_all["period"] > past_date, monthly_forecast_data.columns] # choose range
    full_data = pd.concat([before, monthly_forecast_data])

    ax = sns.lineplot(data=full_data, x="period", y="generation", hue="fueltypeid", palette=palette, errorbar=('ci', False))
    plt.axvline(x=max(types_data_all["period"]), ymin=0, ymax=max(types_data_all["generation"]) * 1.1, color="black")
    plt.annotate(
        " Forecast ", xytext=(max(types_data_all["period"]),
        max(types_data_all["generation"])),
        arrowprops=dict(arrowstyle='->'),
        xy=(monthly_forecast_data["period"].median(), max(types_data_all["generation"]) * 0.9)
    )
    handles, old_labels = ax.get_legend_handles_labels()
    labels = [label_map[name] for name in old_labels]

    plt.legend(bbox_to_anchor=(1, 1), title="Energy Source", handles=handles, labels=labels)
    plt.title("Electricity Generation Projections")
    plt.ylabel("Total Generation (thousand megawatthours)")
    plt.xlabel("Month")
    plt.figtext(0.9, -0.05, caption, ha="right")
    plt.savefig(plots_folder / "monthly_forecast.png", bbox_inches = "tight")
    print("plotting complete!")
