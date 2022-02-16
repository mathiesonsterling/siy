from siy.entities.data_lakes.base_data_lake import BaseDataLake


class BigQueryDataLake(BaseDataLake):
    def __init__(self, project_id: str, dataset: str, processing_dataset: str = ""):
        super().__init__()
        self.project_id = project_id
        self.dataset = dataset
        self.processing_dataset = processing_dataset
