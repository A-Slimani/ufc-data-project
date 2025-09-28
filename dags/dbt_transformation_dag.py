import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable
from docker.types import Mount

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'email_on_failure': False,
  'email_on_retry': False
}

dag = DAG(
  'dbt_transformations',
  default_args=default_args,
  description='run dbt transformations DAG',
  schedule_interval=None,
  start_date=datetime.datetime(2025, 1, 1),
  catchup=False
)

dbt_transformations = DockerOperator(
  task_id='dbt_schema_transformations',
  image='ghcr.io/dbt-labs/dbt-postgres:1.9.0',
  api_version='auto',
  auto_remove='force',
  command='run --profiles-dir /usr/app/dbt --target dev',
  docker_url="unix://var/run/docker.sock",  
  network_mode='ufc-data-project_default',
  mounts=[
    Mount(
      target='/usr/app/dbt',
      source=Variable.get('DBT_PATH'),
      type='bind',
    )
  ],
  dag=dag
)