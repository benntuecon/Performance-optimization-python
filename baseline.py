import time
import logging
import cProfile
from collections import defaultdict
import heapq
import nltk

# nltk.download('stopwords')

from nltk.corpus import stopwords

# setup logging
logging.basicConfig(level=logging.INFO)

stopwords_set = set(stopwords.words('english'))


def read_in_chunks(file_object):
    """
    Lazy function (generator) to read a file piece by piece.
    return a tuple of data and time taken to read the data
    """
    while True:
        data = file_object.read()
        if not data:
            break
        yield data


def count_chunk(counter, words):
    for word in words:
        counter[word] += 1


def get_top_k_words(file_name, k):
    word_count = defaultdict(int)

    profiler = cProfile.Profile()
    profiler.enable()

    with open(file_name, 'r') as f:
        for piece in read_in_chunks(f):
            piece = piece.lower()
            words = [word for word in piece.split() if word not in stopwords_set]
            count_chunk(word_count, words)

    # get top k words
    top_k = heapq.nlargest(k, word_count.items(), key=lambda i: i[1])

    profiler.disable()
    profiler.print_stats(sort='time')

    return top_k


# You can call the function like this:
for word, count in get_top_k_words('../dataset/data_2.5GB.txt', 10):
    logging.info(f'{word}: {count:-20}')
