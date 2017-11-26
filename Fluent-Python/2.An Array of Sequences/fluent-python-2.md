## Fluent Python ##
### Chapter 2. An Array of Sequences ###
### 序列构成的数组 ###

* **Python内置序列**：
	一种分类方式是根据存放数据的方式分类(指针/数值)
	- 容器序列：  
		list, tuple, collections.deque.这类序列可以存放不同类型的数据，这类序列存放的都是对象的引用(指针)
	- 扁平序列：  
		str, bytes, bytearray, memoryview, array.array.只能存放一种数据类型，相比容器序列，这类序列是将元素的值直接存放在序列对应的内存空间，而不是将元素当做单独的对象存放，这类序列更加紧凑，但是只能存放数字，字节和字符。
	另一种分类方式是根据序列存放的元素是否可变分类：
	- 可变序列：  
		list, bytearray, array.array, collections.deque, memoryview
	- 不可变序列：
		tuple, str, and bytes
	序列是否可变可以通过下面的图直观展示：
	![Figure-2-1](https://raw.githubusercontent.com/aldslvda/fluent-python/master/2.An%20Array%20of%20Sequences/figure_2.1.png)
	图中列出的类都来自collections.abc(abc是 abstract base classes缩写)
	可以看到MutableSequence有很多方法继承自Sequence(箭头由子类指向超类，斜体指抽象类和抽象方法)。
	
* **列表推导和生成器表达式**  
	**1.列表推导**    
	
	- 使用列表推导通常可以让你的Python代码更加简洁可读，大多数情况下也会更快，比如：   
	
	```python   
	listi = [i**2 for i in xrange(10)]
	```
	
	- Python2中列表推导的表达式没有独立的作用域，Python3中得到了改善。
	- map/filter 可以与列表推导完成相同的工作。  
	
	```python
	symbols = '$¢£¥€¤'	beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
	beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))	
	```   
	- 示例：使用列表推导求笛卡尔积：   
	
	```python
	colors = ['black', 'white']	sizes = ['S', 'M', 'L']	tshirts = [(color, size) for color in colors for size in sizes]	
	```
	**2.生成器表达式** 
	
	- 生成器表达式背后遵守了迭代器协议，可以逐个地产出元素，而不是先建立一个完整的列表，然后再把这个列表传递到某个构造函数里。这样可以有效节省内存。
	- 示例：生成一个array:
	
	```python
	array.array('I', (ord(symbol) for symbol in symbols))  	array('I', [36, 162, 163, 165, 8364, 164]) 
	
	```
  	- 在计算笛卡尔积的这个问题中, 与列表推导不同的是，生成器表达式会在每次 for 循环运行时才生成一个组合, 而不是两个for循环生成一个含有所有元素的列表。避免了内存的额外占用。（这个不是很懂怎么做到的）
  	
  	**3.元组(tuple)**    
  	元组是对一组数据的记录，存放了一个数据和这个数据对应的位置，而不仅仅是“不可变的列表”，元组也是可以嵌套的, 当做不可变列表时，缺少那些使得自身变化的方法。   
  	
  	- for 循环可以分别提取元组里的元素，也叫作拆包（unpacking）。拆包的用法有很多：   
  	   1. 平行赋值：把一个可迭代对象里的元素，一并赋值到由对应的变量组成的元组中。     
  	   2. 不使用中间变量交换两个变量的值
  	   3. 用* 运算符把一个可迭代对象拆开作为函数的参数
  	   4. 让一个函数可以用元组的形式返回多个值   
  	拆包时可以用占位符_ 帮助处理不感兴趣的元素，也可以把注意力放在一部分元素上，用*处理剩下的元素。   
  	一个例子：
  	  
  	```python
  	t = (20, 8)
  	quotient, remainder = divmod(*t)
  	
  	```	
  **4.具名元组（namedtuple）**   
  collections.namedtuple 是一个工厂函数，它可以用来构建一个带字段名的元组和一个有名字的类  	
  
  - 一个简单的示例：   
  
  ```python
  from collections import namedtuple
  City = namedtuple('City', 'name country population coordinates')
  tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
  
  ```
  
  **5.切片**
  Python中的序列类型都支持切片操作。   
  
  - 对对象进行切片:   
    s[start:end:step] start:end:step 这种用法只能作为索引或下标用在[]中。   
    使用时会调用s.\_\_getitem\_\_(slice(start,end,step))这个方法    
    这里的start:end:step也可以替换成slice(start,end,step),这种方法可以给切片命名，使得代码更有可读性。
    
  - 省略(...)和多维切片，标准库中暂无用法，用于用户自定义类或者拓展，比如numpy。
  - 切片也可以就地修改可变序列: 如果把切片放在赋值语句的左边，或把它作为 del 操作的对象，我们就可以对序列进行嫁接、切除或就地修改操作。
  
  **6. 序列的+和\*操作**   
  
  - 如果在 a * n 这个语句中，序列 a 里的元素是对其他可变对象的引用的话,需要格外注意了,复制后的引用可能指向同一个对象，修改其中一个时，其他引用也会被修改。
  例如：
  
  ```python
  >>> s = [[1,1,1]]*3
  >>> s
[[1, 1, 1], [1, 1, 1], [1, 1, 1]]
  >>> s[0][0] = 2
  >>> s
[[2, 1, 1], [2, 1, 1], [2, 1, 1]]
  ```  
  
  - 增量赋值（+=/\*=）:
    
    1. += 背后的特殊方法是\_\_iadd\_\_(), 在a+=b中，如果a实现了\_\_iadd\_\_(),这个表达式会立刻改变a这个对象，如果没有实现这个方法,这个表达式就会完成a = a+b 的操作,即创建a+b这个对象，将变量a指向新的变量。   
       *=也类似，不过背后的特殊方法是__imul__()
    2. 一个特殊的例子：
    
    ```python
    >>> t = (1, 2, [30, 40])
    >>> t[2] += [50, 60]
    Traceback (most recent call last):
  	File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> t
(1, 2, [30, 40, 50, 60])
    ```    
  **7. sort方法和sorted函数**   
  list.sort函数会就地修改列表，返回值为None.   
  sorted函数会新建一个排好序的列表作为返回值  
  他们都接收两个参数reverse(是否反转) 和key(排序所用的值)
  
  **8. bisect用于管理已排序的序列**   
  bisect 模块包含两个主要函数，bisect 和 insort，两个函数都利用二分查找算法来在有序序列中查找或插入元素。	
  bisect(haystack,needle)    
  haystack.insert(index, needle)   
  bisort(seq, num)
  
  **9. 当列表不是首选时**
  
  - 数组（array）:如果列表只包含纯数字，array.array比list高效
  - 内存视图、NumPy SciPy, 双向队列（collections.deque）