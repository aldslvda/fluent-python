## Fluent Python ##
### Chapter 6. Design Patterns with First-Class Functions ###
### 第六章. 使用一等函数实现设计模式(1) —— 策略模式
这一章中会讲到设计模式的定义和适用场景，以及利用Python的一等函数特性对设计模式的实现。

这篇博文中先讨论策略模式。
#### 6.1 策略模式
合理利用作为一等函数的对象可以简化某些设计模式。
##### 6.1.1 经典的策略模式
《设计模式：可复用面向对象软件的基础》一书是这样概述“策略”模式的：

> 定义一系列算法，把它们一一封装起来，并且使它们可以相互替换。本模式使得算法可以独立于使用它的客户而变化。


![1](https://github.com/aldslvda/blog-images/blob/master/fluent-python-6.1.png?raw=true)

策略模式的一个经典的场景是商店的折扣策略，上图是这个场景的UML类图。具体场景如下:

> 假如一个网店制定了下述折扣规则:   
> - 有 1000 或以上积分的顾客，每个订单享 5% 折扣。   
> - 同一订单中，单个商品的数量达到 20 个或以上，享 10% 折扣。  
> - 订单中的不同商品达到 10 个或以上，享 7% 折扣。   
> - 简单起见，我们假定一个订单一次只能享用一个折扣。  

上面的UML图中:

- 上下文: 把一些计算委托给实现不同算法的可互换组件，提供服务。在这个电商示例中，上下文是 Order，它会根据不同的算法计算促销折扣。   
- 策略:实现不同算法的组件共同的接口。在这个示例中，名为 Promotion 的抽象类扮演这个角色。    
- 具体策略: "策略"的子类，fidelityPromo、BulkPromo 和LargeOrderPromo 是这里实现的三个具体策略。

上面的UML类图中，每个具体策略都是一个类，而且都只定义了一个方法，即 discount。此
外，策略实例没有状态（没有实例属性）。下面是使用Python对这个策略的重构，包括把具体策略用函数实现(而不是类)，取消了Promotion抽象类。
[示例6.1](https://github.com/aldslvda/readings/blob/master/Fluent-Python/6.%20Design%20Patterns%20with%20First-Class%20Functions/order6.1.py)

```python    
#coding=utf8
from abc import ABC, abstractmethod
from collections import namedtuple
Customer = namedtuple('Customer', 'name fidelity')
class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    def total(self):
        return self.price * self.quantity
class Order: # 上下文
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())
class Promotion(ABC) : # 策略：抽象基类
    @abstractmethod
    def discount(self, order):
    """返回折扣金额（正值）"""
    
class FidelityPromo(Promotion): # 第一个具体策略
    """为积分为1000或以上的顾客提供5%折扣"""
    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0
class BulkItemPromo(Promotion): # 第二个具体策略
    """单个商品为20个或以上时提供10%折扣"""
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount
class LargeOrderPromo(Promotion): # 第三个具体策略
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
    return 0   
```    
在这个示例中 Promotion是抽象基类(ABC)，这么做是为了使用@abstractmethod装饰器，从而明确表明所用的模式。

下面是使用不同出小折扣的Order类示例:

```python     
>>> joe = Customer('John Doe', 0)
>>> ann = Customer('Ann Smith', 1100)
>>> cart = [LineItem('banana', 4, .5),
... LineItem('apple', 10, 1.5),
... LineItem('watermellon', 5, 5.0)]
>>> Order(joe, cart, FidelityPromo())
<Order total: 42.00 due: 42.00>
>>> Order(ann, cart, FidelityPromo())
<Order total: 42.00 due: 39.90>
>>> banana_cart = [LineItem('banana', 30, .5),
... LineItem('apple', 10, 1.5)]
>>> Order(joe, banana_cart, BulkItemPromo())
<Order total: 30.00 due: 28.50>
>>> long_order = [LineItem(str(item_code), 1, 1.0)
... for item_code in range(10)]
>>> Order(joe, long_order, LargeOrderPromo())
<Order total: 10.00 due: 9.30>
>>> Order(joe, cart, LargeOrderPromo())
<Order total: 42.00 due: 42.00>
```

##### 6.1.2 使用函数实现策略模式

上面的经典实现中，每个策略是一个类，而且都只定义了一个方法discount, 此外它们都没有实例属性，因此可以用普通函数替换。下面是使用函数的一种实现。
[示例6.3](https://github.com/aldslvda/readings/blob/master/Fluent-Python/6.%20Design%20Patterns%20with%20First-Class%20Functions/order6.3.py)

```python
#coding:utf-8
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    def total(self):
        return self.price * self.quantity

class Order: # 上下文
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
            return self.__total
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())
def fidelity_promo(order):
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0
def bulk_item_promo(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount
def large_order_promo(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0    
```    
这个实例中没有抽象类，而且各个策略都是**函数**。    
下面是实际使用的输出:   

```python
>>> joe = Customer('John Doe', 0)
>>> ann = Customer('Ann Smith', 1100)
>>> cart = [LineItem('banana', 4, .5),
... LineItem('apple', 10, 1.5),
... LineItem('watermellon', 5, 5.0)]
>>> Order(joe, cart, fidelity_promo)
<Order total: 42.00 due: 42.00>
>>> Order(ann, cart, fidelity_promo)
<Order total: 42.00 due: 39.90>
>>> banana_cart = [LineItem('banana', 30, .5),
... LineItem('apple', 10, 1.5)]
>>> Order(joe, banana_cart, bulk_item_promo)
<Order total: 30.00 due: 28.50>
>>> long_order = [LineItem(str(item_code), 1, 1.0)
... for item_code in range(10)]
>>> Order(joe, long_order, large_order_promo)
<Order total: 10.00 due: 9.30>
>>> Order(joe, cart, large_order_promo)
<Order total: 42.00 due: 42.00>    
```      

可以看到应用对应的详细策略只需要将函数作为参数传入Order类，没必要像6.1一样实例化策略对象，这样会使得资源有所节省。

《设计模式：可复用面向对象软件的基础》一书的作者指出：“策略对象通常是很好的享元（flyweight）。” 那本书的另一部分对“享元”下了定义：“享元是可共享的对象，可以同时在多个上下文中使用。” 共享是推荐的做法，这样不必在每个新的上下文（这里是 Order 实例）中使用相同的策略时不断新建具体策略对象，从而减少消耗。因此，为了避免“策略”模式的一个缺点（运行时消耗），《设计模式：可复用面向对象软件的基础》的作者建议再使用另一个模式。但此时，代码行数和维护成本会不断攀升。

在复杂的情况下，需要具体策略维护内部状态时，可能需要把“策略”和“享元”模式结合起来。但是，具体策略一般没有内部状态，只是处理上下文中的数据。此时，一定要使用普通的函数，别去编写只有一个方法的类，再去实现另一个类声明的单函数接口。**函数比用户定义的类的实例轻量**，而且无需使用“享元”模式，因为各个策略函数在 Python 编译模块时只会创建一次。普通的函数也是**“可共享的对象，可以同时在多个上下文中使用”**

至此，我们使用函数实现了“策略”模式，接下来我们会在此基础上讲如何利用一致的条件选择最佳的策略。

##### 6.1.3 选择最佳策略的简单方法(暴力迭代)
使用暴力迭代的话，这个最佳策略选择的实现异常简单:

```python    
promos = [fidelity_promo, bulk_item_promo, large_order_promo]
def best_promo(order):
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)
```
这样直接将best\_promo作为参数传入Order类就行。不过这样做的缺陷是:添加新的策略要定义新的函数，并加进promos列表，否则不在best\_promo的选择范围内。

##### 6.1.4 找出模块中的全部策略
既然说到对模块中函数的遍历，就不得不提到模块的内省函数globals(),这样一说我们就知道，模块也是一等对象（。。。。![](https://github.com/aldslvda/blog-images/blob/master/acfun_emoji/11.png?raw=true)

这样我们有了新的best\_promo:    

```python   
promos = [globals()[name] for name in globals()
            if name.endswith('_promo')
                and name != 'best_promo']
def best_promo(order):
"""选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)
```

另一种方法是，在一个单独的模块(promotions.py)中保存所有策略函数，把best_promo排除在外。   

```python   
promos = [func for name, func in
            inspect.getmembers(promotions, inspect.isfunction)]
def best_promo(order):
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)
```
这个实现的缺陷是，promotions模块中的**所有函数必须是策略函数**，这种实现是强调模块内省的一种用途而不是提供完善的方案。

#### 总结
使用一等对象实现策略模式的核心思想是:
> 用"使用普通的函数"的方式代替"编写只有一个方法的类，再去实现另一个类声明的单函数接口"。将普通的函数作为可共享的对象。     
上面的例子都是基于这一思想进行优化，并且处使用一等对象的特性(函数作为参数、模块内省)。

下一篇我们会讲到命令模式，关于策略模式和命令模式的定义和场景，参见：[关于设计模式：策略模式和命令模式](https://github.com/aldslvda/readings/blob/master/Fluent-Python/6.%20Design%20Patterns%20with%20First-Class%20Functions/design-pattern-mentioned.md)

（今天好高产
![](https://github.com/aldslvda/blog-images/blob/master/acfun_emoji/17.png?raw=true)



