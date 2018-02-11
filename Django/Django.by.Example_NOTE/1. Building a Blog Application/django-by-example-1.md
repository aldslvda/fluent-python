## Dajango By Example Chapter 1. Building a Blog Application
## 搭建一个Blog应用

这一节的内容包括：   
- 安装Django，创建一个project    
- 设计数据模型，生成数据模型的数据库迁移
- 创建一个站点对模型进行管理
- 使用 QuerySet(查询集) and managers(管理器)
- 搭建 视图(views), 模板(templates), 和URL
- 为列表视图添加分页
- 使用Django 的内置类视图 

###  1. 安装Django, 创建一个Django Project
众所周知，Django 是Python的一个Web框架，而且同时兼容Python2.7和Python3,所以我们要先安装Python.
但是由于Django2.0(目前最新版本2.02)开始不兼容Python2.7, 所以直接安装Python3比较靠谱。
Python的安装就不赘述了。
#### 1.1 创建一个独立的Python环境
推荐使用 virtualenv 为你的Django 项目创建独立的Python环境，这样可以对不同的项目单独进行包管理,这样所有的项目都使用系统范围的Python实用的多。    
可以在Shell中运行下面的命令安装virtualenv:   
```shell   
> pip install virtualenv
```
在此之后可以使用下面的命令创建一个独立的Python环境,并激活

```shell   
> virtualenv venv
> source my_env/bin/activate
```
使用deactivate命令可以随时取消venv的激活状态。

