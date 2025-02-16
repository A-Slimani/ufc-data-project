# UFC Data Project
Practice project for data engineering. Scraping ufc data from sherdog and ufcstats

## How to run the data pipelines
- Start by running the dockerfiles with the command `docker compose up --build -d`
- Access the airflow from the browser port `:8080` then run
    - `scrapy_sherdog_ids` first to build the table to connect between ufcstats data and sherdog data 
    - `scrapy_ufcstats` to collect all the data

## Notes
- cant run dbt on airflow running it manually






