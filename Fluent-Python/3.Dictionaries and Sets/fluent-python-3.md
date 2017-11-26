+++
topics = ["Python"]
description = "流畅的Python笔记  第三章"
draft = false
date = "2017-11-23T21:25:19+08:00"
title = "Fluent Python 第三章小结"
tags = ["Python","基础","dict","set"]
+++

## Fluent Python ##
### Chapter 3. Dictionaries and Sets ###
### 字典和集合 ###
dict 类型不但在各种程序里广泛使用，它也是 Python 语言的基石。模块的命名空间、实例的属性和函数的关键字参数中都可以看到字典的身影。跟它有关的内置函数都在\_\_builtins\_\_.\_\_dict\_\_模块中。     
Python 对字典做了高度优化，python字典性能优秀的原因是散列表。   
集合同样依赖散列表。   

*有部分翻译存在疑问，用括号标注原英文正文。

#### 1. 泛映射类型 ####
![Figure-3-1](https://raw.githubusercontent.com/aldslvda/blog-images/master/fluent-python-3.1.png)
collections.abc 模块中有 Mapping 和 MutableMapping 这两个抽象基类,它们的作用是为 dict 和其他类似的类型定义形式接口。   
非抽象映射类型一般不会直接继承这些抽象基类，它们会直接对 dict 或是collections.User.Dict 进行扩展。这些抽象基类的主要作用是作为**形式化的文档**。

标准库里的所有映射类型都是利用 dict 来实现的，因只有**可散列的数据类型**才能用作这些映射里的键。
##### 1.1 可散列的数据类型 #####    
如果一个对象是可散列的，那么在这个对象的生命周期中，它的散列值是不变的，而且这个对象需要实现 \_\_hash\_\_() 方法。另外可散列对象还要有\_\_eq\_\_() 方法，这样才能跟其他键做比较。

Python文档[https://docs.python.org/3/glossary.html#term-hashable](https://docs.python.org/3/glossary.html#term-hashable)中提到，所有不可变的类型都是可散列的，但元组是一个例外，元组可散列的条件是元组的元素都可以散列。    
一个对象可散列的条件是：如果一个对象实现了\_\_eq\_\_方法，并且在方法中用到了这个对象的内部状态的话，那么只有当所有这些内部状态都是不可变的情况下，这个对象才是可散列的。
##### 1.2 创建字典的不同方式 #####

```python
>>> a = dict(one=1, two=2, three=3)>>> b = {'one': 1, 'two': 2, 'three': 3}>>> c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))>>> d = dict([('two', 2), ('one', 1), ('three', 3)])>>> e = dict({'three': 3, 'one': 1, 'two': 2})>>> a == b == c == d == eTrue
```
除此之外，字典推导也能创建一个字典, 和列表推导类似

```python
>>> DIAL_CODES = [ ...  (86, 'China'),...  (91, 'India'),...  (1, 'United States'),...  (62, 'Indonesia'),...  (55, 'Brazil'),...  (92, 'Pakistan'),...  (880, 'Bangladesh'),...  (234, 'Nigeria'),...  (7, 'Russia'),...  (81, 'Japan'),... ]>>> country_code = {country: code for code, country in DIAL_CODES}

```

#### 2.常用的映射方法 ####

这里讲到一个能让程序更加高效的方法 setdefault()，能节省很多次的键查询。

例如：   
2.1:
   
```python
my_dict.setdefault(key, []).append(new_value)

```
2.2  

```python
if key not in my_dict:	my_dict[key] = []my_dict[key].append(new_value)

```

操作2.1和2.2达到的效果是一样的，但是2.1只用了一次键查询，而2.2会用到2-3次(是否有key存在)

#### 3.映射的弹性键查询(flexible key lookup) ####

场景：为了方便起见，就算某个键在映射里不存在，我们也希望在通过这个键读取值的时候能得到一个默认值。有两个方法能实现：使用defaultdict类或者自己实现一个类继承dict,实现\_\_missing\_\_方法。
##### 3.1 defaultdict #####

有一个新字典dd = defaultdict(list),当使用表达式dd[key]而key在defaultdict中不存在的话，就会用list()建立新列表作为值，key作为键放入dd中，然后返回这个列表的引用。   
这个用来生成默认值的可调用对象放在default_factory这个实例属性中。

##### 3.2 特殊方法 \_\_missing\_\_() #####

当一个继承了dict的类实现了\_\_missing\_\_方法，在查询一个不存在的键的时候就会调用这个方法。值得一提的是，只有\_\_getitem\_\_方法会调用\_\_missing\_\_方法。

####4. 字典的变种####
- collections.OrderedDict:这个类的对象在添加键的时候会保持顺序，键的迭代顺序总是一样的
- collections,ChainMap:可以容纳数个映射对象，进行键查询的时候会逐个查询，直到找到为止。
- collections.Counter: 每次更新一个键的时候就会增加这个键的计数器, 比较有用的方法是most_common(n) 按次序返回最常见的n个键和他们的计数。
- collections.UserDict: 把标准dict用Python实现用于用户继承这个类，编写子类。

####5. 继承UserDict编写子类####
更倾向于从 UserDict 而不是从 dict 继承的主要原因是，后者有时会在某些方法的实现上走一些捷径，导致我们不得不在它的子类中重写这些方法，但是 UserDict 就不会带来这些问题。

```python
import collectionsclass StrKeyDict(collections.UserDict):    def __missing__(self, key):        if isinstance(key, str):            raise KeyError(key)        return self[str(key)]    def __contains__(self, key):        return str(key) in self.data    def __setitem__(self, key, item):        self.data[str(key)] = item
```

UserDict 中有一个属性叫做data,它是dict 的一个实例，用于存储数据。

#### 6.不可变的映射类型 ####

标准库里所有的映射类型都是可变的，但有时候也会有需要用到不可变映射的地方，例如不能让用户修改的映射。

Python 3.3 开始，types 模块中引入了一个封装类名叫 MappingProxyType。如果给这个类一个映射，它会返回一个只读的映射视图。虽然是个只读视图，但是它是动态的。这意味着如果对原映射做出了改动，我们通过这个视图可以观察到，但是无法通过这个视图对原映射做出修改。

\* 何为副本？何为视图？     
副本：就是原有数据的一份拷贝。   
视图：可理解为原有数据的一个别称或引用，通过该别称或引用亦便可访问、操作原有数据，但原有数据不会产生拷贝。


#### 7.集合 ####
集合的本质是许多唯一对象的聚集，所以集合的其中一个用途是去重。

集合还实现了很多基础的中缀运算符。给定两个集合 a 和 b，a | b 返回的是它们的合集，a & b 得到的是交集，而 a - b 得到的是差集。合理地利用这些操作，不仅能够让代码的行数变少，还能减少 Python 程序的运行时间。这样做同时也是为了让代码更易读。

除了速度极快的查找功能（这也得归功于它背后的散列表），内置的 set 和 frozenset提供了丰富的功能和操作。   

##### 7.1 set Literals（翻译比较诡异:集合字面量？？？） #####
建立一个集合的时候可以使用{1，2..}类似的操作，但是创建空集的时候只能使用set()构造方法。

##### 7.2 集合推导(类似列表推导) #####

```python
{chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i),'')}
```

##### 7.3 集合的操作 #####

![Figure-3-2](https://raw.githubusercontent.com/aldslvda/blog-images/master/fluent-python-3.1.png)


#### 8.dict和set的背后 ####
要理解Python里字典和集合的长处和短处，它们背后的散列表是必须注意的。   
 
- Python里的字典和集合的效率有多高？
	由于散列表的存在，效率是非常高的（列表由于没有散列表，表现非常差）

##### 8.1 dict的实现及其导致的结果 #####

- 键必须可散列（hashable）
	一个可散列的对象必须满足以下要求。   	(1) 支持 hash() 函数，并且通过 __hash__() 方法所得到的散列值是不变的。   	(2) 支持通过 __eq__() 方法来检测相等性。   	(3) 若 a == b 为真，则 hash(a) == hash(b) 也为真。所有由用户自定义的对象默认都是可散列的，因为它们的散列值由 id() 来获取，而且它们都是不相等的。

- 内存开销巨大
	由于使用了散列表，而散列表本身稀疏，会导致空间效率低下。空间的优化工作可以等到真正需要的时候开启，**优化往往是可维护性的对立面**。

- 键查询快
	由于在空间上的巨大花销，使得时间上的效率很高。

- 键的次序取决于添加顺序
	与建立hash表的时候发生的散列冲突有关。
	
- 往字典里添加新键可能会改变已有键的顺序
	这个和散列冲突有关，所以**慎重进行**迭代一个字典的所有键的过程中同时对字典进行修改这种操作，很有可能会跳过一些已有的键。

#####8.2 set的实现和导致的结果 #####
由于也是基于散列表实现的，set的特点和上一小节提到的dict如出一辙:   

- 集合里的元素必须可散列
- 内存开销大
- 能很快查询元素是否存在于集合
- 元素的顺序取决于添加的顺序
- 添加新元素可能改变已有顺序

