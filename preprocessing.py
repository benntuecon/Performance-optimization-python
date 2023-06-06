import time
from collections import defaultdict
import heapq
import nltk

# nltk.download('stopwords')

from nltk.corpus import stopwords


stopwords_set = stopwords.words('english')

def read_in_chunks(file_object ):
    """
    Lazy function (generator) to read a file piece by piece.
    return a tuple of data and time taken to read the data
    """
    while (start_time:= time.perf_counter()) and (data:=file_object.read()):
        yield data, time.perf_counter() - start_time

def get_top_k_words(file_name, k):
    word_count = defaultdict(int)

    total_io_time = 0
    total_cpu_time = 0
    total_cpu_time_sort = 0

    with open(file_name) as f:
        for piece, io_time in read_in_chunks(f):
            total_io_time += io_time
            
            # Start time of CPU operation
            start_cpu_time = time.perf_counter()

            piece = piece.lower()
            for w in piece.split():
                if w not in stopwords_set:
                    word_count[w] += 1
            # End time of CPU operation
            end_cpu_time = time.perf_counter()

            # Update total CPU time
            total_cpu_time += (end_cpu_time - start_cpu_time)
                
    # get top k words
    start_cpu_time = time.perf_counter()
    top_k = heapq.nlargest(k, word_count.items(), key=lambda i: i[1])
    end_cpu_time = time.perf_counter()
    total_cpu_time_sort += (end_cpu_time - start_cpu_time)

    print('#' * 20)
    print(f'Total I/O time: {total_io_time} seconds')
    print(f'Total CPU time: {total_cpu_time} seconds')
    print(f'Total CPU sort time: {total_cpu_time_sort} seconds')
    print('#' * 20)

    return top_k

# You can call the function like this:
for word, count in get_top_k_words('dataset/data_300MB.txt', 10):
    print(f'{word}: {count:-20}')
