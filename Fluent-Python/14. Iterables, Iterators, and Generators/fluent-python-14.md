## Fluent Python 
### Chapter 14. Iterables, Iterators, and GeneratorsOperator
### 第十四章: 可迭代对象，迭代器和生成器

迭代是数据处理的基石。扫面内存中放不下的数据集时， 我们需要找到一种惰性获取数据的方式，即按需每次获取一个数据项。这就是迭代器模式(Iterator Pattern).
下面会说明Python语言是如何内置迭代器模式的。

> 所有生成器都是迭代器，因为生成器完全实现了迭代器接口。不过，根据《设计模式：可复用面向对象软件的基础》一书的定义，迭代器用于从集合中取出元素；而生成器用于“凭空”生成元素。通过斐波纳契数列能很好地说明二者之间的区别：斐波纳契数列中的数有无穷个，在一个集合里放不下。不过要知道，在 Python 社区中，**大多数时候都把迭代器和生成器视作同一概念**。

Python3 中， 生成器有广泛的用途， 例如range() 在Python2中返回列表， 在3中返回一个类似生成器的对象。

在Python语言内部， 迭代器用于支持:  
- for循环
- 构建和扩展集合类型
- 逐行遍历文本文件
- 列表推导， 字典推导和集合推导
- 元组拆包
- 调用函数时使用\*拆包实参

本章将讨论：
- 语言内部使用iter()内置函数处理可迭代对象的方式
- 如何使用Python实现经典的迭代器模式
- 说明生成器函数的工作原理
- 如何使用生成器函数或生成器表达式代替经典的迭代器
- 如何使用标准库中通用的生成器函数
- 如何使用yeild from 语句合并生成器
- 为什么生成器和协程看似相同实则差别很大， 不能混淆

#### 14.1 从序列开始

我们首先实现一个Sentence类， 通过索引从文本提取单词。

```python
import re
import reprlib
    RE_WORD = re.compile('\w+')
    class Sentence:
        def __init__(self, text):
            self.text = text
            self.words = RE_WORD.findall(text)
        def __getitem__(self, index):
            return self.words[index]
        def __len__(self):
            return len(self.words)
        def __repr__(self):
            return 'Sentence(%s)' % reprlib.repr(self.text)
```

序列可以迭代的原因：iter函数。解释器需要迭代对象 x 时，会自动调用 iter(x)。
内置的 iter 函数有以下作用。
(1) 检查对象是否实现了 \_\_iter\_\_ 方法，如果实现了就调用它，获取一个迭代器。
(2) 如果没有实现 \_\_iter\_\_ 方法，但是实现了 \_\_getitem\_\_ 方法，Python 会创建一个迭代器，尝试按顺序（从索引 0 开始）获取元素。
(3) 如果尝试失败，Python 抛出 TypeError 异常，通常会提示“C object is not iterable”（C对象不可迭代），其中 C 是目标对象所属的类。
任何 Python 序列都可迭代的原因是，它们都实现了 \_\_getitem\_\_ 方法。其实，标准的序列也都实现了 \_\_iter\_\_ 方法

#### 14.2 可迭代对象和迭代器

上面一小节我们可以看到迭代器的定义：
> 使用 iter 内置函数可以获取迭代器的对象。如果对象实现了能返回迭代器的\_\_iter\_\_ 方法，那么对象就是可迭代的。  
> 序列都可以迭代；实现\_\_getitem\_\_ 方法，而且其参数是从零开始的索引，这种对象也可以迭代。  
> 我们要明确可迭代的对象和迭代器之间的关系：Python 从可迭代的对象中获取迭代器。

下面给出一个简单的例子，使用while循环模拟for循环中的迭代器：

```python
# for 实现
s = 'ABC'
for char in s:
    print(char)

# while 实现
s = 'ABC'
it = iter(s) 
while True:
    try:
        print(next(it)) 
    except StopIteration: 
        del it 
    break 
```

标准的迭代器接口有两个方法。
- \_\_next\_\_   
    返回下一个可用的元素，如果没有元素了，抛出 StopIteration 异常。
- \_\_iter\_\_   
    返回 self，以便在应该使用可迭代对象的地方使用迭代器，例如在 for 循环中。
    
这个接口在 collections.abc.Iterator 抽象基类中制定。这个类定义了 \_\_next\_\_ 抽象方法，而且继承自 Iterable 类；\_\_iter\_\_ 抽象方法则在 Iterable 类中定义。

因为迭代器只有\_\_next\_\_ 和\_\_iter\_\_方法，所以迭代器没办法检查遗漏的元素和‘还原’迭代器， 如果想再次迭代， 还是需要传入被迭代的对象。由于Iterator.\_\_init\_\_是返回实例本身，传入迭代器无法还原已经迭代过的元素。

#### 14.3 典型的迭代器

这一节会将迭代器和可迭代对象分离开来，让我们更加清楚迭代器和可迭代对象的关系

