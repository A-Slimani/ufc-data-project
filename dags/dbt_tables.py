import datetime
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(seconds=10),
}

dag = DAG(
    'dbt_tables',
    default_args=default_args,
    description='generate dbt tables for ufc stats',
    schedule_interval='@weekly',
    start_date=datetime.datetime(2024, 1, 1),
    catchup=False,
    tags=['dbt'],
)

scrape_events = DockerOperator(
    task_id='dbt_tables',
    image='ghcr.io/dbt-labs/dbt-postgres:1.8.2',
    api_version='auto',
    command='run',
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    working_dir='/dbt',
    network_mode="bridge",
    mounts=[
        Mount(
            target='/dbt',
            source='/home/aboud/shared/programming/ufc-data-project/ufc-dbt',
            type='bind',
        ),
        Mount(
            target='/root/.dbt',
            source='/home/aboud/.dbt',
            type='bind',
        )
    ],
    dag=dag,
)