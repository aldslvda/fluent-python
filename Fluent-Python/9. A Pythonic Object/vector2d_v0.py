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