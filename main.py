import re
import urllib.request
import collections
from typing import List

def get_stop_words() -> List[str]:
    url = "https://gist.github.com/sebleier/554280"
    response = urllib.request.urlopen(url)
    long_txt = response.read().decode()
    stop_words = long_txt.splitlines()
    return stop_words

def get_top_k_words(file_path: str, k: int, stop_words: List[str]) -> List[tuple]:
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '').lower()
        data = re.sub('[^a-z\s]', '', data)

        words = data.split(' ')
        words = [word for word in words if word not in stop_words]

        word_count = collections.Counter(words)
        top_k_words = word_count.most_common(k)

    return top_k_words

# Usage:
stop_words = get_stop_words()
top_k_words = get_top_k_words('small_50MB_dataset.txt', 10, stop_words)
print(top_k_words)
