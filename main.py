from utils.tracking import track_performance_profile

from baseline import base_solver
from v1_word_count_imporvement import v1_solver


FILES = {
    '50MB': 'small_50MB_dataset.txt',
    '300MB': '../dataset/data_300MB.txt',
    '2.5GB': '../dataset/data_2.5GB.txt',
    '16GB': '../dataset/data_16GB.txt',
}

K = 10


@track_performance_profile
def baseline_exp():
    base_solver.top_k(FILES['50MB'], K)


@track_performance_profile
def v1_exp():
    v1_solver.top_k(FILES['50MB'], K)


def main():
    baseline_exp()


if __name__ == '__main__':
    main()
