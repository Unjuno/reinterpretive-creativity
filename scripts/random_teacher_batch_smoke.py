from scripts.random_teacher_experiments import run_smoke


def run_batch(seeds=range(3), limit=20):
    return [{'seed': seed, 'scores': run_smoke(seed, limit)} for seed in seeds]


def summarize(rows):
    return {
        method: sum(row['scores'][method] for row in rows) / len(rows)
        for method in rows[0]['scores']
    }


if __name__ == '__main__':
    rows = run_batch()
    print(rows)
    print(summarize(rows))
