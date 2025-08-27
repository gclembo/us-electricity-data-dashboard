This project creates a basic dashboard for US electricity genearation and pojections for future generation. 
It takes data from the EIA API, models forecast using the SARIMAX model from statsmodels and plots using Seaborn and MatplotLib. 
Finally the update flow is regulated using Apache Airflow with Docker. 

To initialize the dashboard run the following commands with Docker:

`docker compose up airflow-init`
`docker compose up`

The final rough dashboard can be viewed at: https://gclembo.github.io/us-electricity-data-dashboard/plugins/dashboard/
