from functools import wraps

def coroutine(func):
    """装饰器：向前执行到第一个`yield`表达式，预激`func`""" 
    @wraps(func) 
    def primer(*args,**kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return primer


"""增加装饰器之前, 会抛出异常TypeError: can't send non-None value to a just-started generator"""
@coroutine
def averager():
    total = 0.0 
    count = 0 
    average = None 
    while True: 
        term = yield average
        total += term
        count += 1
        average = total/count
        print(average)
if __name__ == '__main__':
    coro_avg = averager()
    from inspect import getgeneratorstate
    getgeneratorstate(coro_avg)
    coro_avg.send(10)
    coro_avg.send(30)
    coro_avg.send(5)
