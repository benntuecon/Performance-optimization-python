from baseline import BaselineSolution
from baseline import read_file, count_words, sorting, stopwords_set


v1_solver = ...


class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def get_count_and_add(self, word: str) -> int:
        cur = self.root
        for c in word:
            if c not in cur.children:
                cur.children[c] = TrieNode()
            cur = cur.children[c]

        cur.count += 1
        return cur.count
    
    def traverse(self):
        word = []
        for self.root.c


class TrieVersionSolution(BaselineSolution):
    def __init__(self, read_file_func, count_words_func, sorting_func) -> None:
        super().__init__(read_file_func, count_words_func, sorting_func)

    def top_k(self, file_name, k=10):
        word_counts = Trie()

        with open(file_name, 'r') as f:
            for piece in self.read_file_func(f):
                piece = piece.lower()
                words = [word for word in piece.split(
                ) if word not in stopwords_set]
                self.count_words_func(word_counts, words)
        # get top k words
        top_k = self.sorting_func(k, word_counts)
        return top_k



