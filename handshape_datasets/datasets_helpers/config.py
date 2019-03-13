
from . import (aslA as _aslA,
                               aslB as _aslB,
                               ciarp as _ciarp,
                               irish as _irish,
                               indian_training as _indian_training,
                               jsl as _jsl,
                               nus1 as _nus1,
                               nus2 as _nus2,
                               psl as _psl,
                               rwth as _rwth)


options = {
    #'aslA': aslA.AslA,
    #'aslB': aslB.AslB,
    'ciarp': _ciarp.Ciarp,
    # 'indian_kinect': indian_training.download_and_extract,
    # 'isl': irish.download_and_extract,
    'jsl': _jsl.Jsl,
    # 'lsa16': lsa16.download_and_extract,
    'nus1': _nus1.Nus1,
    'nus2': _nus2.Nus2,
    # 'psl': psl.download_and_extract,
    # 'pugeault': pugeault.download_and_extract,
    'rwth-phoenix': _rwth.Rwth
}