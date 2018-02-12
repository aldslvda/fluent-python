## Fluent Python ##
### Chapter 8. Object References, Mutability,and Recycling
### 第八章:对象引用、可变性和垃圾回收   

本章的主题是对象与对象名称之间的区别。名称不是对象，而是单独的东西。先以一个比喻说明 Python 的变量：变量是标注，而不是盒子。    
本章的内容有点儿枯燥，但是这些话题却是解决 Python 程序中很多不易察觉的 bug 的关键。   

#### 8.1 变量不是盒子

Python中的变量类似Java中的引用式变量，最好将它们理解为附加在对象上的标注。   
下面的控制台交互和图示很好的解释了"变量不是盒子"这一观点:

```python    
>>> a = [1,2,3]
>>> b=a
>>> a.append(4)
>>> b
[1, 2, 3, 4]
```    
![变量不是盒子](https://github.com/aldslvda/blog-images/blob/master/fluent-python-8.1.png?raw=true)    

对引用式变量来说，说把变量分配给对象更合理，反过来说就有问题。毕竟，对象在赋值之前就创建了。为了理解 Python 中的赋值语句，应该始终先读右边。对象在右边创建或获取，在此之后左边的变量才会绑定到对象上，这就像为对象贴上标注。

#### 8.2 标识，相等性和别名
首先看下面的例子和图示:

```python    
>>> charles = {'name': 'Charles L. Dodgson', 'born': 1832}
>>> lewis = charles
>>> lewis is charles
True
>>> id(charles), id(lewis)
(4300473992, 4300473992)
>>> lewis['balance'] = 950
>>> charles
{'name': 'Charles L. Dodgson', 'balance': 950, 'born': 1832}
>>> alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950} ➊
>>> alex == charles
True
>>> alex is not charles
True
>>> id(alex)
4382361712
```

lewis 和 charles 是别名，即两个变量绑定同一个对象。而 alex 不是 charles 的别名，因为二者绑定的是不同的对象。alex 和charles 绑定的对象具有相同的值（== 比较的就是值），但是它们的标识不同。

>  每个变量都有标识、类型和值。对象一旦创建，它的标识绝不会变；你可以把标识理解为对象在内存中的地址。is 运算符比较两个对象的标识；id() 函数返回对象标识的整数表示。

##### 8.2.1 is和==
== 运算符比较两个对象的值（对象中保存的数据），而 is 比较对象的标识。  
通常，我们关注的是值，而不是标识，因此 Python 代码中 == 出现的频率比 is 高。  

##### 8.2.2 元组的相对不可变性  
元组与多数 Python 集合（列表、字典、集，等等）一样，保存的是对象的引用。 如果引用的元素是可变的，即便元组本身不可变，元素依然可变。也就是说，元组的不可变性其实是指 tuple 数据结构的物理内容（即保存的引用）不可变，与引用的对象无关。

下面的例子能显而易见地看出元组的相对不可变性:

```python    
>>> t1 = (1, 2, [30, 40])
>>> t2 = (1, 2, [30, 40])
>>> t1 == t2
True
>>> id(t1[-1])
4302515784
>>> t1[-1].append(99)
>>> t1
(1, 2, [30, 40, 99])
>>> id(t1[-1])
4302515784
>>> t1 == t2
False
```     

#### 8.3 默认做浅复制

复制列表（或多数内置的可变集合）最简单的方式是使用内置的类型构造方法: 

```python    
>>> l1 = [3, [55, 44], (7, 8, 9)]
>>> l2 = list(l1)
>>> l2
[3, [55, 44], (7, 8, 9)]
>>> l2 == l1
True
>>> l2 is l1
False
```   
这样构造出的l2和l1并不是同一个对象，l2 = l1[:] 也可以得到同样的效果。 

然而，构造方法或 [:] 做的是浅复制（即复制了最外层容器，副本中的元素是源容器中元素的引用）。如果所有元素都是不可变的，那么这样没有问题，还能节省内存。但是，如果有可变的元素，可能会出现错误(l1, l2 会随着可变对象的修改同时发生变化)。  

这时需要做深复制(deepcopy),下面的例子里我们会将深复制和浅复制对比:    
首先定义一个类

```python     
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)
    def pick(self, name):
        self.passengers.append(name)
    def drop(self, name):
        self.passengers.remove(name)
```

接下来在控制台对类的实例进行操作:
```python     
>>> from bus import Bus
>>> import copy
>>> bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
>>> bus2 = copy.copy(bus1)
>>> bus3 = copy.deepcopy(bus1)
>>> id(bus1), id(bus2), id(bus3)
(4571562840, 4571563288, 4571563512)
>>> bus1.drop('Bill')
>>> bus2.passengers
['Alice', 'Claire', 'David']
>>> id(bus1.passengers), id(bus2.passengers), id(bus3.passengers)
(4571550024, 4571550024, 4566929352)
>>> bus3.passengers
['Alice', 'Bill', 'Claire', 'David']
```     

bus2 是bus1的浅复制副本， bus3是深复制副本。

deepcopy 函数会记住已经复制的对象，因此能优雅地处理循环引用，下面的控制台交互是一个例子。

```python     
>>> a = [10, 20]
>>> b = [a, 30]
>>> a.append(b)
>>> a
[10, 20, [[...], 30]]
>>> from copy import deepcopy
>>> c = deepcopy(a)
>>> c
[10, 20, [[...], 30]]   
```  



#### 8.4 函数的参数作为引用

Python 唯一支持的参数传递模式是共享传参（call by sharing), 共享传参指函数的各个形式参数获得实参中各个引用的副本。也就是说，函数内部的形参是实参的别名。      
这种方案的结果是，函数可能会修改作为参数传入的可变对象，但是无法修改那些对象的标识（即不能把一个对象替换成另一个对象）。    

下面的例子展示了函数会修改接收到的**可变对象**:

```python    
>>> def f(a, b):
... a += b
... return a
...
>>> x = 1
>>> y = 2
>>> f(x, y)
3 >>> x, y
(1, 2)
>>> a = [1, 2]
>>> b = [3, 4]
>>> f(a, b)
[1, 2, 3, 4]
>>> a, b
([1, 2, 3, 4], [3, 4])
>>> t = (10, 20)
>>> u = (30, 40)
>>> f(t, u)
(10, 20, 30, 40)
>>> t, u
((10, 20), (30, 40))
```

##### 8.4.1 可变类型不要作为传入参数默认值
默认值在定义函数时计算（通常在加载模块时），因此默认值变成了函数对象的属性。如果默认值是可变对象，而且修改了它的值，那么后续的函数调用都会受到影响。

##### 8.4.2 防止可变参数造成的影响    
下面的例子说明了可变参数可能造成的影响 

```python   
class TwilightBus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers
    def pick(self, name):
        self.passengers.append(name)
    def drop(self, name):
        self.passengers.remove(name)

```

