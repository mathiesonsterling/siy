from dataclasses import dataclass


# see https://docs.airbyte.com/operator-guides/using-the-airflow-airbyte-operator
@dataclass(frozen=True, eq=True)
class AirbyteConnectionInfo:
    airbyte_conn_id: str
    airflow_conn_id: str
