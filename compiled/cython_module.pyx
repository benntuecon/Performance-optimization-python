cimport cython

@cython.boundscheck(False)  
@cython.wraparound(False)  
cpdef list cython_read_file(str file_name, long start, long end, set stopwords_set):
    with open(file_name, 'r') as f:
        f.seek(start)
        data = f.read(end - start).lower()
        return [d for d in data.split() if d not in stopwords_set]

@cython.boundscheck(False) 
@cython.wraparound(False)  
cpdef dict cython_count_words(list words):
    cdef dict word_counts = {}
    cdef str word
    for word in words:
        if word not in word_counts:
            word_counts[word] = 1
        else:
            word_counts[word] += 1
    return word_counts
