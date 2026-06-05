"""Random teacher smoke helpers."""
from __future__ import annotations
from random import Random
try:
    from scripts import run_experiments as exp
except ModuleNotFoundError:
    import run_experiments as exp  # type: ignore[no-redef]

def build_random_teacher(node_count:int=4, seed:int=0, edge_rate:float=0.35)->exp.Model:
    rng=Random(seed)
    nodes=exp.make_nodes(node_count)
    edges=exp.all_edges(nodes)
    teacher={edge:0 for edge in edges}
    for edge in edges:
        if rng.random()<edge_rate:
            teacher[edge]=1
    if not any(v==1 for v in teacher.values()):
        teacher[rng.choice(edges)]=1
    return teacher

def make_noisy_raw_from_teacher(teacher:exp.Model, seed:int=0)->exp.RawModel:
    rng=Random(seed+1)
    raw:exp.RawModel={}
    for edge,value in teacher.items():
        if value==1:
            raw[edge]={1}
            if rng.random()<0.35:
                raw[edge].add(-1)
    if not exp.has