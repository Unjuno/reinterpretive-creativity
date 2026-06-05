"""Random teacher smoke helpers."""
from random import Random
try:
    from scripts import run_experiments as exp
except ModuleNotFoundError:
    import run_experiments as exp  # type: ignore[no-redef]

def build_random_teacher(node_count=4, seed=0, edge_rate=0.35):
    rng=Random(seed); nodes=exp.make_nodes(node_count); edges=exp.all_edges(nodes)
    teacher={edge