import timeit
from functools import wraps
import cProfile


def log_path(kwargs): return f'logs/{kwargs}'


def add_execute_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        wrapper.__doc__ += f'\n ** The time spend of the execution will be append to the function result**\n'
        return result, elapsed_time
    return wrapper


def track_performance_profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        profiler = cProfile.Profile()
        profiler.enable()

        result = func(*args, **kwargs)

        profiler.disable()
        profiler.print_stats(sort='time')
        profiler.dump_stats(log_path(kwargs=kwargs))

        return result
    return wrapper
