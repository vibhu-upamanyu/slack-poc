import pendulum
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


@dag(dag_id='slack_login_dag_v1', start_date=pendulum.now("UTC"), schedule=None)
def slack_invite_user_dag():
    @task(multiple_outputs=True)
    def get_admin_creds():
        context = get_current_context()
        admin_email = context["dag_run"].conf["admin_email"]
        admin_password = context["dag_run"].conf["admin_password"]
        return {
            "admin_email": admin_email,
            "admin_password": admin_password
        }

    @task(multiple_outputs=True)
    def get_slack_data():
        context = get_current_context()
        slack_workspace_name = context["dag_run"].conf["slack_workspace_name"]
        return {
            "slack_workspace_name": slack_workspace_name
        }

    gmail_login = DockerOperator(
        task_id='gmail_login',
        image='slack_poc:latest',
        docker_url='unix://var/run/docker.sock',
        command="--gmail-login {{ task_instance.xcom_pull(task_ids='get_admin_creds', key='admin_email') }} {{ task_instance.xcom_pull(task_ids='get_admin_creds', key='admin_password') }}",
        network_mode='bridge',
        environment={
            "PYTHONUNBUFFERED": 1
        },
        mounts=[Mount(source='slack-poc-vol', target='/web-automation/slack-poc-vol', type='volume')],
        auto_remove="success"
    )

    slack_login = DockerOperator(
        task_id='slack_login',
        image='slack_poc:latest',
        docker_url='unix://var/run/docker.sock',
        command="--slack-login {{ task_instance.xcom_pull(task_ids='get_admin_creds', key='admin_email') }} {{ task_instance.xcom_pull(task_ids='get_slack_data', key='slack_workspace_name') }}",
        network_mode='bridge',
        environment={
            "PYTHONUNBUFFERED": 1
        },
        mounts=[Mount(source='slack-poc-vol', target='/web-automation/slack-poc-vol', type='volume')],
        auto_remove="success"
    )

    get_admin_creds() >> gmail_login >> get_slack_data() >> slack_login


slack_invite_user_dag()
