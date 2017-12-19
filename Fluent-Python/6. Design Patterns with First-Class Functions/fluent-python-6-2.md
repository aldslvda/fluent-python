## Fluent Python ##
### Chapter 6. Design Patterns with First-Class Functions ###
### 第六章. 使用一等函数实现设计模式(1) —— 策略模式
这一章中会讲到设计模式的定义和适用场景，以及利用Python的一等函数特性对设计模式的实现。

这篇博文中先讨论策略模式。

#### 6.2 命令模式
![命令模式的UML类图](https://github.com/aldslvda/blog-images/blob/master/fluent-python-6.2.png?raw=true)

上面的UML类图所描述的场景是"菜单驱动的文本编辑器",使用命令模式实现。各个命令可以有不同的接收者（实现操作的对象）。对 PasteCommand 来说，接收者是Document。对 OpenCommand 来说，接收者是应用程序。

命令模式的目的是解耦调用操作的对象（调用者）和提供实现的对象（接收者）。在上面所举的示例中，调用者是图形应用程序中的菜单项，而接收者是被编辑的文档或应用程序自身。

这个模式的做法是，在二者之间放一个 Command 对象，让它实现只有一个方法（execute）的接口，调用接收者中的方法执行所需的操作。这样，调用者无需了解接收者的接口，而且不同的接收者可以适应不同的 Command 子类。调用者有一个具体的命令，通过调用 execute 方法执行。注意，UML图中的 MacroCommand 可能保存一系列命令，它的 execute() 方法会在各个命令上调用相同的方法。

如何利用Python的一等对象性质对这个设计模式进行优化呢？之前讲到策略模式时我们提到过:

>  使用函数代替没有状态的类的对象

这样我们可以不为调用者提供Command对象，而是提供一个函数command。调用者不用调用command.excute(),使用command()就行。而MacroCommand可以实现成可调用的对象(实现\_\_call\_\_方法)，维护一个函数列表供以后调用。

```python   
class MacroCommand:
    """一个执行一组命令的命令"""
    def __init__(self, commands):
        self.commands = list(commands)
    def __call__(self):
        for command in self.commands:
            command()
```   

如果需要支持撤销操作(命令模式的定义中要求支持), 上面的代码可能远远不够，这时也可以使用Python提供的一些替代品:   
- 为上面的可调用示例添加属性来保存状态
- 使用函数闭包在调用之间保存函数的内部状态

这里采用的方式与“策略”模式所用的类似：把实现单方法接口的类的实例替换成可调用对象。毕竟，每个Python 可调用对象都实现了单方法接口，这个方法就是 __call__。

#### 总结

通过对策略模式和命令模式的实现，我们看到了Python的一等对象特性的使用方式:

>  设计模式或API 要求组件实现单方法接口，而那个方法的名称很宽泛，例如“execute”“run”或“doIt”。在 Python 中，这些模式或 API 通常可以使用一等函数或其他可调用的对象实现，从而减少样板(重复的)代码。

#### 关于Python语言的设计模式读物
在阅读本章之前，我也去找过设计模式相关书籍，基本都是使用Java/C#实现的，Python相关的设计模式书籍确实乏善可陈。   
Fluent-Python推荐的设计模式读物:    
- 《Python Cookbook（第 3 版）中文版》（David Beazley 和 Brian K. Jones 著）的“8.21 实现访问者模式”使用优雅的方式实现了“访问者”模式，其中的 NodeVisitor 类把方法当作一等对象处理。
- Learning Python Design Patterns（Gennadiy Zlobin 著，Packt 出版社）
- 《Python 高级编程》（Tarek Ziadé著）是市面上最好的 Python 中级书，第 14 章“有用的设计模式”从 Python 程序员的视角介绍了 7 种经典模式。
- Failed Project: Python 3 Patterns,Recipes and Idioms（http://www.mindviewinc.com/Books/Python3Patterns/Index.php）(Last updated  2015-08-04)
- 《Head First 设计模式》(这本我买了。。。。围绕Java讲的)
- 《Ruby 设计模式》（Russ Olsen 著）一书有很多见解也适用于 Python。
- 《设计模式：可复用面向对象软件的基础》一书是必读的。光是“引言”就值回书钱了(书里这么写的)
