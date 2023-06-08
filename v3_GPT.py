from collections import Counter
from threading import Thread
from queue import Queue
import heapq
from baseline import stopwords_set


class ImprovedSolution:
    def __init__(self):
        self.queue = Queue()

    def read_file(self, file_name):
        with open(file_name, 'r') as f:
            while True:
                data = f.read(1024 * 1024)  # read in chunks of 1MB
                if not data:
                    break
                self.queue.put(data)

    def count_words(self, word_counts):
        while not self.queue.empty():
            piece = self.queue.get().lower()
            words = [word for word in piece.split() if word not in stopwords_set]
            word_counts += Counter(words)

    def top_k(self, file_name, k=10):
        word_counts = Counter()

        # Start a thread for reading the file
        reader_thread = Thread(target=self.read_file, args=(file_name,))
        reader_thread.start()

        # Wait for the reader thread to finish
        reader_thread.join()

        # Count the words
        self.count_words(word_counts)

        # Get top k words
        return heapq.nlargest(k, word_counts.items(), key=lambda i: i[1])


v3_solver = ImprovedSolution()
