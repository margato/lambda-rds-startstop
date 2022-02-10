from typing import List


class ResourceService:
    def __init__(self, regions: List[str]):
        self.regions = regions
        self.client = None

    def start_instances(self) -> None:
        pass

    def stop_instances(self) -> None:
        pass
