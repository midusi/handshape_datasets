
from handshape_datasets.datasets import (pugeaultASL,
                                         ciarp,
                                         irish_refactory as _irish,
                                         indian_training as _indian_training,
                                         jsl as _jsl,
                                         nus1 as _nus1,
                                         nus2 as _nus2,
                                         lsa16,
                                         psl as _psl,
                                         rwth)


from typing import Dict
from .dataset_info import DatasetInfo

info = [lsa16.LSA16Info(),
        rwth.RWTHInfo(),
        _irish.IrishInfo(),
        ciarp.CiarpInfo(),
        pugeaultASL.PugeaultASL_AInfo(),
        pugeaultASL.PugeaultASL_BInfo(), _indian_training.Indian_AInfo(),
        _indian_training.Indian_BInfo(),
        _nus1.Nus1Info(), _nus2.Nus2Info(),
        _jsl.JslInfo(), _psl.PslInfo()
        ]

options:Dict[str,DatasetInfo] = {i.id:i for i in info}


# options = {
#     'PugeaultASL_A': pugeaultASL.PugeaultASL_A,
#     #'PugeaultASL_B': pugeaultASL.PugeaultASL_B,
#     'ciarp': ciarp.Ciarp,
#     # 'indian_kinect': indian_training.download_and_extract,
#     # 'isl': irish.download_and_extract,
#     'jsl': _jsl.Jsl,
#     'lsa16': lsa16.LSA16,
#     'nus1': _nus1.Nus1,
#     'nus2': _nus2.Nus2,
#     #'psl': psl.download_and_extract,
#     'rwth': rwth.RWTH
# }
