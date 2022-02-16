from abc import ABC

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from siy.value_items import DockerTask


class BaseWorkflowFactory(ABC):
    def __init__(self, use_gke: bool = False):
        self.use_gke = use_gke

    def _make_kubernetes_task_for_docker_image(self, image: DockerTask) -> KubernetesPodOperator:
        if self.use_gke:
            pass
        else:
            pass
        raise NotImplementedError()