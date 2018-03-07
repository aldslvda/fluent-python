## Fluent Python ##
### Chapter 9. A Pythonic Object
### 第九章: Pythonic 的对象

得益于 Python 数据模型，自定义类型的行为可以像内置类型那样自然。实现如此自然的行为，靠的不是继承，而是鸭子类型（duck typing）：我们只需按照预定行为实现对象所需的方法即可。

本章包含以下话题：  
- 支持用于生成对象其他表示形式的内置函数（如 repr()、bytes()，等等）
- 使用一个类方法实现备选构造方法
- 扩展内置的 format() 函数和 str.format() 方法使用的格式微语言
- 实现只读属性
- 把对象变为可散列的，以便在集合中及作为 dict 的键使用
- 利用 \_\_slots\_\_ 节省内存

#### 9.1 对象表示形式
Python 提供了两种方式获取对象的字符串表示形式。  

- repr() 便于开发者理解的方式返回对象的字符串表示形式。
- str() 便于用户理解的方式返回对象的字符串表示形式。

为了给对象提供其他的表示形式，还会用到另外两个特殊方法：\_\_bytes\_\_ 和\_\_format\_\_。\_\_bytes\_\_ 方法与 \_\_str\_\_ 方法类似：bytes() 函数调用它获取对象的字节序列表示形式。而 \_\_format\_\_ 方法会被内置的 format() 函数和 str.format() 方法调用，使用特殊的格式代码显示对象的字符串表示形式.

#### 9.2 构建一个向量类

向量类的实现如下：

```python  
from array import array
import math
class Vector2d:
    # typecode 是类属性，在 Vector2d 实例和字节序列之间转换时使用
    typecode = 'd'
    # 初始化向量
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    # 定义 __iter__ 方法，把 Vector2d 实例变成可迭代的对象，这样才能拆包（例如，x, y = my_vector）。这个方法的实现方式很简单，直接调用生成器表达式一个接一个产出分量。
    def __iter__(self):
        return (i for i in (self.x, self.y))
    # __repr__ 方法使用 {!r} 获取各个分量的表示形式，然后插值，构成一个字符串；因为 Vector2d 实例是可迭代的对象，所以 *self 会把 x 和 y 分量提供给 format 函数。
    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)
    def __str__(self):
        return str(tuple(self))
    # 为了生成字节序列，我们把 typecode 转换成字节序列，然后迭代 Vector2d 实例，得到一个数组，再把数组转换成字节序列。
    def __bytes__(self):
        return (bytes([ord(self.typecode)])+bytes(array(self.typecode, self)))
    # 比较向量的值
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    # √x^2+y^2
    def __abs__(self):
        return math.hypot(self.x, self.y)
    # 将模的值转化成布尔值
    def __bool__(self):
        return bool(abs(self))

```

#### 9.3 备选构造方法

上一节的vector实例可以将vector转化成字节序列，同理我们也可以将字节序列转化成vector。

vector2d_v1.py：

```python   
from vector2d_v0 import Vector2d as vec

class Vector2d(vec):
    # 类方法
    @classmethod
    # 使用cls传入类本身
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        # 创建memoryview，使用typecode转换 
        memv = memoryview(octets[1:]).cast(typecode)
        # 拆包memoryview, 构造向量
        return cls(*memv)
```

#### 9.4 classmethod 和 staticmethod
python 提供了两个装饰器来装饰类中定义的方法：classmethod 和 staticmethod

- classmethod 用来定义操作类而不是操作实例的方法。classmethod 最常见的方式就是定义备用的构造方法。
- staticmethod 用来定义与实例无关的一些操作，相当于定位在类中的普通函数

#### 9.5 格式化显示
内置的 format() 函数和 str.format() 方法把各个类型的格式化方式委托给相应的.\_\_format\_\_(format_spec) 方法。format_spec 是格式说明符，它是：format(my_obj, format_spec) 的第二个参数，或者str.format() 方法的格式字符串，{} 里代换字段中冒号后面的部分.

```python   
>>> brl = 1/2.43
>>> brl
0.4115226337448559
>>> format(brl, '0.4f') #【1】
'0.4115'
>>> '1 BRL = {rate:0.2f} USD'.format(rate=brl) #【2】
'1 BRL = 0.41 USD'

```
【1】中的'0.4f'是格式说明符
【2】中格式说明符是'0.2f', 'rate'是字段名称，'{0.mass:5.3e}'这样的格式中， '0.mass'是字段名, '5.3e'是格式

**格式规范微语言**: 格式说明符使用的表示法, 格式规范微语言是可扩展的，因为各个类可以自行决定如何解释 format_spec 参数。

首先实现一个简单的格式化方法：

```python    
def __format__(self, fmt_spec=''):
    components = (format(c, fmt_spec) for c in self)
    return '({}, {})'.format(*components)
```

这样可以实现如下效果：

```python    
>>> v1 = Vector2d(3, 4)
>>> format(v1)
'(3.0, 4.0)'
>>> format(v1, '.2f')
'(3.00, 4.00)'
>>> format(v1, '.3e')
'(3.000e+00, 4.000e+00)'
```

下面增加一个自定义的格式说明符p, 如果格式说明符以 'p' 结尾，那么在极坐标中显示向量，即 <r, θ>，其中 r 是模，θ是弧度

下面是实现：

```python    
def angle(self):
    return math.atan2(self.y, self.x)

def __format__(self, fmt_spec=''):
    if fmt_spec.endswith('p'):
        fmt_spec = fmt_spec[:-1]
        coords = (abs(self), self.angle())
        outer_fmt = '<{}, {}>'
    else:
        coords = self 
        outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
    return outer_fmt.format(*components)
```


#### 可散列的(hashable)Vector2d

目前Vectord是不可散列的， 因此不能放入集合中






