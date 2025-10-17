from abc import ABC, abstractmethod


class ObjectStorageBucket(ABC):
    @abstractmethod
    def download(bucket: str, object: str, save_location: str = "/tmp") -> str:
        pass