from scripts.random_teacher_experiments import run_smoke


def run_batch(seeds=range(3), limit=20):
    return [{'seed': seed, 'scores': run_smoke(seed, limit)} for seed in seeds]


if __name__ == '__main__':
    print(run_batch())
