from clockdeco import clock
@clock
def fibonacci_v1(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

import functools
@functools.lru_cache() # ➊
@clock # ➋
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)
if __name__=='__main__':
    print('> ', fibonacci(6))
