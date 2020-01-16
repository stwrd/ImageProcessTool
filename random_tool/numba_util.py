from numba import jit
import numpy as np
import time

x = np.arange(100).reshape(10, 10)

@jit(nopython=True)
def go_fast(a): # Function is compiled and runs in machine code
    trace = 0
    for i in range(a.shape[0]):
        trace += np.tanh(a[i, i])
    return a + trace

def go_fast1(a):
    trace = 0
    for i in range(a.shape[0]):
        trace += np.tanh(a[i, i])
    return a + trace
# DO NOT REPORT THIS... COMPILATION TIME IS INCLUDED IN THE EXECUTION TIME!
start = time.time()
go_fast(x)
go_fast1(x)
end = time.time()
# print("Elapsed (with compilation) = %s" % (end - start))

# NOW THE FUNCTION IS COMPILED, RE-TIME IT EXECUTING FROM CACHE
start = time.time()
for i in range(1000):
    go_fast(x)
end = time.time()
jit_time = end - start
print("Elapsed (after compilation) jit = %s" % (jit_time))

start = time.time()
for i in range(1000):
    go_fast1(x)
end = time.time()
non_jit_time = end - start
print("Elapsed (after compilation) no jit = %s" % (non_jit_time))

faster = non_jit_time/jit_time
print("jit/no_jit = %s" % (faster))