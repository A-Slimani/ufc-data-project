import datetime
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.empty import EmptyOperator 


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'scrapy_events',
    default_args=default_args,
    description='Scrape UFC events',
    schedule_interval=None,  # Disable automatic scheduling
    start_date=datetime.datetime(2024, 1, 1),
    catchup=False,
    tags=['scrapy'],
)

get_sherdog_ids = DockerOperator(
    task_id='get_sherdog_ids',
    image='ufc-data-project-scrapy',
    api_version='auto',
    auto_remove=True,
    command='scrapy crawl sherdog_fighter',
    docker_url="unix://var/run/docker.sock",
    network_mode="ufc-data-project_default",
    environment={
        'URI': '{{ var.value.URI }}',
    },
    dag=dag,
)

scrape_events = DockerOperator(
    task_id='scrape_events',
    image='ufc-data-project-scrapy',
    api_version='auto',
    auto_remove=True,
    command='scrapy crawl events',
    docker_url="unix://var/run/docker.sock",
    network_mode="ufc-data-project_default",    
    environment={
        'URI': '{{ var.value.URI }}',
    },
    dag=dag,
)

scrape_fighters = DockerOperator(
    task_id='scrape_fighters',
    image='ufc-data-project-scrapy',
    api_version='auto',
    auto_remove=True,
    command='scrapy crawl fighters',
    docker_url="unix://var/run/docker.sock",
    network_mode="ufc-data-project_default",    
    environment={
        'URI': '{{ var.value.URI }}',
    },
    dag=dag,
)

scrape_fights = DockerOperator(
    task_id='scrape_fights',
    image='ufc-data-project-scrapy',
    api_version='auto',
    auto_remove=True,
    command='scrapy crawl fights',
    docker_url="unix://var/run/docker.sock",
    network_mode="ufc-data-project_default",    
    environment={
        'URI': '{{ var.value.URI }}',
    },
    dag=dag,
)

get_sherdog_ids >> scrape_events >> scrape_fighters >> scrape_fights