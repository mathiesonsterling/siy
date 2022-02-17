from typing import Iterable, Dict, Union

from siy.entities.sources.base_source import BaseSource
from siy.entities.data_lakes import BaseDataLake, BigQueryDataLake
from siy.value_items import DockerTask, BaseDataTable, PublishedState, BigQueryDataTable, URL


class DBTSource(BaseSource):
    """
    Source for running DBT models to create more data!
    """

    def __init__(self,
                 name: str,
                 data_lake: BaseDataLake,
                 dbt_image_loc: URL,
                 dbt_model_repo: URL,
                 end_models: Iterable[str],
                 state: PublishedState = PublishedState.DEVELOPMENT,
                 depends_on_names: Iterable[str] = None
                 ):
        super().__init__(state=state, depends_on_names=depends_on_names, name=name, data_lake=data_lake)
        self.dbt_image_loc = dbt_image_loc
        self.dbt_model_repo = dbt_model_repo
        self.end_models = end_models

    @property
    def produced_data_tables(self) -> Iterable[BaseDataTable]:
        if isinstance(self.data_lake, BigQueryDataLake):
            return [
                BigQueryDataTable(project_id=self.data_lake.project_id, dataset=self.data_lake.dataset, table_name=m)
                for m in self.end_models
            ]
        else:
            raise NotImplementedError(f"Don't know how to handle data lakes of type {type(self.data_lake)}")

    @property
    def docker_tasks(self) -> Iterable[DockerTask]:
        env_vars = {
            "DBT_MODEL_REPO": str(self.dbt_model_repo)
        }

        if isinstance(self.data_lake, BigQueryDataLake):
            env_vars["INTERIM_DATASET"] = f"{self.data_lake.project_id}.{self.data_lake.processing_dataset}"
            env_vars["OUTPUT_DATASET"] = f"{self.data_lake.project_id}.{self.data_lake.dataset}"
        else:
            raise NotImplementedError(f"Don't know how to handle data lakes of type {type(self.data_lake)}")

        yield DockerTask(
            image_location=self.dbt_image_loc,
            name=self.name,
            env_vars=env_vars
        )

    def to_dict(self) -> Dict[str, Union[str, Dict[str, str]]]:
        return {
            "name": self.name,
            "dbt_image_loc": str(self.dbt_image_loc),
            "dbt_model_repo": str(self.dbt_model_repo),
            "end_models": list(self.end_models),
            "state": str(self.state),
            "depends_on": [s.name for s in self.depends_on],
            "type": type(self)
        }
