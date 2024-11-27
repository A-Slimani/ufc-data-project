import datetime
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.empty import EmptyOperator 

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=1),
}

dag = DAG(
    'scrapy_fights',
    default_args=default_args,
    description='Scrape UFC fights',
    schedule_interval='@weekly',
    start_date=datetime.datetime(2024, 1, 1),
    catchup=False,
    tags=['scrapy'],
)

scrape_fighters = DockerOperator(
    task_id='scrape_fights',
    image='ufc-data-project-scrapy',
    api_version='auto',
    auto_remove=True,
    command='scrapy crawl fights',
    docker_url="unix://var/run/docker.sock",
    network_mode="ufc-data-project_default",    
    environment={
        'URI': '{{ var.value.URI }}',
    }
    dag=dag,
)
