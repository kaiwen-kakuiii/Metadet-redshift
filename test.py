import sys
import numpy as np
import schwimmbad
import multiprocessing
import logging
import time
import fitsio
from metadetect.metadetect import Metadetect
from config import CONFIG
from run_preamble import get_shear_meas_config

(SWAP12, CUT_INTERP, DO_METACAL_MOF, DO_METACAL_SEP,
 DO_METACAL_TRUEDETECT,
 SHEAR_MEAS_CONFIG, SIM_CLASS) = get_shear_meas_config()


def _meas_shear(res):
    return measure_shear_metadetect(
        res, s2n_cut=10, t_ratio_cut=1.2, cut_interp=CUT_INTERP)

def _add_shears(cfg, plus=True):
    g1 = 0.02
    g2 = 0.0

    if not plus:
        g1 *= -1

    if SWAP12:
        g1, g2 = g2, g1

    cfg.update({'g1': g1, 'g2': g2})


def _run_sim(seed):
    config = {}
    config.update(SHEAR_MEAS_CONFIG)

    try:
        # pos shear
        rng = np.random.RandomState(seed=seed + 1000000)
        _add_shears(CONFIG, plus=True)
        if SWAP12:
            assert CONFIG['g1'] == 0.0
            assert CONFIG['g2'] == 0.02
        else:
            assert CONFIG['g1'] == 0.02
            assert CONFIG['g2'] == 0.0
        sim = SIM_CLASS(rng=rng, **CONFIG)
        mbobs = sim.get_mbobs()
        md = Metadetect(config, mbobs, rng)
        md.go()
        
        pres = _meas_shear(md.result)
        
        
        # neg shear
        rng = np.random.RandomState(seed=seed + 1000000)
        _add_shears(CONFIG, plus=False)
        if SWAP12:
            assert CONFIG['g1'] == 0.0
            assert CONFIG['g2'] == -0.02
        else:
            assert CONFIG['g1'] == -0.02
            assert CONFIG['g2'] == 0.0
        sim = SIM_CLASS(rng=rng, **CONFIG)

        mbobs = sim.get_mbobs()
        md = Metadetect(config, mbobs, rng)
        md.go()
        
        mres = _meas_shear(md.result)
        
        retvals = (pres, mres)
        
    except Exception as e:
        print(repr(e))
        retvals = (None, None)
        
    return retvals

print('running metadetect', flush=True)
print('config:', CONFIG, flush=True)
print('swap 12:', SWAP12)

outputs = [_run_sim(0)]

#pres, mres = zip(*outputs)
#pres, mres = cut_nones(pres, mres)
