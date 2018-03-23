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
在面向对象编程中，协议是非正式的接口，只在文档中定义，在代码中不定义。例如，Python 的序列协议只需要 __len__ 和 __getitem__ 两个方法。任何类（如 Spam），只要使用标准的签名和语义实现了这两个方法，就能用在任何期待序列的地方。Spam 是不是哪个类的子类无关紧要，只要提供了所需的方法即可。

_注： 鸭子类型：“当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。”_





