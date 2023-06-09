# distutils: language=c++

from libcpp.string cimport string
from libcpp.unordered_set cimport unordered_set
from libc.stdio cimport fopen, fclose, fseek, fgets, FILE, SEEK_SET
from libc.stdlib cimport malloc, free
from libc.string cimport strtok, strcmp, strlen
from libcpp.vector cimport vector

cimport cython

cdef extern from "ctype.h":
    int isupper(int c) nogil
    int tolower(int c) nogil

cdef char* to_lower(char* s) nogil:
    cdef size_t i
    for i in range(strlen(s)):
        if isupper(s[i]):
            s[i] = tolower(s[i])
    return s

cdef struct WordCounts:
    char* word
    long count

@cython.boundscheck(False)
@cython.wraparound(False)
cdef vector[WordCounts]* cython_read_file(char* file_name, long start, long end, unordered_set[string] stopwords_set) nogil:
    cdef:
        FILE* file = fopen(file_name, "r")
        long size = end - start
        char* buffer = <char*> malloc(size + 1)
        char* token
        vector[WordCounts]* word_counts = new vector[WordCounts]()
        WordCounts word_count
        long i

    if file == NULL:
        return NULL

    if buffer == NULL:
        return NULL

    fseek(file, start, SEEK_SET)
    fgets(buffer, size + 1, file)
    fclose(file)

    token = strtok(buffer, " \n")
    while token != NULL:
        token = to_lower(token)
        if not stopwords_set.count(token):
            for i in range(word_counts[0].size()):
                if strcmp((<WordCounts>word_counts[0][i]).word, token) == 0:
                    (<WordCounts>word_counts[0][i]).count += 1
                    break
            else:
                word_count.word = token
                word_count.count = 1
                word_counts[0].push_back(word_count)
        token = strtok(NULL, " \n")

    free(buffer)

    return word_counts

cpdef dict call_cython_read_file(str file_name, long start, long end, unordered_set[string] stopwords_set):
    cdef vector[WordCounts]* word_counts
    word_counts = cython_read_file(file_name.encode(), start, end, stopwords_set)
    if word_counts == NULL:
        raise RuntimeError("File not found or memory allocation failed")
    return {word_counts[0][i].word.decode('utf-8'): word_counts[0][i].count for i in range(word_counts.size())}
