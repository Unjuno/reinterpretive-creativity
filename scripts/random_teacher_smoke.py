from random import Random
try:
    from scripts import run_experiments as exp
except ModuleNotFoundError:
    import run_experiments as exp

def build_random_teacher(node_count=4, seed=0):
    rng=Random(seed)
    nodes=exp.make_nodes(node_count)
    edges=exp.all_edges(nodes)
    teacher={e:0 for e in edges}
    teacher[rng.choice(edges)]=1
    return teacher
