import logging
import cProfile
from collections import defaultdict
import heapq
from typing import Callable

# uncomment this for the first time run
# nltk.download('stopwords')
from nltk.corpus import stopwords

# setup logging
logging.basicConfig(level=logging.INFO)

# load the stopwords and turn it into a hash-set for better performance check existence check
stopwords_set = set(stopwords.words('english'))


def read_file(file_object):
    """
    Lazy function (generator) to read a file piece by piece.
    return a single chunk of data
    """
    while True:
        data = file_object.read()
        if not data:
            break
        yield data


def count_words(counter, words):
    for word in words:
        counter[word] += 1


def get_top_k_words(file_name, k):
    word_count = defaultdict(int)
    with open(file_name, 'r') as f:
        for piece in read_file(f):
            piece = piece.lower()
            words = [word for word in piece.split() if word not in stopwords_set]
            count_words(word_count, words)

    # get top k words
    top_k = heapq.nlargest(k, word_count.items(), key=lambda i: i[1])
    return top_k


def sorting(k, word_counts):
    return heapq.nlargest(
        k, word_counts.items(), key=lambda i: i[1])


# You can call the function like this:
for word, count in get_top_k_words('../dataset/data_2.5GB.txt', 10):
    logging.info(f'{word}: {count:-20}')


class Solution:
    read_file_func: Callable
    count_words_func: Callable
    sorting_func: Callable

    def top_k(self):
        ...


class BaselineSolution(Solution):
    def top_k(self, file_name, k=10):
        word_counts = defaultdict(int)
        with open(file_name, 'r') as f:
            for piece in self.read_file(f):
                piece = piece.lower()
                words = [word for word in piece.split(
                ) if word not in stopwords_set]
                self.count_words(word_counts, words)
        # get top k words
        top_k = self.sorting(k, word_counts)
        return top_k


base_solver = BaselineSolution(
    read_file,
    count_words,
    sorting
)
