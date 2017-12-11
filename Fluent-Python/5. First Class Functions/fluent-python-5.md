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

lamda函数就是在python表达式内创建匿名函数，但由于句法的限制，lambda函数的定义体只能用纯表达式。

"Functional Programming HOWTO" 中提到，如果使用lambda表达式使得代码难以理解，建议按下面的步骤重构:

- 编写注释，说明lambda表达式的作用       
- 研究注释，用一个名称概括       
- 用这个名称定义一个函数，把lambda表达式转换成这个函数    
- 删除注释

#### 4.可调用对象
Python 的数据模型文档指出了7种可调用对象：
- 用户定义的函数:   
    使用lambda表达式或者def语句创建  
- 内置函数: 
    使用CPython实现的函数   
- 内置方法:
    使用C语言实现的方法   
- 方法:
    类的定义题中实现的函数   
- 类:
    调用时会创建一个实例，然后执行构造函数
- 类的实例:
    如果类定义了\_\_call\_\_方法，那么它的实例可以作为函数调用。  
- 生成器函数:
    使用了yeild关键字的函数或方法, 返回生成器对象。

#### 5.用户定义的可调用类型
不仅python函数式对象，对象也可以表现得像函数，只需要实现方法\_\_call\_\_。

```python

import random
class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)
    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    def __call__(self):
        return self.pick()

```
这样调用BingoCage的实例时，效果和调用pick方法一样。  

实现 \_\_call\_\_ 方法的类是创建函数类对象的简便方式，此时必须在内部维护一个状态，让它在调用之间可用，例如 BingoCage 中的剩余元素。装饰器就是这样。装饰器必须是函数，而且有时要在多次调用之间“记住”某些事 [ 例如备忘（memoization），即缓存消耗大的计算结果，供后面使用 ]。

创建保有内部状态的函数，还有一种截然不同的方式 —— 使用闭包。

#### 6. 从定位参数到仅限关键字参数    
Python提供了极为灵活的参数处理机制，Python3提供了 keyword-only argument。调用函数时使用*和**展开可迭代对象，映射到单个参数。  

下面的例子中，tag函数用于生成html标签

```python

def tag(name, *content, cls=None, **attrs):
    """生成一个或多个HTML标签"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value)
                        for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' %
                (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)

```

下面是这个函数的几种调用方式

```python

>>> tag('br')
'<br />'
>>> tag('p', 'hello')
'<p>hello</p>'
>>> print(tag('p', 'hello', 'world'))
<p>hello</p>
<p>world</p>
>>> tag('p', 'hello', id=33)
'<p id="33">hello</p>'
>>> print(tag('p', 'hello', 'world', cls='sidebar'))
<p class="sidebar">hello</p>
<p class="sidebar">world</p>
>>> tag(content='testing', name="img")
'<img content="testing" />'
>>> my_tag = {'name': 'img', 'title': 'Sunset Boulevard',
... 'src': 'sunset.jpg', 'cls': 'framed'}
>>> tag(**my_tag)
'<img class="framed" src="sunset.jpg" title="Sunset Boulevard" />'

```

#### 7. 获取关于参数的信息。
