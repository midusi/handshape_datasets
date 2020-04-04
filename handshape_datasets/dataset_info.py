from .dataset_loader import DatasetLoader
from typing import Dict,Tuple


from abc import ABC,abstractmethod
class DatasetInfo(ABC):
    def __init__(self, id:str, input_shape:Tuple[int,int,int], metadata:Dict[str, str], description:str, download_size:int, disk_size:int, subject:int):
        self.id=id
        self.input_shape=input_shape
        self.description=description
        self.metadata=metadata
        self.download_size=download_size
        self.disk_size=disk_size
        self.subject=subject

    def summary(self):
        if(self.download_size>1000):
            download_size_format=self.download_size/1024
            size_format="Kb"
            if(self.download_size>1000000):
                download_size_format = download_size_format / 1024
                size_format = "Mb"
                if(self.download_size>1000000000):
                    download_size_format= download_size_format/1024
                    size_format = "Gb"
        if (self.disk_size > 1000):
            disk_size_format = self.disk_size / 1024
            d_size_format = "Kb"
            if (self.download_size > 1000000):
                disk_size_format = disk_size_format / 1024
                d_size_format = "Mb"
                if (self.download_size > 1000000000):
                    disk_size_format = disk_size_format / 1024
                    d_size_format = "Gb"

        return f"Dataset id: {self.id}\nDescription: {self.description}" \
               f"\nInput shape: {self.input_shape}" \
               f"\nMetadata: {self.metadata}" \
               f"\nTamaño descarga: {round(download_size_format,1), size_format}" \
               f"\nTamaño en disco: {round(disk_size_format,1), d_size_format}" \
               f"\nCantidad de subjects: {self.subject}" \

    @abstractmethod
    def get_loader(self)->DatasetLoader:
        pass

class ClassificationDatasetInfo(DatasetInfo):

    def __init__(self, id:str, input_shape:Tuple[int,int,int], metadata:Dict[str, str], description:str, labels:[str], download_size:int , disk_size:int, subject:int):
        super().__init__(id, input_shape, metadata, description, download_size, disk_size, subject)
        self.labels=labels


    def summary(self):
        return super().summary()+f"\nClasses: {len(self.labels)}\n{','.join(self.labels)}"