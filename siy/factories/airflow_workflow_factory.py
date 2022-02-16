from typing import Iterable, Optional

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator
from kubernetes.client.models.v1_env_var import V1EnvVar

from siy.entities import Connection, BaseDestination
from siy.value_items import DockerTask


class AirflowWorkflowFactory:
    """
    Main entry point when airflow is the main orchestrator used

    To use, create a single DAG an iterate over the connection with the create_dags method.
    Load each into the global namespace and you'll be all set!
    """
    def __init__(self, use_gke: bool = False):
        self.use_gke = use_gke

    def create_dags(self, connections: Iterable[Connection]) -> Iterable[DAG]:
        universal_destinations = []

        # create one dag per connection at least
        for c in connections:
            connection_dag = self._create_connection_dag(c)

            # add tasks for the destination - this will depend on if the connection needs all tables or not!
            for destination in c.destinations:
                if destination.processes_all_connections:
                    universal_destinations.append(destination)
                else:
                    self._add_connection_destination(destination=destination, dag=connection_dag)
            yield connection_dag

        for destination in universal_destinations:
            yield self._create_universal_destination_dag(destination)

    def _create_universal_destination_dag(self, destination: BaseDestination) -> DAG:
        dag = DAG(
            dag_id=f"destination_{destination.name}",
            schedule_interval= destination.update_frequency if destination.update_frequency else "@once"
        )

        previous_task: Optional[KubernetesPodOperator] = None
        for task in destination.docker_tasks:
            airflow_task = self._make_kubernetes_task_for_docker_image(task)
            if previous_task:
                previous_task.set_downstream(airflow_task)
            previous_task = airflow_task

        return dag

    def _create_connection_dag(self, connection: Connection) -> DAG:
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

        return dag

    def _add_connection_destination(self, destination: BaseDestination, dag: DAG):
        previous_task: Optional[KubernetesPodOperator] = None
        for t in destination.docker_tasks:
            airflow_task = self._make_kubernetes_task_for_docker_image(t)
            dag.add_task(airflow_task)
            if previous_task:
                previous_task.set_downstream(airflow_task)

    @staticmethod
    def _clean_name_for_airflow(name: str) -> str:
        return name.lower().replace("-", "_")

    def _make_kubernetes_task_for_docker_image(self, docker_task: DockerTask) -> KubernetesPodOperator:
        if self.use_gke:
            raise NotImplementedError()
        else:
            env_vars = [V1EnvVar(name=key, value=docker_task.env_vars[key]) for key in docker_task.env_vars]
            return KubernetesPodOperator(
                image=str(docker_task.image_location),
                name=docker_task.name,
                env_vars=env_vars
            )
