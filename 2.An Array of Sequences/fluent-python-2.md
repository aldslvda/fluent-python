## Fluent Python ##
### Chapter 2. An Array of Sequences ###
### 序列构成的数组 ###

* Python内置序列：
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
	
* 列表推导和生成器表达式
	- 使用生成器表达式通常可以让你的Python代码更加简洁可读，大多数情况下也会更快，比如：   
	
	```python   
	listi = [i**2 for i in xrange(10)]
	```
	
	- 