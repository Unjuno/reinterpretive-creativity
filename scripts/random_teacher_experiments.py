from random import Random
from scripts import run_experiments as e
from scripts.random_teacher_smoke import build_random_teacher as b

def make_noisy_raw_from_teacher(t,seed=0):
 r=Random(seed);return {k:({1,-1} if r.random()<.5 else {1}) for k,v in t.items() if v==1}

def run_smoke():
 t=b(4,0);r=make_noisy_raw_from_teacher(t);return e.random_repair(t,r,0)[0]
