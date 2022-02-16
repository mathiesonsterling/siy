from typing import Iterable, Optional

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator

from siy.factories.base_workflow_factory import BaseWorkflowFactory
from siy.entities import Connection


class AirflowWorkflowFactory(BaseWorkflowFactory):
    def __init__(self, use_gke: bool = False):
        self.use_gke = use_gke

    def create_dags(self, connections: Iterable[Connection]) -> Iterable[DAG]:
        # create one dag per connection at least
        for c in connections:
            connection_dag = self._create_connection_dag(c)
        # add tasks for each source

        # add tasks for the destination - this will depend on if the connection needs all tables or not!

        raise NotImplementedError("Have not yet created this!")

    def _create_connection_dag(self, connection: Connection) -> DAG:
        dag = DAG(
            dag_id=f"generated_{self._clean_name_for_airflow(connection.name)}",
            schedule_interval= connection.overall_update_frequency if connection.overall_update_frequency else "@once"
        )

        # add tasks for each source
        # make sure we get the dependencies each one needs!
        start_task_chains = [s for s in connection.sources if len(list(s.depends_on)) == 0]
        task_ends = {}
        for source in start_task_chains:
            if len(list(source.depends_on)) == 0:
                previous_task: Optional[KubernetesPodOperator] = None
                for task in source.docker_tasks:
                    airflow_task = self._make_kubernetes_task_for_docker_image(task)
                    dag.add_task(airflow_task)
                    if previous_task:
                        airflow_task.set_upstream(previous_task)
                    previous_task = airflow_task
                    task_ends[source.name] = airflow_task

        for source in connection.sources:
            if source not in start_task_chains:
                previous_task = Optional[KubernetesPodOperator] = None
                for task in source.docker_tasks:
                    airflow_task = self._make_kubernetes_task_for_docker_image(task)
                    dag.add_task(airflow_task)
                    if previous_task:
                        airflow_task.set_upstream(previous_task)
                    else:
                        # tie it to all its depends
                        for prerequisite_source in source.depends_on:
                            source_end_task = task_ends[prerequisite_source.name]
                            airflow_task.set_upstream(source_end_task)

                    previous_task = airflow_task
                    task_ends[source.name] = airflow_task

        return dag

    @staticmethod
    def _clean_name_for_airflow(name: str) -> str:
        return name.lower().replace("-", "_")
