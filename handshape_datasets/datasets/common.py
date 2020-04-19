from ..dataset_info import DatasetInfo,ClassificationDatasetInfo
from ..dataset_loader import DatasetLoader
import os
import logging
import numpy as np
from skimage import io
from pathlib import Path
from shutil import rmtree
from os import listdir
from handshape_datasets.datasets.utils import download_bigger_file,download_file,download_file_over_ftp,download_file_content_as_text,download_from_drive,extract_tar,extract_zip