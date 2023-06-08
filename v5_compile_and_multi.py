import multiprocessing
import os
from collections import defaultdict
import heapq
from baseline import stopwords_set
from compiled.cython_module import cython_read_file, cython_count_words
from utils.tracking import track_performance_profile
import psutil


class MultiProcessingSolution:
    def __init__(self, count_words=cython_count_words, read_file=cython_read_file):
        self.count_words = count_words
        self.read_file = read_file

    @staticmethod
    def top_k(results, k):
        word_counts = defaultdict(int)
        for partial_result in results:
            for word, count in partial_result.items():
                word_counts[word] += count

        return heapq.nlargest(k, word_counts.items(), key=lambda i: i[1])

    def process_file(self, file_name, start, end):
        words = self.read_file(file_name, start, end, stopwords_set)
        return self.count_words(words)

    def process_file_multiprocessing(self, file_name, k=10):
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

        # Create a Pool of subprocesses
        with multiprocessing.Pool() as pool:
            results = pool.starmap(self.process_file, [(
                file_name, start, end) for start, end in ranges])

        top_k = self.top_k(results, k)
        return top_k


v5_solver = MultiProcessingSolution()
