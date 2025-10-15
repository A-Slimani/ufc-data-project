import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from airflow.models import Variable

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'email_on_failure': False,
  'email_on_retry': False
}

dag = DAG(
  'scrape_ufc_build_railway',
  default_args=default_args,
  description='scrape all ufc events for railway',
  schedule_interval=None,
  start_date=datetime.datetime(2025, 1, 1),
  catchup=False
)

scrape_fighters_and_events = DockerOperator(
  task_id='scrape_fighters_and_events',
  image='ufc-data-project_ufc-scraper',
  api_version='auto',
  auto_remove='force',
  command='python ./scraper/ufc_fighters_and_events.py --build',
  docker_url="unix://var/run/docker.sock",
  network_mode="ufc-data-project_default",
  environment={
    'DB_URI': '{{ var.value.DB_URI_RAILWAY }}',
    'LOG_DIR': '{{ var.value.LOG_DIR }}'
  },
  tmp_dir='/tmp/airflow',
  dag=dag
)

scrape_fights = DockerOperator(
  task_id='scrape_fights',
  image='ufc-data-project_ufc-scraper',
  api_version='auto',
  auto_remove='force',
  command='python ./scraper/ufc_fights.py --build',
  docker_url="unix://var/run/docker.sock",
  network_mode="ufc-data-project_default",
  environment={
    'DB_URI': '{{ var.value.DB_URI_RAILWAY }}',
    'LOG_DIR': '{{ var.value.LOG_DIR }}'
  },
  tmp_dir='/tmp/airflow',
  dag=dag
)

dbt_transformations = DockerOperator(
  task_id='dbt_schema_transformations',
  image='ghcr.io/dbt-labs/dbt-postgres:1.9.0',
  api_version='auto',
  auto_remove='force',
  command='run --profiles-dir /usr/app/dbt --target railway',
  docker_url="unix://var/run/docker.sock",  
  network_mode='ufc-data-project_default',
  mounts=[
    Mount(
      target='/usr/app/dbt',
      source=Variable.get("DBT_PATH"),
      type='bind',
    )
  ],
  dag=dag
)

scrape_fighters_and_events >> scrape_fights >> dbt_transformations
