## Fluent Python 
### Chapter 15. Context Managers and else Blocks
### 第十五章: 上下文管理器和 else 块

本章主要会讨论python中的流程控制特性
- with语句和上下文管理器
- for, while, try 语句的else子句
  
with 语句会设置一个临时的上下文，交给上下文管理器对象控制，并且负责清理上下
文。这么做能避免错误并减少样板代码，因此 API 更安全，而且更易于使用。除了自动
关闭文件之外，with 块还有很多用途。
else 子句与 with 语句完全没有关系。但是也涉及到流程控制。

#### 15.1 if语句之外的else块
else 子句不仅能在 if 语句中使用，还能在 for、while 和 try 语句中使用。

for/else、while/else 和 try/else 的语义关系紧密，不过与 if/else 差别很大。
else 子句的行为如下：
##### for
仅当 for 循环运行完毕时（即 for 循环没有被 break 语句中止）才运行 else 块。

##### while
仅当 while 循环因为条件为False而退出时（即 while 循环没有被 break 语句中止）才运行 else 块。
##### try
仅当 try 块中没有异常抛出时才运行 else 块。[官方文档](https://docs.python.org/3/reference/compound_stmts.html)还指出：“else 子句抛出的异常不会由前面的 except 子句处理。”在所有情况下，如果异常或者 return、break 或 continue 语句导致控制权跳到了复合语句的主块之外，else 子句也会被跳过。

在 Python 中，try/except 不仅用于处理错误，还常用于控制流程。为此，Python [官方词汇表](https://docs.python.org/3/glossary.html#term-eafp)还定义了两个缩略词（口号）。
- EAFP
    取得原谅比获得许可容易（easier to ask for forgiveness than permission）。这是一种常见的 Python 编程风格，先假定存在有效的键或属性，如果假定不成立，那么捕获异常。这种风格简单明快，特点是代码中有很多 try 和 except 语句。与其他很多语言一样（如 C 语言），这种风格的对立面是 LBYL 风格。接下来，词汇表定义了 LBYL。
- LBYL
　　三思而后行（look before you leap）。这种编程风格在调用函数或查找属性或键之前显式测试前提条件。与 EAFP 风格相反，这种风格的特点是代码中有很多 if 语句。在多线程环境中，LBYL 风格可能会在“检查”和“行事”的空当引入条件竞争。例如，对 if key in mapping: return mapping[key] 这段代码来说，如果在测试之后，但在查找之前，另一个线程从映射中删除了那个键，那么这段代码就会失败。这个问题可以使用锁或者 EAFP 风格解决。如果选择使用 EAFP 风格，那就要更深入地了解 else 子句，并在 try/except 语句中合理使用。

#### 15.2 with块和上下文管理

上下文管理器对象存在的目的是管理 with 语句，就像迭代器的存在是为了管理 for 语句 一样。

with 语句的目的是简化 try/finally 模式。这种模式用于保证一段代码运行完毕后执行某项操作，即便那段代码由于异常、return 语句或 sys.exit() 调用而中止，也会执行指定的操作。finally 子句中的代码通常用于释放重要的资源，或者还原临时变更的状态。

上下文管理器协议包含 \_\_enter\_\_ 和 \_\_exit\_\_ 两个方法。with 语句开始运行时，会在 上下文管理器对象上调用 \_\_enter\_\_ 方法。with 语句运行结束后，会在上下文管理器对象上调用 \_\_exit\_\_ 方法，以此扮演 finally 子句的角色。

最常见的例子是确保文件对象被关闭。在退出了with块后，文件对象变成了只能读取属性而不能进行IO操作的对象。

> 不易察觉但很重要的一点：执行 with 后面的表达 式得到的结果是上下文管理器对象，不过，把值绑定到目标变量上（as 子句）是在上下文管理器对象上调用 \_\_enter\_\_ 方法的结果。
> 不管控制流程以哪种方式退出 with 块，都会在上下文管理器对象上调用 \_\_exit\_\_ 方 法，而不是在 \_\_enter\_\_ 方法返回的对象上调用。

#### 15.3 contextlib 标准库中的上下文管理器
contextlib 模块中有一些类和函数使用范围很广。

- closing

　　如果对象提供了 close() 方法，但没有实现 __enter__/__exit__ 协议，那么可以 使用这个函数构建上下文管理器。

- suppress

　　构建临时忽略指定异常的上下文管理器。

- @contextmanager

　　这个装饰器把简单的生成器函数变成上下文管理器，这样就不用创建类去实现管理器协议了。

- ContextDecorator

　　这是个基类，用于定义基于类的上下文管理器。这种上下文管理器也能用于装饰函数，在受管理的上下文中运行整个函数。

- ExitStack

　　这个上下文管理器能进入多个上下文管理器。with 块结束时，ExitStack 按照后进 先出的顺序调用栈中各个上下文管理器的 __exit__ 方法。如果事先不知道 with 块要进入多少个上下文管理器，可以使用这个类。例如，同时打开任意一个文件列表中的所有文件。

显然，在这些实用工具中，使用最广泛的是 @contextmanager 装饰器，因此要格外留心。这个装饰器也有迷惑人的一面，因为它与迭代无关，却要使用 yield 语句。由此可以引出协程，这是下一章的主题。

在使用 @contextmanager 装饰的生成器中，yield 语句的作用是把函数的定义体分成两 部分：yield 语句前面的所有代码在 with 块开始时（即解释器调用 \_\_enter\_\_ 方法 时）执行， yield 语句后面的代码在 with 块结束时（即调用 \_\_exit\_\_ 方法时）执行。

一个例子：

```python
import contextlib

@contextlib.contextmanager 
def looking_glass():
    import sys 
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write 
    msg = '' 
    try:
        yield 'JABBERWOCKY' 
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write

    if msg:
        print(msg)

```

> 使用 @contextmanager 装饰器时，要把 yield 语句放在 try/finally 语句 中（或者放在 with 语句中），这是无法避免的，因为我们永远不知道上下文管理器 的用户会在 with 块中做什么。

> 在这节的例子中yield 与迭代没有任何关系。在本 节所举的示例中，生成器函数的作用更像是协程：执行到某一点时暂停，让客户代码运 行，直到客户让协程继续做事。

#### 15.4 小结
- 讨论了 for、while 和 try 语句的 else 子句。
- 然后，本章讨论了上下文管理器和 with 语句的作用。
- 最后，我们分析了标准库中 contextlib 模块里的函数。
- @contextmanager 装饰器优雅且实用，把三个不同的 Python 特性结合到了一起：函数装 饰器、生成器和 with 语句。









