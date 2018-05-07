## Fluent Python ##
### Chapter 10. Sequence Hacking, Hashing, and Slicing
### 第十章: 序列的修改、散列和切片

 这章以上章的Vector2d为基础，定义多维向量，这个类的行为和Python标准的扁平序列一样。将实现下面的功能：

 - 基本的序列协议—— \_\_len\_\_ 和 \_\_getitem\_\_
 - 正确表述拥有很多元素的实例
 - 适当的切片支持，用于生成新的 Vector 实例
 - 综合各个元素的值计算散列值
 - 自定义的格式语言扩展
 - 此外，我们还将通过 __getattr__ 方法实现属性的动态存取，以此取代 Vector2d 使用的只读特性——不过，序列类型通常不会这么做。


#### 10.1 Vector类：用户自定义的序列类型

序列类型的构造方法最好接受可迭代的对象为参数, 首先我们为vector加上这个构造方法

```python  
from array import array
import reprlib
import math
class Vector:
    typecode = 'd'
    def __init__(self, components):
        # 将vector的分量存储在_components中
        # self._components是迭代器
        self._components = array(self.typecode, components)
    def __iter__(self):
        return iter(self._components)
    def __repr__(self):
        # 使用 reprlib.repr() 函数获取 self._components 的有限长度表示形式
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)
    def __str__(self):
        return str(tuple(self))
    def __bytes__(self):
        return (bytes([ord(self.typecode)])+bytes(self._components))
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))
    def __bool__(self):
        return bool(abs(self))
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

```
_注： reprlib.repr 的方式需要做些说明。这个函数用于生成大型结构或递归结构的安全表示形式，它会限制输出字符串的长度，用 '...' 表示截断的部分。_    

_调用 repr() 函数的目的是调试，因此绝对不能抛出异常。如果 \_\_repr\_\_ 方法的实现有问题，那么必须处理，尽量输出有用的内容，让用户能够识别目标对象。_ 

#### 10.2 协议和鸭子类型
在 Python 中创建功能完善的序列类型无需使用继承，只需实现符合序列协议的方法。不过，这里说的协议是什么呢？
在面向对象编程中，协议是非正式的接口，只在文档中定义，在代码中不定义。例如，Python 的序列协议只需要 \_\_len\_\_ 和 \_\_getitem\_\_ 两个方法。任何类（如 Spam），只要使用标准的签名和语义实现了这两个方法，就能用在任何期待序列的地方。Spam 是不是哪个类的子类无关紧要，只要提供了所需的方法即可。

_注： 鸭子类型：“当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。”_

协议是非正式的，没有强制力，因此如果你知道类的具体使用场景，通常只需要实现一个协议的部分。例如，为了支持迭代，只需实现 \_\_getitem\_\_ 方法，没必要提供 \_\_len\_\_方法。

#### 10.3 Vector:可切片的序列
添加\_\_len\_\_ 和 \_\_getitem\_\_方法后就可以实现基本的切片了

```python
class Vector:
    # 省略了很多行
    # ...
    def __len__(self):
        return len(self._components)
    def __getitem__(self, index):
        return self._components[index]
```
但是这样实现的切片会存在一个问题， 就是切片得到的结果是数组而不是新的Vector类

##### 10.3.1 切片原理

首先通过一个例子查看切片的原理:

```python   
>>> class MySeq:
...     def __getitem__(self, index):
...         return index
... 
>>> s = MySeq()
>>> s[1]
1
>>> s[1:4]
slice(1, 4, None)
>>> s[1:4:2]
slice(1, 4, 2)
>>> s[1:4:2, 9]
(slice(1, 4, 2), 9)
>>> s[1:4:2, 7:9]
(slice(1, 4, 2), slice(7, 9, None))

```

slice(1, 4, 2) 表示的是 从1开始, 到4结束, step是2(左开右闭)

slice 有一个有趣的方法indices   

> S.indices(len) -> (start, stop, stride)
给定长度为 len 的序列，计算 S 表示的扩展切片的起始（start）和结尾（stop）索引，以及步幅（stride）。超出边界的索引会被截掉，这与常规切片的处理方式一
样。

换句话说，indices 方法开放了内置序列实现的棘手逻辑，用于优雅地处理缺失索引和负数索引，以及长度超过目标序列的切片。这个方法会“整顿”元组，把 start、stop 和stride 都变成非负数，而且都落在指定长度序列的边界内。
下面举几个例子。假设有个长度为 5 的序列，例如 'ABCDE'：

```python
>>> slice(None, 10, 2).indices(5)
(0, 5, 2)
>>> slice(-3, None, None).indices(5)
(2, 5, 1)
```
'ABCDE'[:10:2] 等同于 'ABCDE'[0:5:2]   
'ABCDE'[-3:] 等同于 'ABCDE'[2:5:1]

##### 10.3.2 能处理切片的\_\_getitem\_\_方法

对上文提到的Vector类的\_\_getitem\_\_方法 做出如下改动:

```python
def __getitem__(self, index):
    cls = type(self)
    if isinstance(index, slice):
        return cls(self._components[index])
    elif isinstance(index, numbers.Integral):   
        return self._components[index]
    else:
        msg = '{cls.__name__} indices must be integers'
        raise TypeError(msg.format(cls=cls))
```

传入slice对象时，getitem会将_components 数组的切片构建成一个新的 Vector 实例

