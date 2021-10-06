from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago

from common_python.notifications.ms_teams_status import on_failure, on_success
from common_python.sf_operator_generator import default_args
from common_python.create_dm_load import dm_load
from common_python.utils import get_schedule_info


sys_load_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

dag_args = {
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'trigger_rule': 'all_success',
    'on_failure_callback': on_failure,
    'on_success_callback': on_success,
    # 'catchup': False,
    **default_args,
}

dag_name = 'Data_Mart_Data_Load'
dag_purpose = 'A DAG for Data Mart layer every day loading'

schedule_interval, description = get_schedule_info(dag_name, dag_purpose)

dag = DAG(
    dag_id=dag_name,
    default_args=dag_args,
    description=description,
    schedule_interval=schedule_interval,
)

with dag as dag:
    dm_load(dag=dag)
