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

