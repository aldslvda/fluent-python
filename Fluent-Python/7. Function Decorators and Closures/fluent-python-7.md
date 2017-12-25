+++
topics = ["Python"]
description = "Python中的装饰器和函数闭包"
draft = false
date = "2017-12-26T00:51:47+08:00"
title = "Fluent Python 第七章小结"
tags = ["Python","装饰器","闭包","变量作用域"]
+++

## Fluent Python ##
### Chapter 7. Function Decorators and Closures
### 第七章: 函数装饰器和函数闭包

函数装饰器使用特殊的标记增强函数，要想掌握装饰器，首先要理解函数闭包。  
nonlocal 是在Python3 中引入的保留关键字，如果要使用函数闭包和装饰器，也必须要了解nonlocal。    
另外，闭包同时也是函数式编程和回调式异步编程的基础。   
这一张要讨论的话题:    
基础知识：    

- python 计算装饰器句法
- python 如何判断变量是否是局部的
- 闭包存在的原因和工作原理
- nonlocal 可以解决的问题

进一步探讨装饰器:

- 实现行为良好的装饰器
- 标准库中有用的装饰器
- 实现参数化装饰器

#### 7.1 装饰器基础知识

装饰器是一个可调用的对象，它的参数是另一个函数（被装饰的函数），装饰器可能会将输入的函数进行处理返回结果，或者将其替换成另一个函数或者可调用对象。     
下面是一个例子, 假设有一个名为decorate的装饰器:

```python
@decorate
def target():
    print('running target()') 

# 等价于下面的写法
target = decorate(target())

```    
上述两段代码得到的target函数都是经过decrate处理过的, 下面的控制台会话证明了这点:   

```python   
>>> def deco(func):
...     def inner():
...         print('running inner()')
...     return inner
...
>>> @deco
... def target():
...     print('running target()')
...
>>> target()
running inner()
>>> target
<function deco.<locals>.inner at 0x10063b598>
```     

可以看到target 已经被替换成了inner,严格来说target现在是inner的引用。       

#### 7.2 Python何时执行装饰器    
装饰器的一大特性是，能把被装饰的函数替换成其他函数，第二个特性是装饰器加载模块时会立即执行。  
第二个特性看可以看看下面这个例子:    

```python     
registry = []
def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')
@register
def f2():
    print('running f2()')
def f3():
    print('running f3()')
def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()
if __name__=='__main__':
    main()
```      

控制台输出如下:

```python    
running register(<function f1 at 0x10320eb70>)
running register(<function f2 at 0x10320eae8>)
running main()
registry -> [<function f1 at 0x10320eb70>, <function f2 at 0x10320eae8>]
running f1()
running f2()
running f3()
```     

如果是导入:    
```python    
>>> import registeration
running register(<function f1 at 0x1100480d0>)
running register(<function f2 at 0x110048158>)
>>> registeration.registry
[<function f1 at 0x1100480d0>, <function f2 at 0x110048158>]   
```      

上面的例子可以看出：函数装饰器在导入模块时立即执行，而被装饰的函数只在明确调用时运行。这突出了 Python 的**导入时**和**运行时**之间的区别。    

这里提到装饰器的通常用法和registeration.py中的不同:   
- 例子中的装饰器函数与被装饰的函数在同一个模块中定义。实际情况是，装饰器通常在一个模块中定义，然后应用到其他模块中的函数上。
- 例子中的 register 

#### 7.3 使用装饰器改进策略模式
在使用一等对象的特性实现策略模式时，曾经说过，当时的实现有一些问题，就是如何方便的遍历所有的策略以获取最佳的折扣，现在我们可以使用装饰器很好的解决这个问题。

```python    
promos = []
def promotion(promo_func):
    promos.append(promo_func)
    return promo_func
@promotion
def fidelity(order):
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0
@promotion
    def bulk_item(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
        return discount
@promotion
def large_order(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0
def best_promo(order):
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)
```     

