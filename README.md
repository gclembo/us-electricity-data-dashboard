This project creates a basic dashboard for US electricity generation and projections for future generation. 
It takes data from the EIA API, models forecast using the SARIMAX model from statsmodels and plots using Seaborn and MatplotLib. 
Finally the update flow is regulated using Apache Airflow with Docker. 

To initialize the dashboard first you will need to put your EIA v2 API into plugins/etl/api_key_template.txt 

Then run the following commands with Docker:

`docker compose up airflow-init`

`docker compose up`

The final rough dashboard can be viewed at: https://gclembo.github.io/us-electricity-data-dashboard/plugins/dashboard/

The html file for this can be found at plugins/dashboard/index.html

