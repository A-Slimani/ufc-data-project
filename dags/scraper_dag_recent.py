import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'email_on_failure': False,
  'email_on_retry': False
}

dag = DAG(
  'scrape_ufc_recent',
  default_args=default_args,
  description='scrape recent ufc events',
  schedule_interval=None,
  start_date=datetime.datetime(2025, 1, 1),
  catchup=False
)

scrape_fighters_and_events = DockerOperator(
  task_id='scrape_fighters_and_events',
  image='ufc-data-project-3-ufc-scraper',
  api_version='auto',
  auto_remove='force',
  command='python ./scraper/ufc_fighters_and_events.py --recent',
  docker_url="unix://var/run/docker.sock",
  network_mode="ufc-data-project-3_default",
  environment={
    'DB_URI': '{{ var.value.DB_URI }}'
  },
  dag=dag
)

scrape_fights = DockerOperator(
  task_id='scrape_fights',
  image='ufc-data-project-3-ufc-scraper',
  api_version='auto',
  auto_remove='force',
  command='python ./scraper/ufc_fights.py --recent',
  docker_url="unix://var/run/docker.sock",
  network_mode="ufc-data-project-3_default",
  environment={
    'DB_URI': '{{ var.value.DB_URI }}'
  },
  dag=dag
)

scrape_fighters_and_events >> scrape_fights