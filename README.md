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
      2. using two pointers to avoid unnecessary string copy

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

### Baseline results (300MB file):
#### 291281 function calls in ***13.753 seconds***

Here is the given text transformed into a Markdown table with an additional column representing the percentage of total time:

| ncalls | tottime | percall | cumtime | percall | tottime (%) | filename:lineno(function) |
|--------|---------|---------|---------|---------|-------------|---------------------------|
| 1      | 8.001   | 8.001   | 8.001   | 8.001   | 58.19% | sandbox.py:39(\<listcomp>) |
| 1      | 3.026   | 3.026   | 3.026   | 3.026   | 22.00% | {method 'split' of 'str' objects} |
| 1      | 1.761   | 1.761   | 1.761   | 1.761   | 12.80% | {method 'lower' of 'str' objects} |
| 2      | 0.596   | 0.298   | 0.817   | 0.408   | 4.34% | {method 'read' of '_io.TextIOWrapper' objects} |
| 2      | 0.220   | 0.110   | 0.220   | 0.110   | 1.60% | {built-in method _codecs.utf_8_decode} |
| 1      | 0.096   | 0.096   | 0.118   | 0.118   | 0.70% | heapq.py:523(nlargest) |
| 2      | 0.028   | 0.014   | 0.845   | 0.423   | 0.20% | sandbox.py:18(read_in_chunks) |

Note: The percentages in the 'tottime (%)' column were calculated as follows: `tottime for each function` / `total time of all functions (13.753 seconds)` * 100%. The percentages are rounded to two decimal places.

### Baseline results (2.5GB file): 
#### 3476811 function calls in ***712.093 seconds***

| ncalls | tottime | percall | cumtime | percall | tottime (%) | filename:lineno(function) |
|--------|---------|---------|---------|---------|-------------|---------------------------|
| 1      | 284.289 | 284.289 | 284.289 | 284.289 | 39.91% | sandbox.py:30(count_chunk) |
| 1      | 170.100 | 170.100 | 170.100 | 170.100 | 23.87% | sandbox.py:44(\<listcomp>) |
| 1      | 86.611  | 86.611  | 86.958  | 86.958  | 12.16% | heapq.py:523(nlargest) |
| 1      | 57.762  | 57.762  | 57.762  | 57.762  | 8.11%  | {method 'lower' of 'str' objects} |
| 1      | 56.148  | 56.148  | 56.148  | 56.148  | 7.88%  | {method 'split' of 'str' objects} |
| 2      | 39.774  | 19.887  | 56.737  | 28.369  | 5.58%  | {method 'read' of '_io.TextIOWrapper' objects} |
| 2      | 16.959  | 8.480   | 16.959  | 8.480   | 2.38%  | {built-in method _codecs.utf_8_decode} |

Note: The percentages in the 'tottime (%)' column were calculated as follows: `tottime for each function` / `total time of all functions (712.093 seconds)` * 100%. The percentages are rounded to two decimal places.

### Baseline results (16GB file): N/A (too slow to finish)
----

### Two pointers optimization results (50MB file):

### Two pointers optimization results (300MB file):
---
### multiprocessing results (16GB file): (FAILED out of memory)
### multiprocessing optimization results (50MB file):
#### 199425 function calls (199368 primitive calls) in ***1.016*** seconds

| ncalls | tottime | percall | cumtime | percall | tottime (%) | filename:lineno(function) |
|--------|---------|---------|---------|---------|-------------|---------------------------|
| 19     | 0.717   | 0.038   | 0.717   | 0.038   | 66.77% | {method 'acquire' of '_thread.lock' objects} |
| 1      | 0.165   | 0.165   | 0.222   | 0.222   | 15.35% | v4_multi.py:22(top_k) |
| 1      | 0.041   | 0.041   | 0.057   | 0.057   | 3.81% | heapq.py:523(nlargest) |
| 9      | 0.027   | 0.003   | 0.027   | 0.003   | 2.51% | {built-in method _posixsubprocess.fork_exec} |
| 194188 | 0.016   | 0.000   | 0.016   | 0.000   | 1.49% | v4_multi.py:28(<lambda>) |
| 45     | 0.014   | 0.000   | 0.014   | 0.000   | 1.30% | {built-in method posix.waitpid} |
| 1      | 0.006   | 0.006   | 1.016   | 1.016   | 0.56% | main.py:45(v4_exp) |


### multiprocessing results (300MB file):
#### 296482 function calls (296425 primitive calls) in ***3.194*** seconds
| ncalls | tottime | percall | cumtime | percall | tottime (%) | filename:lineno(function) |
|--------|---------|---------|---------|---------|-------------|---------------------------|
| 19     | 2.699   | 0.142   | 2.699   | 0.142   | 84.29% | {method 'acquire' of '_thread.lock' objects} |
| 1      | 0.314   | 0.314   | 0.404   | 0.404   | 9.81% | v4_multi.py:22(top_k) |
| 1      | 0.064   | 0.064   | 0.090   | 0.090   | 2.00% | heapq.py:523(nlargest) |
| 291235 | 0.026   | 0.000   | 0.026   | 0.000   | 0.81% | v4_multi.py:28(<lambda>) |
| 9      | 0.026   | 0.003   | 0.026   | 0.003   | 0.81% | {built-in method _posixsubprocess.fork_exec} |
| 47     | 0.026   | 0.001   | 0.026   | 0.001   | 0.81% | {built-in method posix.waitpid} |
| 1      | 0.009   | 0.009   | 3.194   | 3.194   | 0.28% | main.py:45(v4_exp) |

### multiprocessing results (2.5GB file):
####  3482003 function calls (3481946 primitive calls) in ***431.212*** seconds
| ncalls | tottime | percall | cumtime | percall | tottime (%) | filename:lineno(function) |
|--------|---------|---------|---------|---------|-------------|---------------------------|
| 19     | 424.825 | 22.359  | 424.825 | 22.359  | 98.46% | {method 'acquire' of '_thread.lock' objects} |
| 1      | 5.099   | 5.099   | 6.165   | 6.165   | 1.18% | v4_multi.py:22(top_k) |
| 1      | 0.742   | 0.742   | 1.066   | 1.066   | 0.17% | heapq.py:523(nlargest) |
| 3476762| 0.324   | 0.000   | 0.324   | 0.000   | 0.08% | v4_multi.py:28(<lambda>) |
| 1      | 0.114   | 0.114   | 431.212 | 431.212 | 0.03% | main.py:45(v4_exp) |
| 9      | 0.028   | 0.003   | 0.028   | 0.003   | 0.01% | {built-in method _posixsubprocess.fork_exec} |
| 46     | 0.025   | 0.001   | 0.025   | 0.001   | 0.01% | {built-in method posix.waitpid} |


### multiprocessing results (16GB file): (FAILED out of memory)
### compiled optimization results 
#### (50MB file) 199434 function calls (199377 primitive calls) in ***0.967*** seconds
####  (300MB file): 296482 function calls (296425 primitive calls) in ***2.743*** seconds


#### (2.5GB file): 
#### 
#### (16GB file): 
#### 9479072 function calls (9479015 primitive calls) in ***3730.872*** seconds
