
from baseline import base_solver
from v1_apply_two_pointer import v1_solver
from v3_GPT import v3_solver
from v4_multi import v4_solver
from v5_compile_and_multi import v5_solver
from utils.tracking import track_performance_profile

# from v1_word_count_improvement import v1_solver
# from v2_sorting_improvement import v2_solver

FILES = {
    '50MB': 'small_50MB_dataset.txt',
    '300MB': '../dataset/data_300MB.txt',
    '2.5GB': '../dataset/data_2.5GB.txt',
    '16GB': '../dataset/data_16GB.txt',
}

K = 10


@track_performance_profile
def baseline_exp():
    print('starting base experiment')
    base_solver.top_k(FILES['300MB'], K)


@track_performance_profile
def v1_exp():
    v1_solver.top_k(FILES['300MB'], K)


@track_performance_profile
def v2_exp():
    v2_solver.top_k(FILES['50MB'], K)


@track_performance_profile
def v3_exp():
    print(v3_solver.top_k(FILES['300MB'], K))


@track_performance_profile
def v4_exp():
    print(v4_solver.process_file_multiprocessing(FILES['2.5GB'], K))


@track_performance_profile
def v5_exp():
    print(v5_solver.process_file_multiprocessing(FILES['16GB'], K))


def main():
    # baseline_exp()
    # v1_exp()
    # v1_exp()
    # v2_exp()
    # v3_exp()
    # v4_exp()
    v5_exp()


if __name__ == '__main__':
    print('calling main ...')
    main()
