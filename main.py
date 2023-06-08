
from baseline import base_solver
from v1_apply_two_pointer import v1_solver
from v3_GPT import v3_solver
from v4_multi import v4_solver
from v5_compile_and_multi import v5_solver
from utils.tracking import track_performance_profile
import argparse

# from v1_word_count_improvement import v1_solver
# from v2_sorting_improvement import v2_solver

FILES = {
    '50': 'small_50MB_dataset.txt',
    '300': '../dataset/data_300MB.txt',
    '2-5': '../dataset/data_2.5GB.txt',
    '16': '../dataset/data_16GB.txt',
}

K = 10


@track_performance_profile
def baseline_exp(file_code='50'):
    print(
        base_solver.top_k(FILES[file_code], K)
    )


@track_performance_profile
def v1_exp(file_code='50'):
    print(v1_solver.top_k(FILES[file_code], K))


@track_performance_profile
def v2_exp(file_code='50'):
    print(v1_solver.top_k(FILES[file_code], K))


@track_performance_profile
def v3_exp(file_code='50'):
    print(v1_solver.top_k(FILES[file_code], K))


@track_performance_profile
def v4_exp(file_code='50'):
    print(v4_solver.process_file_multiprocessing(FILES[file_code], K))


@track_performance_profile
def v5_exp(file_code='50'):
    print(v5_solver.process_file_multiprocessing(FILES[file_code], K))


def main():
    # baseline_exp()
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--exp', type=str, default='v5')
    argparser.add_argument('--file_code', type=str, default='50')
    args = argparser.parse_args()

    match args.exp:
        case 'baseline':
            baseline_exp(args.file_code)
        case 'v1':
            v1_exp(args.file_code)
        case 'v2':
            v2_exp(args.file_code)
        case 'v3':
            v3_exp(args.file_code)
        case 'v4':
            v4_exp(args.file_code)
        case 'v5':
            v5_exp(args.file_code)
        case _:
            print('Invalid exp name')


if __name__ == '__main__':
    print('calling main ...')
    main()
