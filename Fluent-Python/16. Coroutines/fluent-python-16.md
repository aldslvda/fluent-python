## Fluent Python 
### Chapter 16. Coroutines
### 第十六章: 协程

在协程中， 不管数据如何流动，yield 都是一种流程控制工具。

#### 16.1 生成器如何进化成协程
生成器的调用方可以使用 .send(...) 方法发送数据，发送的数据会成为生成器函数中 yield 表达式的值。因此，生成器可以作为协程使用。协程是指一个过程，这个过程与调用方协作，产出由调用方提供的值。

除了 .send(...) 方法，PEP 342 还添加了 .throw(...) 和 .close() 方法：前者的作用是让调用方抛出异常，在生成器中处理；后者的作用是终止生成器。

#### 16.2 用于协程的生成器的基本行为

```python
>>> def simple_coroutine(): 
...     print('-> coroutine started') 
...     x = yield 
...     print('-> coroutine received:', x) ...

>>> my_coro = simple_coroutine()

>>> my_coro 
<generator object simple_coroutine at 0x100c2be10>

>>> next(my_coro) 

-> coroutine started

>>> my_coro.send(42) 

-> coroutine received: 42 
Traceback (most recent call last):
    ...
StopIteration
```

协程可以身处四个状态中的一个。当前状态可以使用 inspect.getgeneratorstate(...) 函数确定，该函数会返回下述字符串中的一个。    
- 'GEN_CREATED'    
  等待开始执行。 
- 'GEN_RUNNING'    
  解释器正在执行。   
    只有在多线程应用中才能看到这个状态。此外，生成器对象在自己身上调用 getgeneratorstate 函数也行，不过这样做没什么用。
- 'GEN_SUSPENDED'     
  在 yield 表达式处暂停。 
- 'GEN_CLOSED'      
    执行结束。

> 因为 send 方法的参数会成为暂停的 yield 表达式的值，所以，仅当协程处于暂停状态时 才能调用 send 方法





