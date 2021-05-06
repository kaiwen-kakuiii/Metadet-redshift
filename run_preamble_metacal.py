from mdetsims import (TEST_METACAL_SEP_CONFIG)
from mdetsims import End2EndSim, Sim


def get_shear_meas_config():
    """get config info for shear measurement"""
    # simulation and measurement config stuff
    try:
        from config import SWAP12
    except ImportError:
        SWAP12 = False

    try:
        from config import CUT_INTERP
    except ImportError:
        CUT_INTERP = False

    # set the config for the shear meas algorithm
    try:
        from config import DO_METACAL_SEP
    except ImportError:
        DO_METACAL_SEP = False


    SHEAR_MEAS_CONFIG = TEST_METACAL_SEP_CONFIG

    try:
        from config import SHEAR_MEAS_CONFIG
    except ImportError:
        pass

    try:
        from config import DO_END2END_SIM
    except ImportError:
        DO_END2END_SIM = False

    if DO_END2END_SIM:
        SIM_CLASS = End2EndSim
    else:
        SIM_CLASS = Sim

    return (
        SWAP12, CUT_INTERP, SHEAR_MEAS_CONFIG, SIM_CLASS)
