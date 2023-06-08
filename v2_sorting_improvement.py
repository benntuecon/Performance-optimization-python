from baseline import BaselineSolution


class SortingSolution(BaselineSolution):
    @staticmethod
    def sorting(k, words):
        n = len(words)
        for i in range(k):
            # Perform bubble sort for k iterations
            for j in range(n - i - 1):
                if words[j][1] > words[j + 1][1]:
                    words[j], words[j + 1] = words[j + 1], words[j]
        return words[n - k:]  # Return the top k elements


v2_solver = SortingSolution()