#### 10.4 Vector 类： 动态存取属性
我们想额外提供下述句法，用于读取向量的前四个分量：

```python
>>> v = Vector(range(10))
>>> v.x
0.0
>>> v.y, v.z, v.t
(1.0, 2.0, 3.0)
```

首先我们要了解一下Python中对象的属性查找机制:

>  简单来说，对 my_obj.x 表达式，Python 会检查 my_obj 实例有没有名为 x 的属性；如果没有，到类（my_obj.__class__）中查找；如果还没有，顺着继承树继续查找。 如果依旧找不到，调用 my_obj 所属类中定义的 __getattr__ 方法，传入 self 和属性名称的字符串形式（如 'x'）。

下面我们为Vector类增加 \_\_getattr\_\_方法:

```python
shortcut_names = 'xyzt'
def __getattr__(self, name):
    cls = type(self)
    if len(name) == 1:
        pos = cls.shortcut_names.find(name)
    if 0 <= pos < len(self._components):
        return self._components[pos]
    msg = '{.__name__!r} object has no attribute {!r}'
    raise AttributeError(msg.format(cls, name)
```

这样的实现可以初步达到我们需要的效果，但是可能会出现下面的矛盾情形：

```python
>>> v = Vector(range(5))
>>> v
Vector([0.0, 1.0, 2.0, 3.0, 4.0])
>>> v.x
0.0
>>> v.x = 10
>>> v.x
10
>>> v
Vector([0.0, 1.0, 2.0, 3.0, 4.0])
```

这里对v.x赋值并没有改变Vector第一分量的值，这样赋值只是让Vector类多了一个名为x的属性。

为了避免这种情况出现我们需要实现一个\_\_setattr\_\_方法：
```python
def __setattr__(self, name, value):
    cls = type(self)
    if len(name) == 1:
        if name in cls.shortcut_names:
            error = 'readonly attribute {attr_name!r}'
        elif name.islower():
            error = "can't set attributes 'a' to 'z' in {cls_name!r}"
        else:
            error = ''
    if error:
        msg = error.format(cls_name=cls.__name__, attr_name=name)
        raise AttributeError(msg)
    super().__setattr__(name, value)
```
对单个字符的属性进行单独处理。

有一个问题要特别注意：多数时候，如果实现了 __getattr__ 方法，那么也要定义 __setattr__ 方法，以防对象的行为不一致。
如果想允许修改分量，可以使用 __setitem__ 方法，支持 v[0] = 1.1 这样的赋值，以及（或者）实现 __setattr__ 方法，支持 v.x = 1.1 这样的赋值

#### 10.5 Vector类： 散列和快速等值测试
实现\_\_hash\_\_方法，加上现有的\_\_eq\_\_方法
我们使用^（异或）运算符依次计算各个分量的散列值，像这样：v[0] ^ v[1] ^ v[2]...。需要用到归约函数reduce
![Figure-10-1](https://raw.githubusercontent.com/aldslvda/blog-images/master/fluent-python-10-1.jpg)

下面提供了三种计算累计异或的方式：
```python
>>> n = 0
>>> for i in range(1, 6):
...     n ^= i
...
>>> n
1 >>> import functools
>>> functools.reduce(lambda a, b: a^b, range(6))
1 >>> import operator
>>> functools.reduce(operator.xor, range(6))
1
```

显然第三种比较简洁， 本书的第五章讲过， 尽量避免lambda表达式的使用。

增加的\_\_hash\_\_方法如下:

```python
def __hash__(self):
    hashes = (hash(x) for x in self._components)
    return functools.reduce(operator.xor, hashes, 0)
```
这是一种映射归约运算
![Figure-10-2](https://raw.githubusercontent.com/aldslvda/blog-images/master/fluent-python-10-2.jpg)
> 映射归约：把函数应用到各个元素上，生成一个新序列（映射，map），然后计算聚合值（归约，reduce）

为了提高比较的效率修改\_\_eq\_\_方法(两种实现方式逻辑一样)：
```python
def __eq__(self, other):
    if len(self) != len(other):
        return False
    for a, b in zip(self, other):
        if a != b:
            return False
    return True

def __eq__(self, other):
    return len(self) == len(other) and all(a == b for a, b in zip(self, other))
```

#### 10.6 格式化
Vector 类的 \_\_format\_\_ 方法与 Vector2d 类的相似，但是不使用极坐标，而使用球面坐标（也叫超球面坐标），因为 Vector 类支持 n 个维度，而超过四维后，球体变成了“超球体”(n维球体)。 因此，我们会把自定义的格式后缀由 'p' 变成 'h'
下面是格式化的实现：

```python
import itertools
def angle(self, n):
    r = math.sqrt(sum(x * x for x in self[n:]))
    a = math.atan2(r, self[n-1])
    if (n == len(self) - 1) and (self[-1] < 0):
        return math.pi * 2 - a
    else:
        return a
def angles(self):
    return (self.angle(n) for n in range(1, len(self)))
def __format__(self, fmt_spec=''):
    if fmt_spec.endswith('h'): # 超球面坐标
        fmt_spec = fmt_spec[:-1]
        coords = itertools.chain([abs(self)],
        self.angles())
        outer_fmt = '<{}>'
    else:
        coords = self
        outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
    return outer_fmt.format(', '.join(components))
```

#### 10.7 小结

我们经常分析 Python 标准对象的行为，然后进行模仿，让 Vector 的行为符合 Python 风格。



