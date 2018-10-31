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


