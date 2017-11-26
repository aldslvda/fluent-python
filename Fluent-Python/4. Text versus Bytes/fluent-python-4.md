+++
topics = ["Python"]
description = "流畅的Python笔记  第四章"
draft = false
date = "2017-11-27T00:03:27+08:00"
title = "Fluent Python 第四章小结"
tags = ["Python","基础","bytes","Unicode","文本处理"]
+++

## Fluent Python ##
### Chapter 4. Texts versus Bytes ###
### 第四章.  文本和字节 ###
\* 注: 本章中讨论的所有字符和字节的问题以Python3为主
Python 3 明确区分了人类可读的文本字符串(text)和原始的字节序列(Bytes)。隐式地把字节序列转换成Unicode文本已成过去。

#### 1. 字符问题 ####
字符串是一个相当简单的概念，但是字符的定义比较复杂。
Python3的str对象中获取的单个元素是Unicode, 但是Python2的str对象获取的是原始的字节序列。
Unicode 标准把字符的标识和具体的字节表述进行了如下的明确区分:   

- 字符的标识，即码位，是 0~1 114 111(0x10fff)的数字（十进制），在 Unicode 标准中以4~6个十六进制数字表示，而且加前缀“U+”。例如，字母 A 的码位是 U+0041，欧元符号的码位是 U+20AC，高音谱号的码位是 U+1D11E。在 Unicode 6.3 中（这是 Python 3.4使用的标准），约 10% 的有效码位有对应的字符。

- 字符的具体表述取决于所用的编码。编码是在码位和字节序列之间转换时使用的算法。在 UTF-8 编码中，A（U+0041）的码位编码成单个字节 \x41，而在 UTF-16LE编码中编码成两个字节 \x41\x00。再举个例子，欧元符号（U+20AC）在 UTF-8 编码中是三个字节——\xe2\x82\xac，而在 UTF-16LE 中编码成两个字节：\xac\x20。

将码位(code points)转化成字节序列(Bytes)的过程是编码，将字符序列转化为码位的过程是解码。

#### 2.字节概要 ####
Python 内置了两种基本的二进制序列类型：Python 3 引入的不可变 bytes 类型和 Python 2.6 添加的可变bytearray 类型。   
bytes 或 bytearray 对象的各个元素是介于 0~255(0x0~0xff)之间的整数。   
bytes对象的切片还是bytes对象，最小单位是长度为1的bytes对象.     
bytearray 对象的切片还是 bytearray 对象。   
除了格式化方法（format 和 format_map）和几个处理 Unicode 数据的方法（包括casefold、isdecimal、isidentifier、isnumeric、isprintable 和 encode）之外，str 类型的其他方法都支持 bytes 和 bytearray 类型。这意味着，我们可以使用熟悉的字符串方法处理二进制序列，如 endswith、replace、strip、translate、upper等，只有少数几个其他方法的参数是 bytes 对象，而不是 str 对象。此外，如果正则表达式编译自二进制序列而不是字符串，re 模块中的正则表达式函数也能处理二进制序列.   
二进制序列有个类方法是 str 没有的，名为 fromhex: 

```python
bytes.fromhex('31 4B CE A9')
b'1K\xce\xa9'
```

新建bytes或bytearray可以调用各自的构造方法:

- 一个str对象和一个encoding参数
- 一个提供0~0xff的整数的可迭代对象
- 一个实现了缓冲协议的对象(buffer protocol, 例如bytes, bytearray, memory view, array.array)

#### 3.结构体和内存视图(struct and memory view) ####
struct 模块能处理bytes、bytearray 和 memoryview 对象, 能将打包的字节序列和不同类型字段组成的元组相互转换。   
memoryview 类不是用于创建或存储字节序列的，而是共享内存，让你访问其他二进制序列、打包的数组和缓冲中的数据切片，而无需复制字节序列。   

```python
import struct
fmt = '<3s3sHH' 
#格式：< 是小字节序，3s3s 是两个 3 字节序列，HH 是两个 16 位二进制整数。
with open('filter.gif', 'rb') as fp:
    img = memoryview(fp.read()) 
    #创建一个内存视图

header = img[:10] 
#header也是一个内存视图
bytes(header) 
# b'GIF89a+\x02\xe6\x00'
struct.unpack(fmt, header) 
# (b'GIF', b'89a', 555, 230) 分别代表文件类型,版本,宽度,高度
del header 
# 删除引用, 释放内存
del img
```

#### 4. 基本的编解码器 ####
Python 自带了超过 100 种编解码器（codec, encoder/decoder），用于在文本和字节之间相互转换。每个编解码器都有一个名称，如 'utf_8'，而且经常有几个别名，如'utf8'、'utf-8' 和 'U8'。这些名称可以传给open()、str.encode()、bytes.decode() 等函数的 encoding 参数。

