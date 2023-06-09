import multiprocessing
import os
from collections import defaultdict
import heapq
from baseline import stopwords_set
from compiled.cython_module import call_cython_read_file as cython_read_file
from utils.tracking import track_performance_profile
import psutil


class MultiProcessingSolution:
    def __init__(self,  read_file=cython_read_file):
        self.read_file = read_file

    @staticmethod
    def top_k(results, k):
        word_counts = defaultdict(int)
        for partial_result in results:
            print(list(partial_result.items())[:100])
            for word, count in partial_result.items():
                word_counts[word] += count

        return heapq.nlargest(k, word_counts.items(), key=lambda i: i[1])

    def process_file_multiprocessing(self, file_name: str, k: int = 10):
        file_size = os.path.getsize(file_name)
        available_ram = psutil.virtual_memory().available * 0.95
        cpu_count = multiprocessing.cpu_count()

        # Calculate the range for each process based on available RAM
        chunk_size = min(available_ram, file_size) // cpu_count // 1024 // 1024
        chunk_size *= (1024 * 1024)
        num_chunks = file_size // (chunk_size)

        ranges = [(i * chunk_size, (i + 1) * chunk_size)
                  for i in range(int(num_chunks))]
        # Make sure the last chunk reads till the end of file
        ranges[-1] = (ranges[-1][0], file_size)

        file_name_bytes = file_name.encode('utf-8')

        stopwords_set_bytes = {word.encode('utf-8') for word in stopwords_set}

        # Create a Pool of subprocesses
        with multiprocessing.Pool() as pool:
            results = pool.starmap(self.read_file, [(
                file_name, start, end, stopwords_set_bytes) for start, end in ranges])

        top_k = self.top_k(results, k)
        return top_k


v5_solver = MultiProcessingSolution()