这样做的好处有:

- 策略函数无须使用特殊的名称作区分
- @promotion 装饰器既可以增加策略，也可以方便禁用策略（注释掉装饰器即可）
- 策略函数可以在任何地方定义，只需要使用@promotion装饰器

多数装饰器会修改被装饰的函数。通常，它们会定义一个内部函数，然后将其返回，替换被装饰的函数。使用内部函数的代码几乎都要靠闭包才能正确运作。为了理解闭包，我们要先了解 Python 中的变量作用域。   
#### 7.4 Python中变量的作用域   
下面的一系列控制台交互可以让我们更加了解Python的变量作用域：     

```python    
>>> def f1(a):
...     print(a)
...     print(b)
...
>>> f1(3)
3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in f1
NameError: name 'b' is not defined

```      
这个例子中由于没有定义全局变量b导致报错

```python    
>>> b = 6
>>> f1(3)
3
6

```    
这里定义了全局变量b,正常运行

```python    
>>> def f2(a):
...     print(a)
...     print(b)
...     b = 6
...
>>> b = 3
>>> f2(3)
3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in f2
UnboundLocalError: local variable 'b' referenced before assignment

```    

这里由于函数f2的定义体中给b赋值了，导致f2判断b是局部变量。

这里我们可以看到Python对变量的一个设计: Python 不要求声明变量，但是假定在函数定义体中赋值的变量是局部变量。这样的好处是可以防止在不知情的情况下使用全局变量。
如果也要在函数定义体中对全局变量赋值，只需要用global声明：

```python    
>>> def f3(a):
...     global b
...     print(a)
...     print(b)
...     b = 6
...
>>> b = 3
>>> f3(b)
3
3
>>> b
6
>>>
```     

为了深入理解一下f1/f2这两个函数的变量加载方式，可以使用dis模块反汇编，查看字节码：  

```python     
>>> dis(f1)
  2           0 LOAD_GLOBAL              0 (print)
              2 LOAD_FAST                0 (a)
              4 CALL_FUNCTION            1
              6 POP_TOP

  3           8 LOAD_GLOBAL              0 (print)
             10 LOAD_GLOBAL              1 (b)  #全局变量
             12 CALL_FUNCTION            1
             14 POP_TOP
             16 LOAD_CONST               0 (None)
             18 RETURN_VALUE

SyntaxError: invalid syntax
>>> dis(f2)
  2           0 LOAD_GLOBAL              0 (print)
              2 LOAD_FAST                0 (a)
              4 CALL_FUNCTION            1
              6 POP_TOP

  3           8 LOAD_GLOBAL              0 (print)
             10 LOAD_FAST                1 (b)  #局部变量
             12 CALL_FUNCTION            1
             14 POP_TOP

  4          16 LOAD_CONST               1 (6)
             18 STORE_FAST               1 (b)
             20 LOAD_CONST               0 (None)
             22 RETURN_VALUE
```       


####  7.5  闭包   
闭包指延伸了作用域的函数，其中包含函数定义体中引用、但是不在定义体中定义的非全局变量。函数是不是匿名的没有关系，关键是它能访问定义体之外定义的非全局变量。     
这个概念非常抽象，我们通过一个例子更好地理解它:

> 假如有个名为 avg 的函数，它的作用是计算不断增加的系列值的均值；例如，整个历史中某个商品的平均收盘价。每天都会增加新价格，因此平均值要考虑至目前为止所有的价格。    

首先看看这个函数的面对对象实现:

```python   
class Averager():
    def __init__(self):
        self.series = []
    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)
```   

其中Averager()是一个可调用对象，创建Averager的实例就可以达成上面所说的要求。

> \>\>\> avg = Averager()     
> \>\>\> avg(10)   
> 10.0   
> \>\>\> avg(11)    
> 10.5   
> \>\>\> avg(12)    
> 11.0  

接下来是函数式实现，使用高阶函数make_averager:    

```python    
def make_averager():
    series = []
    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager
```    
> \>\>\> avg = make_averager()    
> \>\>\> avg(10)    
>  10.0    
> \>\>\> avg(11)    
>  10.5    
> \>\>\> avg(12)    
>  11.0    

这两个示例的相同点: 都是通过更新历史值再进行平均值计算。问题在于数据的存储，面对对象实现是存储在实例属性self.series中的，而make_averager是存储在series中的。

这里需要注意的地方是，在 avg = make\_averager() 这句执行以后，make_averager函数已经返回了，这时series的本地作用域已经不存在了。

而在averager中，series是自由变量（free variable）,指未在本地作用域中绑定的变量。
![自由变量](https://github.com/aldslvda/blog-images/blob/master/fluent-python-7.1.png?raw=true)

接下来审查averager对象，我们发现Python在\_\_code\_\_属性中保存局部变量和自由变量的名称。

```python    
>>> from averager import make_averager
>>>
>>> avg = make_averager()
>>> avg.__code__.co_varnames
('new_value', 'total')
>>> avg.__code__.co_freevars
('series',)
```   

series 绑定在 avg.\_\_closure\_\_属性中

```python     
>>> avg.__closure__[0].cell_contents
[]
>>> avg(10)
10.0
>>> avg.__closure__[0].cell_contents
[10]
>>> avg(11)
10.5
>>> avg.__closure__[0].cell_contents
[10, 11]
>>> avg(13)
11.333333333333334
>>> avg.__closure__[0].cell_contents
[10, 11, 13]
```     

这样我们可以很形象的理解闭包的性质了，闭包是一种函数，它会保留定义函数时存在的自由变量的绑定，这样调用函数时，虽然定义作用域不可用了，但是仍能使用那些绑定。    

只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量，这也是匿名函数容易和闭包混淆的一个原因。    

#### 7.6 nonlocal声明

前面实现的make_averager函数的效率并不高，因为每次调用avg都要对所有历史值求和，实际上只需要当前值+历史值的和就可以了。    
接下来我们尝试对代码进行一些优化:      

```python
def make_averager_v1():
    count = 0
    total = 0
    def averager(new_value):
        count += 1
        total += new_value
        return total / count
    return averager    
```      

控制台输出如下:   
```python      
>>> from averager import make_averager_v1
>>> avg = make_averager_v1()
>>> avg(10)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/NickAl/study/github/readings/Fluent-Python/7. Function Decorators and Closures/averager.py", line 13, in averager
    count += 1
UnboundLocalError: local variable 'count' referenced before assignment
>>>
```      

由于函数的定义体对count赋值了，由于count是int,赋值会隐式的创建一个新对象，导致函数判断count是局部变量而不是自由变量，不会保存在闭包中，会导致抛出异常。

Python3 中的nonlocal声明会把变量标记为自由变量，使得变量可以保存在闭包中。
下面利用nonlocal对上面的代码进行修正：

```python    
def make_averager_v1():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager
```   
在没有nonlocal声明的Python2中，我们可以将变量作为值存储在可变对象中来解决这个问题。

#### 7.7 实现一个简单的装饰器     
下面是一个简单的装饰器，输出函数的运行时间, clocked是一个闭包，func是自由变量。   

```python    
import time
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
```    

下面的Python代码展示了如何使用这个装饰器:

```python     
# clockdeco_demo.py
import time
from clockdeco import clock
@clock
def snooze(seconds):
    time.sleep(seconds)
@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)
if __name__=='__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))
```    

输出如下:

> -> % python3 clockdeco_demo.py     
> **************************************** Calling snooze(.123)     
> [0.12309374s] snooze(0.123) -> None     
> **************************************** Calling factorial(6)     
> [0.00000162s] factorial(1) -> 1    
> [0.00003553s] factorial(2) -> 2    
> [0.00005951s] factorial(3) -> 6    
> [0.00008194s] factorial(4) -> 24    
> [0.00010441s] factorial(5) -> 120    
> [0.00013048s] factorial(6) -> 720    
> 6! = 720    

这个例子中，clocked参数做了如下操作:     
(1) 记录初始时间 t0。    
(2) 调用原来的 factorial 函数，保存结果。    
(3) 计算经过的时间。    
(4) 格式化收集的数据，然后打印出来。    
(5) 返回第 2 步保存的结果。    
这是装饰器的典型行为：把被装饰的函数替换成新函数，二者接受相同的参数，而且（通常）返回被装饰的函数本该返回的值，同时还会做些额外操作。

上面的装饰器还存在一些问题:

- 不支持关键字参数
- 遮盖了被装饰的函数的\_\_name\_\_和\_\_doc\_\_属性

下面的示例解决了这个问题：

```python    
#clockdeco2.py
import time
import functools
def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
            arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked
```
functool.wrap是标准库中可以直接取用的装饰器。

#### 7.8 标准库中的装饰器

这节会讲到functool中的两个值得关注的装饰器: lru\_cache和single\_dispatch

##### 7.8.1　使用functools.lru_cache做备忘
functools.lru_cache 是非常实用的装饰器，它实现了备忘（memoization）功能。这是一项优化技术，它把耗时的函数的结果保存起来，避免传入相同的参数时重复计算。LRU三个字母是“Least Recently Used”的缩写，表明缓存不会无限制增长，一段时间不用的缓存条目会被扔掉。    
生成第 n 个斐波纳契数这种慢速递归函数适合使用 lru_cache，下面的代码是一个示例

```python     
from clockdeco import clock
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)
if __name__=='__main__':
    print(fibonacci(6))

```

输出如下：

> -> % python3 fibo_demo.py  
> [0.00000075s] fibonacci(0) -> 0   
> [0.00000106s] fibonacci(1) -> 1  
> [0.00008829s] fibonacci(2) -> 1  
> [0.00000052s] fibonacci(1) -> 1  
> [0.00000056s] fibonacci(0) -> 0  
> [0.00000068s] fibonacci(1) -> 1  
> [0.00002681s] fibonacci(2) -> 1  
> [0.00005140s] fibonacci(3) -> 2  
> [0.00016751s] fibonacci(4) -> 3  
> [0.00000051s] fibonacci(1) -> 1  
> [0.00000046s] fibonacci(0) -> 0  
> [0.00000054s] fibonacci(1) -> 1  
> [0.00002430s] fibonacci(2) -> 1  
> [0.00005003s] fibonacci(3) -> 2  
> [0.00000054s] fibonacci(0) -> 0  
> [0.00000057s] fibonacci(1) -> 1  
> [0.00002484s] fibonacci(2) -> 1   
> [0.00000044s] fibonacci(1) -> 1  
> [0.00000081s] fibonacci(0) -> 0   
> [0.00000073s] fibonacci(1) -> 1   
> [0.00002765s] fibonacci(2) -> 1   
> [0.00005353s] fibonacci(3) -> 2   
> [0.00010212s] fibonacci(4) -> 3  
> [0.00017658s] fibonacci(5) -> 5  
> [0.00037021s] fibonacci(6) -> 8  
>  8

可以看到低阶的部分不断的被运算，非常浪费时间，下面是利用缓存优化后的代码:

```python    
import functools
from clockdeco import clock
@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)
if __name__=='__main__':
    print(fibonacci(6))
```

控制台输出:

> -> % python3 fibo_demo.py  
> [0.00000114s] fibonacci(0) -> 0  
> [0.00000152s] fibonacci(1) -> 1  
> [0.00014005s] fibonacci(2) -> 1  
> [0.00000173s] fibonacci(3) -> 2  
> [0.00018128s] fibonacci(4) -> 3  
> [0.00000119s] fibonacci(5) -> 5   
> [0.00022029s] fibonacci(6) -> 8   
>  8  

这里要注意的两点是:lru\_cache必须向常规函数一样被调用，而是装饰器是可以叠加的。   
上面的例子告诉我们lru\_cache在优化递归缓存方面的巨大用途，其实它在Web应用中也能起到很大的用处

> functools.lru_cache(maxsize=128, typed=False)

上面可以看出functools.lru\_cache接收两个参数，maxsize和typed。
- maxsize指定存储结果的数量，缓存满了之后，旧的结果会被丢掉，一般为了性能考虑，这个值设为2的幂。
- typed是否区分不同类型的结果（如浮点数和整数）
- 同时lru\_cache要求被传入的函数的参数是可散列的。

7.8.2 单分派泛函数

Python中经常会困扰我们的问题是:没有switch语句，如何处理多条件的问题。用多个if/elif/else组合可以解决这个问题，但有时候这样做的代码过于冗杂难以阅读。      

single\_dispatch装饰器就是被用来处理这种问题的。使用 @singledispatch 装饰的普通函数会变成泛函数（generic function）：根据第一个参数的类型，以不同方式执行相同操作的一组函数。

下面的例子展示了一个根据参数类型不同生成不同的Html的场景

```python
from functools import singledispatch
from collections import abc
import numbers
import html
@singledispatch
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)
@htmlize.register(str)
def _(text):
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)
@htmlize.register(numbers.Integral)
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)
@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

```     

注册的专门函数应该尽可能处理抽象基类（如 numbers.Integral 和abc.MutableSequence），不要处理具体实现（如 int 和 list）。这样，代码支持的兼容类型更广泛。例如，Python 扩展可以子类化 numbers.Integral，使用固定的位数实现 int 类型。   

single dispatch 类似重载，但绝不是为了把 Java 的那种方法重载带入 Python。   

#### 7.9 参数化装饰器
Python 把被装饰的函数作为第一个参数传给装饰器函数。那怎么让装饰器接受其他参数呢？答案是：创建一个装饰器工厂函数，把参数传给它，返回一个装饰器，然后再把它应用到要装饰的函数上。

下面依次讲解上文中出现过的装饰器的参数化:

##### 7.9.1 参数化的registeration
为了便于启用或禁用 register 执行的函数注册功能，我们为它提供一个可选的 active参数，设为 False 时，不注册被装饰的函数。
```python     
registry = set()
def register(active=True):
    def decorate(func):
        print('running register(active=%s)->decorate(%s)'% (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate
@register(active=False)
def f1():
    print('running f1()')
@register()
def f2():
    print('running f2()')
def f3():
    print('running f3()')
```      

这里的关键是，register() 要返回 decorate，然后把它应用到被装饰的函数上。    
这只是一个最简单的例子，参数化装饰器通常会把被装饰的函数替换掉，而且结构上需要多一层嵌套。接下来会探讨这种函数金字塔。  

##### 7.9.2 参数化clock装饰器

我们需要对clock装饰器添加一个功能：让用户传入一个格式字符串，控制被装饰函数的输出。

```python   
import time
DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'
def clock(fmt=DEFAULT_FMT): #参数化的装饰器工厂函数
    def decorate(func):     #真正的装饰器
        def clocked(*_args):#包装函数的函数
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate 
if __name__ == '__main__':
    @clock()
    def snooze(seconds):
        time.sleep(seconds)
        for i in range(3):
            snooze(.123)
```   

#### 7.10 小结
这章开始已经进入元编程领域了。
参数化装饰器基本上都涉及至少两层嵌套函数，如果想使用 @functools.wraps 生成装饰器，为高级技术提供更好的支持，嵌套层级可能还会更深，比如前面简要介绍过的叠放装饰器。     
若想真正理解装饰器，需要区分导入时和运行时，还要知道变量作用域、闭包和新增的nonlocal 声明。掌握闭包和 nonlocal 不仅对构建装饰器有帮助，还能协助你在构建GUI 程序时面向事件编程，或者使用回调处理异步 I/O。