```python
>>> for codec in ['latin_1', 'utf_8', 'utf_16']:
... print(codec, 'El Niño'.encode(codec), sep='\t')
...
latin_1 b'El Ni\xf1o'
utf_8 b'El Ni\xc3\xb1o'
utf_16 b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'
```

某些编码（如 ASCII 和多字节的 GB2312）不能表示所有 Unicode字符。然而，UTF 编码的设计目的就是处理每一个 Unicode 码位。  

一些典型编码:

- latin1: 一种重要的编码，是其他编码的基础，例如 cp1252 和 Unicode（注意，latin1 与cp1252 的字节值是一样的，甚至连码位也相同）
- cp1252:Microsoft 制定的 latin1 超集，添加了有用的符号，例如弯引号和€（欧元）；有些Windows 应用把它称为“ANSI”，但它并不是 ANSI 标准。
- cp437: IBM PC 最初的字符集，包含框图符号。与后来出现的 latin1 不兼容。
- gb2312:用于编码简体中文的陈旧标准；这是亚洲语言中使用较广泛的多字节编码之一。
- utf-8:目前 Web 中最常见的 8 位编码； 与 ASCII 兼容（纯 ASCII 文本是有效的 UTF-8 文本）。
- utf-16le: UTF-16 的 16 位编码方案的一种形式；所有 UTF-16 支持通过转义序列（称为“代理对”，surrogate pair）表示超过 U+FFFF 的码位。

#### 5. 编解码中出现的问题 ####
##### 5.1 UnicodeEncodeError #####
把文本转换成字节序列时，如果目标编码中**没有定义**某个字符，那就会抛出 UnicodeEncodeError

##### 5.2 UnicodeDecodeError #####
不是每一个字节都包含有效的 ASCII 字符，也不是每一个字符序列都是有效的 UTF-8 或 UTF-16。因此，把二进制序列转换成文本时，如果假设是这两个编码中的一个，遇到无法转换的字节序列时会抛出 UnicodeDecodeError    
一些陈旧的8位编码可以解码任何字节序列，不抛出错误，但是会得到无用的输出。

##### 5.3 使用预期之外的编码加载模块时抛出的SyntaxError #####
Python 3 默认使用 UTF-8 编码源码，Python 2（从 2.5 开始）则默认使用 ASCII。如果加载的 .py 模块中包含 UTF-8 之外的数据，而且没有声明编码，会抛出SyntaxError   
这个问题可以在文件的前两行加入#encoding:${encoding_name}解决。

##### 5.4 找出一个字节序列的编码 #####
单纯的字节序列是无法找出编码的，必须通过协议/规定的格式告知解码者。——有些通信协议和文件格式，如 HTTP 和 XML，包含明确指明内容编码的首部。   
但是字节流也可以通过寻找规则来判断可能的编码: 例如，如果 b'\x00' 字节经常出现，那么可能是 16 位或 32位编码，而不是 8 位编码方案，因为纯文本中不能包含空字符；如果字节序列b'\x20\x00' 经常出现，那么可能是 UTF-16LE 编码中的空格字符（U+0020）    
统一字符编码侦测包 Chardet（https://pypi.python.org/pypi/chardet）就是这样工作的，它能识别所支持的 30 种编码.    

##### 5.5 BOM：有用的鬼符 #####
utf-16编码的序列开头会有几个额外的字节，称为BOM，即字节序标记（byte-order mark），指明字节序。
小字节序设备中，低8位在前，高8位在后，大字节序的设备则反之。   
UTF-16 有两个变种：UTF-16LE，显式指明使用小字节序；UTF-16BE，显式指明使用大字节序。如果使用这两个变种，不会生成 BOM    
与字节序有关的问题只对一个字（word）占多个字节的编码（如 UTF-16 和 UTF-32）有影响。UTF-8 的一大优势是，不管设备使用哪种字节序，生成的字节序列始终一致，因此不需要 BOM。   

#### 6. 处理文本 ####
处理文本的最佳实践是“Unicode 三明治”（要尽早把输入（例如读取文件时）的字节序列解码成字符串，处理过程全部用字符串，输出时尽量晚编码成字符序列)
![Figure-4-1](https://github.com/aldslvda/blog-images/blob/master/fluent-python-4.1.png?raw=true)

文本处理中的一些要点:

- 需要在多台设备中或多种场合下运行的代码，一定不能依赖默认编码。打开文件时始终应该明确传入 encoding= 参数，因为不同的设备使用的默认编码可能不同。
- 除非想判断编码，否则不要在二进制模式中打开文本文件；即便如此，也应该使用 Chardet，而不是重新发明轮子（参见 4.4.4 节）。常规代码只应该使用二进制模式打开二进制文件。

#### 7. 为了正确的比较规范化Unicode 字符串 ####
在 Unicode 标准中，'é'和 'e\u0301' 这样的序列叫“标准等价物”（canonical equivalent），应用程序应该把它们视作相同的字符。但是，Python 看到的是不同的码位序列，因此判定二者不相等。    
上述的问题的解决方案是规范化Unicode字符串。通常是使用 unicodedata.normalize 函数提供的 Unicode 规范化。第一个参数是'NFC'、'NFD'、'NFKC' 和 'NFKD'之一。   
NFC（Normalization Form C）使用最少的码位构成等价的字符串，而 NFD 把组合字符分解成基字符和单独的组合字符。这两种规范化方式都能让比较行为符合预期。
NFKC 和 NFKD的首字母缩略词中，字母 K 表示“compatibility”（兼容性）。这两种是较严格的规范化形式，对“兼容字符”有影响。    
**由于这一节的内容的领域偏向性太过严重，一般工作不会见到，只是略作了解，碰到相关问题再细查**

#### 8. 支持字符串和字节序列的双模式API ####
##### 8.1 正则表达式 #####

如果使用字节序列构建正则表达式，\d 和 \w 等模式只能匹配 ASCII 字符；相比之下，如果是字符串模式，就能匹配 ASCII 之外的 Unicode 数字或字母。

```python
import re
re_numbers_str = re.compile(r'\d+')
re_words_str = re.compile(r'\w+')
re_numbers_bytes = re.compile(rb'\d+')
re_words_bytes = re.compile(rb'\w+')
text_str = ("Ramanujan saw \u0be7\u0bed\u0be8\u0bef" 
" as 1729 = 1³ + 12³ = 9³ + 10³.") 
text_bytes = text_str.encode('utf_8') 
print('Text', repr(text_str), sep='\n ')
print('Numbers')
print(' str :', re_numbers_str.findall(text_str)) 
print(' bytes:', re_numbers_bytes.findall(text_bytes)) 
print('Words')
print(' str :', re_words_str.findall(text_str)) 
print(' bytes:', re_words_bytes.findall(text_bytes)) 
```

上面这段代码的输出:

> 4
> b'caf\xc3\xa9' 5
> café
> NicktheMega13:4. Text versus Bytes NickAl$ python3 fp4.py
> Text
>  'Ramanujan saw ௧௭௨௯ as 1729 = 1³ + 12³ = 9³ + 10³.'
> Numbers
>  str : ['௧௭௨௯', '1729', '1', '12', '9', '10']
>  bytes: [b'1729', b'1', b'12', b'9', b'10']
> Words
>  str : ['Ramanujan', 'saw', '௧௭௨௯', 'as', '1729', '1³', '12³', '9³', '10³']
>  bytes: [b'Ramanujan', b'saw', b'as', b'1729', b'1', b'12', b'9', b'10']

##### 8.2 os函数 #####
GNU/Linux 内核不理解 Unicode，对任何合理的编码方案来说，在文
件名中使用字节序列都是无效的，无法解码成字符串。在不同操作系统中使用各种客户端的文件服务器，在遇到这个问题时尤其容易出错。    
为了规避这个问题，os 模块中的所有函数、文件名或路径名参数既能使用字符串，也能使用字节序列。如果这样的函数使用字符串参数调用，该参数会使用sys.getfilesystemencoding() 得到的编解码器自动编码，然后操作系统会使用相同的编解码器解码。这几乎就是我们想要的行为，与 Unicode 三明治最佳实践一致。   
利用这一特性可以修复一些含有鬼符的文件名。

#### 9. 总结 ####
随着 Unicode 的广泛使用（80% 的网站已经使用 UTF-8），我们必须把文本字符串与它们在文件中的二进制序列表述区分开，而 Python 3 中这个区分是强制的。   
这一部分要解决的问题大多是一些由于地区/语言不通造成的编码差异，这种差异可以通过规范化Unicode解决,也可以通过规范化编码解决。   
Unicode 异常复杂，充满特殊情况，而且要覆盖各种人类语言和产业标准策略。所以要做到完美的处理非常困难。    
Python 3.3 起，创建 str 对象时，解释器会检查里面的字符，然后为该字符串选择最经济的内存布局：如果字符都在 latin1 字符集中，那就使用 1 个字节存储每个码位；否则，根据字符串中的具体字符，选择 2 个或 4 个字节存储每个码位。
Python 3 对 int 类型的处理方式：如果一个整数在一个机器字中放得下，那就存储在一个机器字中；否则解释器切换成变长表述，类似于Python 2 中的 long 类型。
