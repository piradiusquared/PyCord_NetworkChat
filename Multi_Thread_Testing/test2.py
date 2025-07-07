from multiprocessing import Pool
import time

count = 50000000
def countdown(n):
    while n>0:
        n -= 1

pool = Pool(processes=2)
start = time.time()
r1 = pool.apply_async(countdown, [count])
r2 = pool.apply_async(countdown, [count])
pool.close()
pool.join()
end = time.time()
print('Time taken in seconds -', end - start)
