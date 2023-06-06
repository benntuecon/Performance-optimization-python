# Data Engineering Assignment 1


## Goal 


The task of this assignment is to optimize the performance of reading a huge text tile, do simple cleaning, count to frequency of the words, and return the top k words with highest frequency.

Main issues to take care of:
- The largest file can't fit into memory
- Try to optimize the performance as much as possible

------------------
## Experiments setup 

### Environment
- Device: MacBook Pro M1 14" 2021, CPU 8 cores, 16GB RAM
- Language: Python 3.11 / (Cython) /(Rust)

### Data
- Three text files(.txt file) with different sizes: 300MB, 2.5GB, 16GB

### Baseline
- check `baseline.py` for the baseline implementation
- 


### Performance measurement
- use python `cProfile`  module Profile to measure the performance, and use `pstats` to analyze the result for optimization


------------------
## Optimization methods

For the serial different optimization methods, please check the corresponding folder for details.
1. Identify the Performance Bottlenecks:
   1. check performance of baseline
   2. check IO bound or CPU bound
   3. optimize the significant part

2. Optimize algorithm and data structure
   1. Word counting part:
      1. choosing between `dict`, `defaultdict`, `Counter`, `self-implmented trie`
      2. choosing between `list`, `set`
      3. using two pointers to avoid unnecessary string copy

   2.  Sort part:
       1.  heapq `nlargest`
       2.  `bubble sort` for small k, `k = 10` for example.


3. Leverage Parallel Processing: 
   
   1. try to use multi-threading
      1. `threading`, limited by GIL, not likely to be faster than the baseline, since the program is CPU bound.

   2. try to use multi-processing:
      1. `multiprocessing`, higher overhead but can use multiple cores to do the counting part, can be faster than the baseline. 
         1. `Pool` with `map` or `apply_async`
         2. Pass the offset variable to each process, and let each process read the file from the offset, and do the counting part.

4. further optimization methods:
   1. compiled python code `cython`, `numba`
   2. use low level lang like `Rust` to implement the core part
   3. garbage collection `gc`
------------------
## Results
#### Initial results:

