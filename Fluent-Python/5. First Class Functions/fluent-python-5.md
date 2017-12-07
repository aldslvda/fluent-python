## Fluent Python ##
### Chapter 5. First Class Functions ###
### 第五章. 一等函数
首先解释一下标题的含义:   
编程语言理论家把“一等对象”定义为满足下述条件的程序实体：

- 在运行时创建
- 能赋值给变量或数据结构中的元素
- 能作为参数传给函数
- 能作为函数的返回结果

在Python中，整数、字符串和字典都是一等对象，特别提到的是，函数也是一等对象，这一特性称为一等函数。

#### 1. 把函数视作对象

```python

>>> print.__doc__
"print(value, ..., sep=' ', end='\\n', file=sys.stdout, flush=False)\n\nPrints the values to a stream, or to sys.stdout by default.\nOptional keyword arguments:\nfile:  a file-like object (stream); defaults to the current sys.stdout.\nsep:   string inserted between values, default a space.\nend:   string appended after the last value, default a newline.\nflush: whether to forcibly flush the stream."
>>> type(print)
<class 'builtin_function_or_method'>

```

由上面的控制台输出可以看到函数print有一个名为\_\_doc\_\_的属性, 同时是builtin\_function\_or\_method的一个实例。

```python

>> def plus(a):
...     return a+1
...
>>> map(plus, range(10))
<map object at 0x109553c50>
>>> list(map(plus, range(10)))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

``` 

由上面的控制台输出可以看到函数是可以作为参数被传递的。   
有了一等函数，就可以使用函数式编程。

#### 2. 高阶函数    
接受函数为参数，或者把函数作为结果返回的函数是高阶函数（higher-orderfunction），第一节中提到的map就是一个高阶函数。

##### 2.1 常见的高阶函数
函数式语言通常会提供map、filter和reduce这三个高阶函数。

- 在Python中，map/filter有更好用的替代品，Python2中map/filter返回的是列表，所以比较好的替代品是列表推导，Python3中这两个函数的返回则是生成器，所以比较好的替代是生成器表达式   

reduce比较特别：

```python

>>> from functools import reduce 
>>> from operator import add 
>>> reduce(add, range(100)) 
4950
>>> sum(100)
4950

```

sum 和 reduce 的通用思想是把某个操作连续应用到序列的元素上，累计之前的结果，把一系列值归约成一个值。     
类似的归约函数还有all()和any(), all()传入一个可迭代对象，若所有元素都为True,返回True,否则返回False; 而any()只要有一个True就返回True。

#### 3.匿名函数  
为了使用高阶函数，有时创建一次性的小型函数更便利， 这便是匿名函数的由来。

