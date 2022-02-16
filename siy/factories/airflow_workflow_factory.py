from typing import Iterable

from airflow import DAG

from siy.entities import Connection

class AirflowWorkflowFactory:
    def create_dags(self, connections: Iterable[Connection]) -> Iterable[DAG]:
        # create one dag per connection at least
        for c in connections

        # add tasks for each source

        # add tasks for the destination - this will depend on if the connection needs all tables or not!

        raise NotImplementedError("Have not yet created this!")

    def _create_connection_dag(self, connection: Connection) -> DAG:
        dag = DAG(
            dag_id=f"generated_{self._clean_name_for_airflow(connection.name)}",
            schedule_interval= connection.overall_update_frequency if connection.overall_update_frequency else "@once"
        )

        # add tasks for each source

    @staticmethod
    def _clean_name_for_airflow(name: str) -> str:
        return name.lower().replace("-", "_")
