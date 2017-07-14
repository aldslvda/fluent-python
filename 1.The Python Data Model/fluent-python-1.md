## Fluent Python ##
### Chapter 1. The Python Data Model ###
### Python数据模型 ###
* 特殊方法：magic method/dunder method (double underscores (i.e., \_\_getitem__()))
* 特殊方法使对象能**实现，支持基本的语言框架并与之交互**,例如：
	- Iteration 迭代
	- Collections 集合
	- Attribute access 访问属性
	- Operator overloading 运算符重载
	- Function and method invocation 函数和方法调用
	- Object creation and destruction 对象的创建和销毁
	- String representation and formatting 字符串表示和格式化
	- Managed contexts (i.e., with blocks) 管理上下文  
* namedtuple的使用：   

    ```python  
    >>> import collections
    >>> Card = collections.namedtuple('Card', ['x','y'])    
    >>> card = Card(11,22)  
    >>> print card.x
    11
    >>> print card.y
    22 
    >>> x, y = card
    >>> print x,y
    11 22   
	```

* 使用特殊方法的好处：
	- 类的使用者不需要记忆**随意定义**的标准方法名。（例如：怎样获取对象中元素的数量，.size()? .length()? 如果用特殊方法\_\_len__()可以直接调用len(object)）
	- 类的使用者更容易从Python庞大的标准库中获益，并且可以避免重造轮子（例如：random.choice函数）  
	- \_\_getitem__()方法使得类可以进行迭代(iterable),可以进行切片(index slicing)

* 使用特殊方法需要注意的：
	- 特殊方法不是给人用的，而是给Python解释器用的，一般我们用len(my_obj)而不是my\_obj.\_\_len\_\_()
	- 对于list, str, bytearray之类的内置类型，使用len()时，CPython 解释器直接返回PyVarObject的ob_size这个属性的值，这比调用__len__()方法快得多。PyVarObject是一个代表所有可变长度对象的C语言结构体。
	- 一般对特殊方法的调用都是隐式的，比如for语句隐式地调用了__iter__()函数
	- 通过内置的函数（例如 len、iter、str，等等）来使用特殊方法是最好的选择。这些内置函数不仅会调用特殊方法，通常还提供额外的好处(上面提到过)，而且对于一些内置的类来说，调用函数的速度更快。
	- 不要随意使用特殊方法的命名方式命名一般的方法，可能会造成混淆。
* 特殊方法使用的举例([构造向量](https://github.com/aldslvda/fluent-python/blob/master/1.The%20Python%20Data%20Model/1-2/numeric_types.py))：
	- 对象的字符串表示：如果没有实现\_\_repr\_\_这个特殊方法，控制台就会出现 <Vector object at 0x10e100070>这样的表示，而如果我们实现了这个方法，控制台就能将对象的详细信息打印出来。    
	  \_\_repr\_\_方法中可以使用%r 获取不同类型属性的标准字符串表示，比如Vector(1, 2) 或 Vector('1', '2')    
	  \_\_repr\_\_ 需要尽可能没有歧义，并且提示如何使用类创建相同的变量    
	  与\_\_str\_\_的不同之处在于， \_\_str\_\_在str()函数或者 print对象时会被调用，\_\_str\_\_用于展示适合展示给终端用户的信息。如果二者只能选其中一个创建，那么\_\_repr\_\_是比较好的选择，因为Python解释器在找不到\_\_str\_\_时会调用\_\_repr\_\_作为替代。([StackOverflow](https://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python))    
	- 算术运算：上面的向量对象使用\_\_add\_\_和\_\_mul\_\_实现了+和*运算。这两个运算的实现都是构造了新的对象，而不是对原来的对象进行改动。实际上这也是中缀运算的基本要求。
	- 布尔运算: Python中的对象在需要的场景(比如if, while)可以作为bool值使用。  
	  一般用户自定义的对象都被默认为True，但是如果对象实现了\_\_bool\_\_或者\_\_len\_\_，情况就不一样了。如果实现了\_\_bool\_\_,对象的布尔值视为bool()的返回值；如果没有实现\_\_bool\_\_而实现了\_\_len\_\_，那么len()为0的对象就被视为False。    
	  
* 特殊方法一览：
	The Python Language Reference的[“Data Model”](https://docs.python.org/3/reference/datamodel.html)这一章节列出了83个特殊方法，其中有47个用于实现算术运算，位运算和比较。

* 小结：
	- 通过实现特殊函数，自定义的对象可以表现得更像是内置的对象，同时使得对象的使用更加便捷，更加Pythonic
	- Python自定义对象的一个基本要求是提供自身的可用的字符串表示。一个用途是开发者用于debug和打印log，另一个用法是终端用户查看对象的信息。这两个功能分别用\_\_repr\_\_和\_\_str\_\_实现
	- 对序列类型的对象的模拟是特殊方法使用最广泛的场景，比如前面提到的[FrenchDeck](https://github.com/aldslvda/fluent-python/blob/master/1.The%20Python%20Data%20Model/1-1/card_deck.py)
	- Python 的运算符重载这一模式提供了丰富的数值类型，除了内置的类型之外，还有
decimal.Decimal 和 fractions.Fraction。这些都支持中缀运算。