from airflow import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime 

from plugins.dashboard.generate_plots import run_plot_script
from plugins.etl.etl_script import run_etl_script
from plugins.modeling.forecast_modeling import run_forecasting_script

with DAG(
    dag_id="dashboard_refresh",
    start_date=datetime(2025, 8, 25),
    schedule="0 12 1 * *",
    catchup=False, 
    tags=["dashboard", "refresh", "electricity"]
) as dag: 
    etl = PythonOperator(
        task_id="etl",
        python_callable=run_etl_script 
    )
    modeling = PythonOperator(
        task_id="modeling",
        python_callable=run_forecasting_script 
    )
    render_plots = PythonOperator(
        task_id="plotting",
        python_callable=run_plot_script 
    )
    etl >> modeling >> render_plots