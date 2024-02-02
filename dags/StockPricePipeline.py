from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from src.CrawlStockPrice import *

config_symbol = "TCB"

# Declare default arguments in Airflow
default_args = {
    'owner':'anh.ho',
    'start_date':'2024-02-02',
    'email':'anh.ho@tititada.com',
    'retries':0,
}

dag= DAG(
    dag_id="company_profile_pipeline",
    default_args=default_args,
    schedule='@daily',
    catchup=True
)

brand_check_existing_table = BranchPythonOperator(
    task_id='CheckTableExisting',
    python_callable=check_table_existing,
    op_kwargs = {'table_name':"stock_price"},
    dag=dag,
)

create_table = PythonOperator(
    task_id = "CreateStockPriceTable",
    python_callable=create_stock_price_table,
    dag=dag,
)

insert_data = PythonOperator(
    task_id = "InsertStockPrice",
    python_callable=insert_stock_price,
    op_kwargs={'symbol': config_symbol},
    dag=dag,
)

brand_check_existing_table >> [insert_data,create_table]