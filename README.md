# Data Engineering Assignment 1

The task of this assignment is to optimize the performance of reading a huge text tile, do simple cleaning, count to frequency of the words, and return the top k words with highest frequency.

Main issues to take care of:
- File can't fit into memory
- IO bound or CPU bound
- Try to optimize the performance as much as possible


1. baseline 
   1. check performance of baseline
   2. check IO bound or CPU bound
   3. optimize the significant part
2. Optimize algorithm and data structure
   1. use `Counter` instead of `dict`
   2. use `heap` instead of `sort`
   3. use `generator` instead of `list`
   4. 
   
3. try to use JIT compiler
    1. `numba`
    2. `cython`
4. try to use multi-threading
   1. `threading`, limited by GIL

5. try to use multi-processing:
   1. `multiprocessing`, higher overhead but can use multiple cores 


