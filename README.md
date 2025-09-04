# End to End UFC data pipeline project

Practice data engineering project using ufc data.
[Here is a write up of the project and it's learnings](https://innovative-walnut-cd4.notion.site/Data-Pipeline-Project-1b94bb5188cb80c6bcf3d86bf6042a9e)

## Pre setup
- Ensure you have docker installed

## Setup
1. Clone the repo with `git clone https://github.com/A-Slimani/ufc-data-project`
2. Enter into the project folder and setup python environment with `python -m venv .venv`
3. Install python dependecies with `pip install -r requirements.txt`
4. Setup environment with docker run the command `docker-compose up -d`
5. Ensure you have a dbt profile created read more here `https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles`
6. Enter airflow web ui and add db connection variable `DB_URI` `your uri here`

