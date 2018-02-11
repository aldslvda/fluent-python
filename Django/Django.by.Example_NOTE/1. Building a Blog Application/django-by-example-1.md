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
另外,可以使用virtualenvwrapper对virtualenv进行管理,这个工具可以使创建和管理virtualenv变得更加容易。

#### 1.2 使用pip安装Django
进入venv, Shell中运行下面的命令即可:  

```shell
> pip install django
```
#### 1.3 创建一个Django Project
运行下面的命令: 

```shell
> django-admin startproject aldsblog
```

这样我们得到了一个名为aldsblog的project,项目结构如下图所示（暴露了windows >_>：   
![Figure-1-1](https://github.com/aldslvda/blog-images/blob/master/djangobyexample-1.1.png?raw=true)

- manage.py: 用来和项目交互的命令行工具   
- mysite/: 项目目录，包含下面的文件:       
    - \_\_init\_\_.py: 空文件, 让Python 将项目文件夹看作一个module  
    - settings.py: 项目的相关配置(有默认值).  
    - urls.py: 定义url pattarn的文件, 每个url指向一个视图.  
    - wsgi.py: 讲项目作为WSGI应用运行的一系列配置.

自动生成的settings.py文件包含了：使用SQLite的基本设置, Django自动加入到项目中的一系列应用。   
我们需要先为项目创建初始的数据表。

由于我使用的数据库是mysql,所以要对默认的设置做出一些更改：

```python   
# in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aldsblog',
        'USER': 'root',
        'HOST': 'localhost',
        'PASSWORD': 'root',
        'PORT': '3306',
        }
}
```