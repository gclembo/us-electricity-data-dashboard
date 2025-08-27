import pandas as pd
from pathlib import Path
from statsmodels.tsa.statespace.sarimax import SARIMAX

def run_forecasting_script():
    # get data
    file_path = Path(__file__)
    project_folder = file_path.resolve().parent.parent
    data_folder = project_folder / "data"

    all_data_filename = "electricity.csv"
    electricity_data = pd.read_csv(data_folder / all_data_filename, parse_dates=["period"])

    # Modeling functions
    def get_dataset(data, category):
        out = data.loc[
            data["fueltypeid"] == category,
            ["period", "generation", "year", "month"]
        ]
        out = out.sort_values(by="period", ascending=True)
        out.index = pd.DatetimeIndex(out["period"], freq="MS")
        out = out.drop("period", axis=1)
        return out

    def get_forecast(X, y, steps=12):
        model = SARIMAX(
            endog=y, exog=X.loc[:, ["year", "month"]],
            order=(1, 2, 1),
            seasonal_order=(1, 1, 2, 12),
            trend="c",
            enforce_invertibility=False
        )

        min_date = max(y.index)
        next_dates = pd.date_range(start=min_date, periods=12, freq="MS")
        next_year_month = pd.DataFrame({
            "year": next_dates.year,
            "month": next_dates.month
        })

        result = model.fit(maxiter=200)
        return result.get_forecast(steps=steps, exog=next_year_month)


    def get_all_forecasts(data, fuel_names, fore_steps=12):
        out = pd.DataFrame()

        for cat in fuel_names:
            X = get_dataset(data, cat)
            y = X.pop("generation")
            future_forecast = get_forecast(X, y, fore_steps)

            min_date = max(y.index)
            next_dates = pd.date_range(start=min_date, periods=fore_steps + 1, freq="MS")[1:]

            temp = pd.DataFrame({
                "generation": future_forecast.predicted_mean,
                "fueltypeid": cat,
                "period": next_dates
            })
            out = pd.concat([out, temp])
        return out

    # Get forecast
    fuel_types = electricity_data.fueltypeid.unique()
    fuel_types = fuel_types[fuel_types != "ALL"]
    monthly_forecast_data = get_all_forecasts(electricity_data, fuel_types, 12)

    # Export Forecast
    monthly_forecast_filename = "monthly_forecast.csv"
    monthly_forecast_data.to_csv(data_folder / monthly_forecast_filename, index=False)
    print("modeling complete!")