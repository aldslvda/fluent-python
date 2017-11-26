+++
topics = ["Python"]
description = "流畅的Python笔记  第三章"
draft = false
date = "2017-11-23T21:25:19+08:00"
title = "Fluent Python 第三章小结"
tags = ["Python","基础","dict","set"]
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
