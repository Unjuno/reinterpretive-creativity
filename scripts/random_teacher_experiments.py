from random import Random
from scripts import run_experiments as e
from scripts.random_teacher_smoke import build_random_teacher as b

def make_noisy_raw_from_teacher(t,seed=0):
 r=Random(seed)
 return {k:({1,-1} if r.random()<.5 else {1}) for k,v in t.items() if v==1}

def run_smoke(seed=0,limit=20):
 t=b(4,seed); raw=make_noisy_raw_from_teacher(t,seed)
 return {
  'random_repair':e.random_repair(t,raw,seed)[0],
  'random_search':e.random_search_baseline(t,raw,seed,limit)[0],
  'local_repair':e.local_repair_search(t,raw,seed,limit)[0],
  'reinterpretation':e.reinterpretation_search(t,raw,seed,limit)[0],
 }
