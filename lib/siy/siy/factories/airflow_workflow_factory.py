from typing import Iterable, Optional, Tuple

from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from kubernetes.client.models.v1_env_var import V1EnvVar

from siy.entities import Connection, BaseDataLake, BigQueryDataTable, AirbyteIngestSource, BaseSource
from siy.value_items import DockerTask, TableProcessedMessage, AirbyteConnectionInfo
from siy.repositories import BaseTableProcessedMessageRepository


def notify_destination_of_table_processed(*args, **kwargs):
    data_lake_type = kwargs["data_lake_type"]
    # todo construct our repo here
    repo: BaseTableProcessedMessageRepository = None
    table_strings = str(kwargs["tables"]).split(",")
    destination_name = kwargs["destination_name"]

    if data_lake_type == "BigQueryDataLake":
        tables = [BigQueryDataTable.parse(ts) for ts in table_strings]
        for table in tables:
            message = TableProcessedMessage(
                table=table,
                destination_name=destination_name,
                handled=False
            )
            repo.add(message=message)


class AirflowWorkflowFactory:
    """
    Main entry point when airflow is the main orchestrator used

    To use, create a single DAG an iterate over the connection with the create_dags method.
    Load each into the global namespace and you'll be all set!
    """
    def __init__(
            self, data_lake: BaseDataLake, airbyte_connection_info: AirbyteConnectionInfo,
            use_gke: bool = False, namespace: str = "default"
    ):
        self.use_gke = use_gke
        self.namespace = namespace
        self.data_lake = data_lake
        self.airbyte_connection_info = airbyte_connection_info

    def create_dags(self, connections: Iterable[Connection]) -> Iterable[DAG]:
        all_sources = [source for con in connections for source in con.sources]
        all_tables = {t for source in all_sources for t in source.produced_data_tables}

        # create one dag per connection at least
        for c in connections:
            connection_dag, sources_done = self._create_connection_dag(c)

            for d in c.destinations:
                kwargs = {
                    "destination_name": d.name,
                    "tables": ",".join([str(t1) for t1 in all_tables]),
                    "data_lake_type": type(self.data_lake)
                }
                notify_op = PythonOperator(
                    python_callable=notify_destination_of_table_processed,
                    op_kwargs=kwargs,
                    dag=connection_dag
                )
                sources_done.set_downstream(notify_op)

            yield connection_dag

    # we need to add destination trigger tasks - these should NOT block, but should be part of the DAG

    def _create_connection_dag(self, connection: Connection) -> Tuple[DAG, DummyOperator]:
        dag = DAG(
            dag_id=f"generated_{self._clean_name_for_airflow(connection.name)}",
            schedule_interval= connection.overall_update_frequency if connection.overall_update_frequency else "@once"
        )

        sources_done = DummyOperator(dag=dag, task_id="sources_complete")

        # add tasks for each source
        # make sure we get the dependencies each one needs!
        start_task_chains = [s for s in connection.sources if len(list(s.depends_on)) == 0]
        task_ends = {}
        for source in start_task_chains:
            if len(list(source.depends_on)) == 0:
                tasks = self._get_tasks_for_source(source)

                previous_task: Optional[KubernetesPodOperator] = None
                for airflow_task in tasks:
                    dag.add_task(airflow_task)
                    if previous_task:
                        airflow_task.set_upstream(previous_task)
                    previous_task = airflow_task
                    task_ends[source.name] = airflow_task

        for source in connection.sources:
            if source not in start_task_chains:
                tasks = self._get_tasks_for_source(source)

                previous_task: Optional[KubernetesPodOperator] = None
                for airflow_task in tasks:
                    dag.add_task(airflow_task)
                    if previous_task:
                        previous_task.set_downstream(airflow_task)
                    else:
                        # tie it to all its depends
                        for prerequisite_source in source.depends_on:
                            source_end_task = task_ends[prerequisite_source.name]
                            source_end_task.set_downstream(airflow_task)

                    previous_task = airflow_task
                    task_ends[source.name] = airflow_task

        end_tasks = [t for t in dag.tasks if len(t.downstream_task_ids) == 0]
        for t in end_tasks:
            t.set_downstream(sources_done)

        return dag, sources_done

    @staticmethod
    def _clean_name_for_airflow(name: str) -> str:
        return name.lower().replace("-", "_")

    def _get_tasks_for_source(self, source: BaseSource):
        if isinstance(source, AirbyteIngestSource):
            return [self._make_airbytes_task_for_source(source)]
        else:
            return [self._make_kubernetes_task_for_docker_image(t) for t in source.docker_tasks]

    def _make_airbytes_task_for_source(self, source: AirbyteIngestSource) -> AirbyteTriggerSyncOperator:
        return AirbyteTriggerSyncOperator(
            task_id=source.name,
            airbyte_conn_id=self.airbyte_connection_info.airbyte_conn_id,
            connection_id=self.airbyte_connection_info.airflow_conn_id
        )

    def _make_kubernetes_task_for_docker_image(self, docker_task: DockerTask) -> KubernetesPodOperator:
        if self.use_gke:
            raise NotImplementedError()
        else:
            env_vars = [V1EnvVar(name=key, value=docker_task.env_vars[key]) for key in docker_task.env_vars]
            return KubernetesPodOperator(
                image=str(docker_task.image_location),
                name=docker_task.name,
                env_vars=env_vars,
                namespace=self.namespace
            )
