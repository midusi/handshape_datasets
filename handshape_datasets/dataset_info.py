from .dataset_loader import DatasetLoader
from typing import Dict,Tuple


from abc import ABC,abstractmethod
class DatasetInfo(ABC):
    def __init__(self, id:str, input_shape:Tuple[int,int,int], metadata:Dict[str, str], description:str):
        self.id=id
        self.input_shape=input_shape
        self.description=description
        self.metadata=metadata

    def summary(self):
        return f"Dataset id: {self.id}\nDescription: {self.description}" \
               f"\nInput shape: {self.input_shape}" \
               f"\nMetadata: {self.metadata}"


    @abstractmethod
    def get_loader(self)->DatasetLoader:
        pass

class ClassificationDatasetInfo(DatasetInfo):

    def __init__(self, id:str, input_shape:Tuple[int,int,int], metadata:Dict[str, str], description:str, labels:[str]):
        super().__init__(id, input_shape, metadata, description)
        self.labels=labels


    def summary(self):
        return super().summary()+f"\nClasses: {len(self.labels)}\n{','.join(self.labels)}"