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
Python提供了极为灵活的参数处理机制，Python3提供了 keyword-only argument。调用函数时使用*和*展开可迭代对象，映射到单个参数。  

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

#### 7. 获取关于参数的信息    
这里举一个处理web请求的例子: 

```python

import bobo
@bobo.query('/')
def hello(person):
    return 'Hello %s!' % person

```
在上面这段代码中，bobo是一个web微框架，bobo.query()装饰器将hello()函数与请求处理机制结合在一起，使得hello()自动接收请求中的person作为参数，若没有person参数，则返回403.

函数对象有个 \_\_defaults\_\_ 属性，它的值是一个元组，里面保存着定位参数和关键字参数的默认值。仅限关键字参数的默认值在 \_\_kwdefaults\_\_ 属性中。然而，参数的名称在 \_\_code\_\_ 属性中，它的值是一个 code 对象引用，自身也有很多属性。

下面举一个[clip.py](https://github.com/aldslvda/readings/blob/master/Fluent-Python/5.%20First%20Class%20Functions/clip.py)的例子，讲解函数对象用于获取参数信息的属性。

```python

def clip(text, max_len=80):
    """在max_len前面或后面的第一个空格处截断文本
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
        if space_after >= 0:
            end = space_after
            if end is None: # 没找到空格
                end = len(text)
    return text[:end].rstrip()

```

我们在控制台输入下面的命令，查看属性

```python

>>> from clip import clip
>>> clip.__defaults__
(80,)
>>> clip.__code__
<code object clip at 0x10dadcc90, file "/Users/NickAl/study/github/readings/Fluent-Python/5. First Class Functions/clip.py", line 2>
>>> clip.__code__.co_varnames
('text', 'max_len', 'end', 'space_before', 'space_after')
>>> clip.__code__.co_argcount
2

```

参数名称在 \_\_code\_\_.co\_varnames中，不过里面还有函数定义体中创建的局部变量。因此，参数名称是前 N 个字符串，N的值由 \_\_code\\_.co\_argcount 确定。顺便说一下，这里不包含前缀为 * 或 ** 的长度可变的参数。参数的默认值只能通过它们在 \_\_defaults\_\_ 元组中的位置确定，因此要从后向前扫描才能把参数和默认值对应起来。

另一种查看属性的方式是，使用inspect 模块

```python
>>> from clip import clip
>>> from inspect import signature
>>> sig = signature(clip)
>>> sig
<Signature (text, max_len=80)>
>>> for name, param in sig.parameters.items():
...     print(param.kind, ':', name, '=', param.default)
...
POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'>
POSITIONAL_OR_KEYWORD : max_len = 80

```

inspect.signature 函数返回一个 inspect.Signature 对象，它有一个 parameters 属性，这是一个有序映射，把参数名和 inspect.Parameter 对象对应起来。

inspect.Signature的kind属性有下面5种:

- POSITIONAL\_OR\_KEYWORD:可以通过定位参数和关键字参数传入的形参（多数 Python 函数的参数属于此类）。
- VAR\_POSITIONAL:定位参数元组。
- VAR\_KEYWORD:关键字参数字典。
- KEYWORD\_ONLY:仅限关键字参数（Python 3 新增）。
- POSITIONAL\_ONLY:仅限定位参数；目前，Python 声明函数的句法不支持，但是有些使用 C 语言实现且不接受关键字参数的函数（如 divmod）支持。

#### 8. 函数注解

Python 3 提供了一种句法，用于为函数声明中的参数和返回值附加元数据, 这就是注解。
在clip.py中声明一个新的函数clip\_with\_anno, 只在声明时加入注解，其他一样。

```python

def clip_with_anno(text:str, max_len: 'int > 0' = 80) -> str:

```

```python

>>> from clip import clip_with_anno
>>> clip_with_anno.__annotations__
{'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}

```

注解和参数、返回值的对应关系一目了然。然而Python本身对注解没有任何操作。

#### 9. Python标准库中为支持函数式编程提供的包

##### 9.1 operator模块
下面展示了使用reduce计算阶乘的两种方式，区别是是否使用了operator库。

```python

from functools import reduce
from operator import mul

def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))
def fact_with_mul(n):
    return reduce(mul, range(1, n+1))

```

上面的例子使用mul避免了lambda表达式的使用。
operator还提供了一些有效的函数:

- attrgetter 与 itemgetter这样获取对象属性和可迭代对象的元素的函数。
- methodcaller 创建的函数会在对象上调用参数指定的方法

##### 9.2 functools.partial
functools.partial 这个高阶函数用于**部分应用**一个函数。部分应用是指，基于一个函数创建一个新的可调用对象，把原函数的某些参数固定。使用这个函数可以把接受一个或多个参数的函数改编成需要回调的 API，这样参数更少.

```python

>>> from operator import mul
>>> from functools import partial
>>> triple = partial(mul, 3)
>>> triple(7)
21
>>> list(map(triple, range(1, 10)))
[3, 6, 9, 12, 15, 18, 21, 24, 27]

```

#### 10. 小结
这一小节主要讲了Python函数的一等性质，即函数也是对象这一概念，并说明了这一性质的一部分应用场景，以及功能有限的lambda函数的一些替代方式。

高强度加班了两周，终终终终于有时间吧这章看完啦![1](https://github.com/aldslvda/blog-images/blob/master/acfun_emoji/01.png?raw=true)

To be continued ... 敬请期待![1](https://github.com/aldslvda/blog-images/blob/master/acfun_emoji/25.png?raw=true)

 