```python
import re
import reprlib
RE_WORD = re.compile('\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)
    def __iter__(self):
        return SentenceIterator(self.words)


class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0
    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word
    def __iter__(self):
        return self
```

如果在Sentence中实现\_\_next\_\_方法， 可以让Sentence同时成为可迭代对象和迭代器。但是这是一个相当糟糕的设计。**可迭代的对象一定不能是自身的迭代器**

> 迭代器模式中指明， 迭代器应该有以下特点：
> 1. 访问一个聚合对象的内容而无需暴露它的内部表示
> 2. 支持对聚合对象的多种遍历(每次调用iter()都新建一个独立的迭代器)
> 3. 为遍历不同的聚合结构提供统一的接口

#### 14.4 生成器函数

Python中实现上一节相同功能的方式是使用生成器函数代替额外实现的迭代器。

```python
import re
import reprlib
RE_WORD = re.compile('\w+')
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)
    def __iter__(self):
        for word in self.words:
            yield word
        return
```
相比起上一节的实现简单许多。

> 只要 Python 函数的定义体中有 yield 关键字，该函数就是生成器函数。调用生成器函数时，会返回一个生成器对象。也就是说，生成器函数是生成器工厂。

#### 14.5 生成器的惰性实现

re.finditer是re.findall的惰性版本， 返回的不是一个列表而是一个生成器，这样也能节省大量内存。

```python
import re
import reprlib
RE_WORD = re.compile('\w+')
class Sentence:
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)
    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()
```

使用finditer使得Sentence的元素变得可以惰性获得了。

#### 14.6 生成器表达式

下面使用生成器表达式构建生成器, 会使代码更加简洁
```python
import re
import reprlib
RE_WORD = re.compile('\w+')
class Sentence:
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)
    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))
```

#### 14.7 yeild from 

> 注: yeild from 是Python3.3中新出现的语法

如果生成器函数需要产出另一个生成器生成的值，传统的解决方法是使用嵌套的 for 循
环。  
例如：

```python
>>> def chain(*iterables):
...     for it in iterables:
...         for i in it:
...             yield i
...
>>> s = 'ABC'
>>> t = tuple(range(3))
>>> list(chain(s, t))
['A', 'B', 'C', 0, 1, 2]
```

这个chain生成器函数吧操作依次交给各个可迭代对象处理。我们可以用下面的方法简化：

```python
>>> def chain(*iterables):
...     for i in iterables:
...     yield from i
...
>>> list(chain(s, t))
['A', 'B', 'C', 0, 1, 2]
```

可以看出，yield from i 完全代替了内层的 for 循环， 使得代码简化很多。

#### 14.8 深入分析iter()函数
在 Python 中迭代对象 x 时会调用 iter(x), 这是上文中我们反复提到的, 这也是iter()最常见的用法。   

iter 函数还有一个鲜为人知的用法：传入两个参数，使用常规的函数或任何可调用的对象创建迭代器。这样使用时，第一个参数必须是可调用的对象，用于不断调用（没有参数），产出各个值；第二个值是哨符，这是个标记值，当可调用的对象返回这个值时，触发迭代器抛出 StopIteration 异常，而不产出哨符。

例子：
```python
# 掷骰子直到掷出1点
from random import randint
def d6():
    return randint(1, 6)

d6_iter = iter(d6, 1)
for roll in d6_iter:
    print(roll)
```

#### 14.9 生成器当成协程

> Python 2.5 实现了“PEP 342 — Coroutines via Enhanced Generators”（https://www.python.org/dev/peps/pep-0342/ ）。这个提案为生成器对象添加了额外的方法和功能，其中最值得关注的是 .send() 方法， 这个函数让生成器变身为**协程**。

与 .\_\_next\_\_() 方法一样，.send() 方法致使生成器前进到下一个 yield 语句。不过，.send() 方法还允许使用生成器的客户把数据发给自己，即不管传给 .send() 方法什么参数，那个参数都会成为生成器函数定义体中对应的 yield 表达式的值。也就是说，.send() 方法允许在客户代码和生成器之间双向交换数据。而 .\_\_next\_\_() 方法只允许客户从生成器中获取数据。

> - 生成器用于生成供迭代的数据
> - 协程是数据的消费者
> - 为了避免脑袋炸裂，不能把这两个概念混为一谈
> - 协程与迭代无关
> - 注意，虽然在协程中会使用 yield 产出值，但这与迭代无关
>       
>    <div align = right>——David Beazley  “A Curious Course on Coroutines and Concurrency”</div>

基于这几点， 本章不讨论协程![233](https://github.com/aldslvda/blog-images/blob/master/acfun_emoji/11.png?raw=true)

#### 14.9 小结
Python 语言对迭代的支持非常深入, Python 已经融合（grok）了迭代器。Python 从语义上集成迭代器模式是个很好的例证，说明设计模式在各种编程语言中使用的方式并不相同。