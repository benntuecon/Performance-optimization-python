from collections import defaultdict, Counter
from baseline import BaselineSolution, stopwords_set


class TwoPointerSolution(BaselineSolution):

    @staticmethod
    def count_words(words):
        """ two pointer solution

        Args:
            word_counts (dict): inplace update
            words (str): a single piece of data, using two pointers to find the word
        """
        n = len(words)
        start = end = 0
        while end < n:
            while end < n and words[end] != ' ':
                end += 1
            # word_counts[words[start:end]] += 1
            if words[start:end] not in stopwords_set:
                yield words[start:end]
            start = end = end + 1

    def top_k(self, file_name, k=10):
        word_counts = defaultdict(int)
        with open(file_name, 'r') as f:
            for piece in self.read_file(f):
                piece = piece.lower()
                for word in self.count_words(piece):
                    word_counts[word] += 1

        # get top k words
        top_k = self.sorting(k, word_counts)
        return top_k


v1_solver = TwoPointerSolution()
